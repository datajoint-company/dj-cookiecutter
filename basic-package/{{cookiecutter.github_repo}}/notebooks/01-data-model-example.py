# ~~
from datajoint_utilities.dj_search.lists import drop_schemas

import {{cookiecutter.__pkg_import_name}}.pipeline

drop_schemas("my_pipeline", dry_run=False, force_drop=True)
drop_schemas(None, dry_run=False, force_drop=True)


# ~~
import datetime as dt
import warnings

import datajoint as dj
import numpy as np
from datajoint_utilities.generic.typed import subset, utc_timestamp
from faker import Faker

from cim_extra.lif import SpikeSim, seed_from_string
from {{cookiecutter.__pkg_import_name}}.tables import Block, DataArray, Group, Tag, schema_core

warnings.filterwarnings("ignore")

# ~~
rng = np.random.default_rng(0)
markers1 = np.array([1, 8])
markers2 = np.array([markers1 - 1, markers1, markers1 + 1])
dataset1 = rng.random(markers1.max() + 2)
dataset2 = rng.random(len(dataset1))
dataset1[markers1] = 2.0
dataset2[markers1] = 1.5
dataset3 = np.mean(dataset1[np.vstack((markers1 - 1, markers1, markers1 + 1))], 1)
dataset4 = dataset2[markers2]

block = Block.create_new(
    "example.session",
    "block",
    uuid="dfcdab44-87f0-91fa-6a0d-f970b49af93e",
    description="it's a block",
)

dim1 = dict(type="SampledDim", axis=1, sampling_interval=0.02, unit="s")
array1 = DataArray.create_new(
    "example.session.signal",
    "signal",
    block_uuid=block,
    data=dataset1,
    description="analog signal",
    units="mV",
    label="membrane potential",
    dimensions=dim1,
)

array2 = DataArray.create_new(
    "example.session.stimulus",
    "stimuli",
    block_uuid=block,
    data=dataset2,
    description="stimulus source",
    units="Lm",
    label="Stimuli",
    dimensions=[dict(type="SetDim", axis=1, axis_label="Stim")],
)

array3 = DataArray.create_new(
    "example.session.waveform",
    "waveform",
    block_uuid=block,
    data=dataset3,
    description="average waveform of spikes",
)

array4 = DataArray.create_new(
    "example.session.sts",
    "sts",
    block_uuid=block,
    data=dataset4,
    description="spike triggered stimulus",
)

feat1 = [dict(feature_uuid=array3, link_type="untagged")]
tag1 = Tag.create_new(
    "example.session.spiketrain",
    "spike train",
    data_array_uuid=array1,
    position=markers1,
    features=feat1,
)

tag2 = Tag.create_new(
    "example.session.spikestim",
    "spike stimuli",
    data_array_uuid=array2,
    position=markers2,
    features=dict(feature_uuid=array4, link_type="untagged"),
)

dj.list_schemas()

# def get_features():
#     return DataArray * DataArrays & (dj.U("feature_uuid") & Tag.Feature).proj(data_array_uuid="feature_uuid")

# feature_uuid, data_array_uuid = (Tag.Feature & (Tag & (Tags & "name='spike train'"))).fetch("feature_uuid", "data_array_uuid")
# ids = np.append(data_array_uuid, feature_uuid)
# DataArray & [{"data_array_uuid": i} for i in ids.tolist()]

# Tag.Feature * DataArray
# # DataArray & {"data_array_uuid": }
# data_array_uuid = DataArray.fetch("data_array_uuid", as_dict=True)
# DataArray &
# (Tag * Tags) & "name='spike train'"
# ~~
schema_core.list_tables()


# ~~
di_core_schema = dj.Diagram(schema_core)
di_core_lookups = dj.Diagram.from_sequence([Blocks, Groups, DataArrays, Tags])
di_core_schema
di_core_schema - di_core_lookups


# ~~ [markdown]
#  ## Example Data
#
#  ### Simple Leaky Integrate and Fire Model
#
#  **Datasets**:
#
#  - Timestamps
#  - Stimulus vector
#  - Cell voltage recording
#  - Spike timestamps
#  - Spike-triggered stimulus array
#  - Waveform

# ~~
def run_simul(seed=12345):
    spike_data = SpikeSim(total_duration=3.0, sampling_interval=0.002, seed=seed)
    spike_data.stimulus(
        stim_duration=0.25,
        min_val=0.25,
        max_val=1.5,
        n_freqs=6,
        stim_type="const",
        shuffle=True,
    )
    spike_data.signal()
    spike_data.STS(delay=0.02)
    spike_data.get_waveforms(span=0.05)
    return spike_data


spike_data = run_simul()


# ~~
import polars as pl

pl.concat([spike_data._lif_data.head(), spike_data._lif_data.tail()])


# ~~
spike_data.plot()


# ~~
spike_data.plot_waveform()


# ~~
def import_data(seed=12345):
    spike_data = run_simul(seed)
    waveform = spike_data.waveform
    sts = spike_data.sts
    voltage = spike_data.membrane_voltage
    spikes = spike_data.spike_times
    stimuli = spike_data.stim
    return dict(
        stimuli=dict(
            data=stimuli,
            name="constant stimulus",
            type="single_channel.stimuli",
            label="Stimulus amplitude (constant)",
            units="Lum",
            data_type=str(stimuli.dtype),
            shape=stimuli.shape,
            dimensions=dict(
                ranges=[
                    dict(
                        axis=1,
                        sampling_interval=spike_data.sampling_interval,
                        offset=spike_data.time.min(),
                        unit="s",
                        unit_name="Seconds",
                        axis_label="Stim values",
                    )
                ],
            ),
        ),
        voltage=dict(
            data=voltage,
            name="membrane voltage",
            type="single_channel.voltage",
            label="Regularly sampled voltage",
            units="mV",
            data_type=str(voltage.dtype),
            shape=voltage.shape,
            dimensions=dict(
                sampled=[
                    dict(
                        axis=1,
                        sampling_interval=spike_data.sampling_interval,
                        offset=spike_data.time.min(),
                        unit="s",
                        unit_name="Seconds",
                        axis_label="Time",
                    )
                ]
            ),
        ),
        presentations=dict(
            name="Stimulus onset/offset time",
            type="presentations",
            position=spike_data.stim_onsets,
            extent=spike_data.stim_extents,
            units="s",
        ),
        spikes=dict(
            data=spikes,
            name="spike times",
            type="spikes",
            label="Spike times from a single channel neuron",
            units="s",
            data_type=str(spikes.dtype),
            shape=spikes.shape,
        ),
        waveform=dict(
            data=waveform,
            name="spike waveforms",
            type="waveform",
            label="waveform from around spike times",
            units="mV",
            data_type=str(waveform.dtype),
            shape=waveform.shape,
        ),
        sts=dict(
            data=sts,
            name="spike triggered stimulus",
            type="sts",
            label="Stimulus values around each spike time",
            units="Lum",
            data_type=str(sts.dtype),
            shape=sts.shape,
            dimensions=dict(
                ranges=[
                    dict(
                        axis=1,
                        ticks=spikes,
                        axis_label="Spike",
                    )
                ],
                sets=[
                    dict(
                        axis=2,
                        labels=[f"px{i}" for i in map(str, range(1, sts.shape[1] + 1))],
                        axis_label="Stim values",
                    )
                ],
            ),
        ),
    )


# ~~ [markdown]
#  ## Incorporating into existing elements example

# ~~
dj.Diagram(db_subject)


# ~~
Subject()


# ~~ [markdown]
#  ## Simulate data
#
#  Multi-trial, multi-session recordings per subject.
#
#  - Subject
#    - Session
#      - Trial
#      - ...
#      - Trial
#    - ...
#    - Session
#  - Subject
#    - ...
#

# ~~
def generate_subjects(n_mice=5):
    fake = Faker()
    Faker.seed(12345)
    rng = np.random.default_rng(12345)
    return [
        {
            "subject": fake.first_name().lower(),
            "sex": rng.permuted(["M", "F"])[0],
            "birth_date": utc_timestamp(fake.date_of_birth(maximum_age=2)),
            "comment": fake.sentence(),
        }
        for _ in range(n_mice)
    ]


# Manual insert into Subject table
Subject.insert(generate_subjects(), skip_duplicates=True)
Subject()


# ~~ [markdown]
#  ## Subject Recording Tables

# ~~
rng = np.random.default_rng(12345)
schema = dj.Schema("my_pipeline")


# ~~ [markdown]
#  ### Session table

# ~~
@schema
class Session(dj.Imported):
    definition = """
    -> Subject
    session_datetime: BIGINT UNSIGNED
    ___
    session_num : SMALLINT UNSIGNED
    -> Block
    """

    def make(self, key):
        dob = (Subject & key).fetch1("birth_date")

        # up to 3 sessions at 2 months intervals as days
        session_days = (60 * (rng.random(rng.choice(3) + 1) + 1)).astype(int)

        # add some hours and add to dob to get session date after dob
        session_datetime = np.sort(
            np.array(
                [
                    int(rng.random() * 1e9 + utc_timestamp(dt.timedelta(days=d)) + dob)
                    for d in session_days.tolist()
                ]
            )
        )

        for n, sessdate in enumerate(session_datetime, 1):
            session = {"session_num": n, "session_datetime": sessdate, **key}
            session |= Block.create_new(
                "ephys recording session",
                "session.ephys",
                session=session,
            ).fetch1("KEY")
            self.insert1(session)


# ~~ [markdown]
#  ### Trial table

# ~~
@schema
class Trial(dj.Imported):
    definition = """
    -> Session
    trial_num : SMALLINT UNSIGNED
    ---
    -> Block
    """

    def make(self, key):
        n_trials = rng.choice(4) + 1
        for t in range(n_trials):
            trial = {"trial_num": t + 1, **key}
            trial |= Block.create_new(
                "ephys recording trial",
                "trial.ephys",
                trial=trial,
            ).fetch1("KEY")
            self.insert1(trial)


# ~~ [markdown]
#  ### Recording table

# ~~
@schema
class Recording(dj.Imported):
    definition = """
    -> Trial
    """

    class Stimulus(dj.Part):
        definition = """
        -> DataArray
        -> Recording
        """

    class Voltage(dj.Part):
        definition = """
        -> DataArray
        -> Recording
        """

    class Spikes(dj.Part):
        definition = """
        -> Tag
        -> Recording
        """

    def make(self, key):
        # key
        seed_val = f'{key["subject"]}{key["session_datetime"]}{key["trial_num"]}'
        data = import_data(seed=seed_from_string(seed_val))
        block_uuid = (Trial & key).fetch1("block_uuid")
        master_pk = {**key, "block_uuid": block_uuid}
        print(master_pk)
        self.insert1(key, allow_direct_insert=True)

        # --- insert membrane voltage data ---
        voltage = data["voltage"]
        volt_dta = DataArray.create_new(
            **subset(
                voltage,
                "name",
                "type",
                "data",
                "shape",
                "data_type",
                "units",
                "label",
            ),
            block=block_uuid,
        )
        volt_dta_pk = volt_dta.fetch1("KEY")

        voltage_dim = voltage["dimensions"]["sampled"][0]
        voltage_dim |= volt_dta_pk
        DataArray.SampledDim.insert1(voltage_dim, ignore_extra_fields=True)
        self.Voltage.insert1({**volt_dta_pk, **master_pk})

        # --- insert voltage tag (spikes) ---
        spikes = data["spikes"]
        tag_dta = Tags.create_new(
            **subset(spikes, "name", "type"),
            uuid_parts=dict(data=spikes["data"]),
            insert1_kwargs=dict(skip_duplicates=True),
        )
        tag_dta_pk = tag_dta.fetch1("KEY")
        tag_dta_pk |= volt_dta_pk
        tag_dta_pk |= {"position": spikes["data"], "units": spikes["units"]}
        Tag.insert1(tag_dta_pk)
        self.Spikes.insert1({**tag_dta_pk, **master_pk}, ignore_extra_fields=True)


# ~~
Session()

# ~~
@schema
class SpikeFeatures(dj.Computed):
    definition = """
    -> Recording.Spikes
    """

    class Waveform(dj.Part):
        definition = """
        -> Tag.Feature
        -> SpikeFeatures
        """
        # # --- insert voltage feature (waveform of spikes) ---
        # waveform = data["waveform"]
        # feature = Features.create_new(
        #     **subset(waveform, "name", "type"), skip_duplicates=True
        # )
        # feature_entry = {"feature_uuid": feature.fetch1("feature_uuid")}
        # feature_entry |= subset(tag_entry, "block_uuid", "data_array_uuid", "tag_uuid")

    class STS(dj.Part):
        definition = """
        -> Tag.Feature
        -> SpikeFeatures
        """


# ~~ [markdown]
#  ## Populate tables

# ~~
Trial()

# ~~
Session.populate()
Session * Blocks
Trial.populate()
Trial * Blocks
Recording.populate(limit=1)
Recording * Blocks

# ~~
subject = {"subject": Subject.fetch("subject", limit=1)[0]}
subject


# ~~
(Session & subject) * Blocks * DataArray


# ~~
# subj_trials = (Trial & subject) * Blocks
# key = subj_trials.fetch("KEY", limit=1)[0]
# del key["block_uuid"]

# ~~
Blocks()


# ~~
DataArrays()


# ~~
Tags()


# ~~
Groups()
