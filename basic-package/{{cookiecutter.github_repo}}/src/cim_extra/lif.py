# type: ignore
from collections import namedtuple

import numpy as np
import pandas as pd
import plotnine as gg
import polars as pl
from matplotlib import pyplot as plt
from numpy.typing import ArrayLike, NDArray
from scipy.stats import laplace, norm


def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def norm_pdf_pts(n=25, mu=0.0, sigma=1.0, alpha=0.01) -> NDArray:
    left = norm.ppf(alpha, mu, sigma)
    right = norm.ppf(1 - alpha, mu, sigma)
    p_spaced = np.linspace(left, right, n)
    return norm.pdf(p_spaced, mu, sigma)


def filter1d_DoG(data: ArrayLike, k=5, sigma=0.2) -> NDArray:
    filt_1 = norm_pdf_pts(k, 0.0, 1.0)
    filt_2 = norm_pdf_pts(k, 0.0, sigma)
    return np.convolve(data, filt_1, mode="same") - np.convolve(
        data, filt_2, mode="same"
    )


def unit_osc(t, hz):
    return np.sin(np.pi * hz * t) ** 2.0


def gsmoother(data, n=5):
    f = norm_pdf_pts(n)
    f = f / f.sum()
    out = np.convolve(data, f, mode="valid")
    s = len(out)
    d = len(data)
    l = int(round((d - s) / 2.0))
    r = int(d - (s + l))
    return np.pad(out, (l, r), "edge")


def seed_from_string(string, max_char=8):
    return int("".join([f"{ord(t)}" for i, t in enumerate(string) if i < max_char]))


class LIF:
    def __init__(
        self,
        sampling_interval=0.0002,
        offset=0.01,
        tau_m=0.025,
        tau_a=0.02,
        adapt_init=2.0,
        noise_multiplier=3.5,
        peak=3.0,
        valley=0.0,
        threshold=1.0,
        seed=111111,
    ):
        self._dt = sampling_interval  # ........... simulation time step [s]
        self._adapt = adapt_init  # ............... increment in adaptation current [nA]
        self.noise_multiplier = noise_multiplier  # noise intensity
        self.offset = offset  # ................... offset curent [nA]
        self.tau_m = tau_m  # ..................... membrane time_constant [s]
        self.tau_a = tau_a  # ..................... adaptation time_constant [s]
        self.v_threshold = threshold  # ........... spiking threshold
        self.v_peak = peak  # ..................... voltage after reaching threshold
        self.v_valley = valley  # ................. reset voltage after spiking
        self._seed = seed  # ...................... seed for random number generator
        self._reset()

    def _reset(self):
        self._rng = np.random.default_rng(self._seed)
        self._step = 0
        self._export = namedtuple(
            "state",
            ["elapsed_t", "stim_s", "membrane_v", "adaptation_i", "noise_e", "spike_b"],
        )
        self.elapsed_t = 0.0  # ...... current time [s]
        self.stim_s = 0.0
        self.membrane_v = 0.0  # ..... current membrane voltage
        self.adaptation_i = 0.0  # ... current adaptation current
        self.noise_e = 0.0  # ........ current noise value
        self.spike_b = False  # ...... current spike indicator

    def _update(self, stim_value):
        self.stim_s = stim_value
        self.noise_e = (
            self.noise_multiplier
            * self._rng.choice([-1.0, 1.0])
            * self._rng.beta(100.0, 100.0)
        )

        self.adaptation_i -= self._dt / self.tau_a * self.adaptation_i

        self.membrane_v += (
            self._dt
            * (
                -self.membrane_v
                - self.adaptation_i
                + stim_value
                + self.noise_e
                + self.offset
            )
            / self.tau_m
        )

        if self._step > 1:
            if self.spike_b:
                self.spike_b = False
                self.membrane_v = self.v_valley
                self.adaptation_i += self._adapt

            if self.membrane_v > self.v_threshold:
                self.spike_b = True
                self.membrane_v = self.v_peak

        self._step += 1
        self.elapsed_t += self._dt

    def current_state(self):
        return self._export._make(
            [getattr(self, field) for field in self._export._fields]
        )

    def make(self, stim, n=None):
        self._reset()
        if isinstance(stim, (np.ndarray, list)):
            n = min(n or len(stim), len(stim))
        else:
            default_n = 500
            n = n if n is not None else default_n
            stim = np.tile(stim, n)

        for i in range(n):
            self._update(stim[i])
            yield self.current_state()

    def run(self, stimulus, n=None, frame="polars"):
        fieldnames = self._export._fields
        generator = self.make(stimulus, n)
        array = [list(s) for s in generator]

        if frame == "polars":
            return pl.DataFrame(array, columns=fieldnames)

        elif frame == "pandas":
            return pd.DataFrame(array, columns=fieldnames)

        elif frame == "numpy":
            dtypes = [float if f != "spike_b" else bool for f in fieldnames]
            return np.array(array, dtype=list(zip(fieldnames, dtypes)), ndmin=2)

        else:
            return list(generator)


class SpikeSim:
    def __init__(
        self,
        total_duration=3.0,
        sampling_interval=0.0002,
        *,
        seed=111111,
    ):
        self.seed = seed
        self.rng = np.random.default_rng(self.seed)
        self.total_duration = total_duration
        self.sampling_interval = sampling_interval
        self.time = np.arange(
            self.rng.uniform(-self.sampling_interval * 3, 0),
            self.total_duration,
            self.sampling_interval,
        )
        self._reset_stim()
        self._reset_signal()

    def _reset_stim(self):
        self.stim = np.ones_like(self.time)
        self.stim_shown = np.zeros_like(self.time, dtype=bool)
        self.stim_onsets = np.empty(0)
        self.stim_extents = np.empty(0)
        self.stim_values = np.empty(0)
        self.stim_duration = 0.0
        self.sts = np.empty(0)

    def _reset_signal(self):
        self.membrane_voltage = np.empty(0)
        self.spike_times = np.empty(0)
        self._lif_data = pl.DataFrame()
        self.waveform = np.empty(0)

    def _nearest_ts_idx(self, t, time_vec):
        return int(np.argmin(np.abs(time_vec - t)))

    def stimulus(
        self,
        stim_duration=0.1,
        min_val=5.0,
        max_val=300.0,
        *,
        n_freqs=None,
        stim_type="wave",
        shuffle=False,
    ):
        self._reset_stim()

        self.stim_duration = min(stim_duration, self.total_duration / 3.0)

        self.stim_onsets = np.cumsum(
            self.rng.uniform(
                self.stim_duration * 3,
                self.stim_duration * 4,
                int(np.ceil(self.total_duration / self.stim_duration)),
            )
            - self.stim_duration * 2
        )
        self.stim_onsets = self.stim_onsets[
            self.stim_onsets < (self.total_duration - self.stim_duration)
        ]

        freqs = np.linspace(
            max(min_val, 1e-10), max_val, n_freqs or len(self.stim_onsets)
        )
        self.stim_values = np.resize(freqs, len(self.stim_onsets))
        if shuffle:
            self.rng.shuffle(self.stim_values)
        self.stim_extents = np.zeros_like(self.stim_onsets)

        for stim_index, onset in enumerate(self.stim_onsets):
            idx = (self.time >= onset) & (self.time < onset + self.stim_duration)
            ts = self.time[idx]
            value = self.stim_values[stim_index]
            if stim_type in ["wave", "pulse"]:
                stim_vec = unit_osc(ts - ts.min(), value)
            elif stim_type in ["square", "const"]:
                stim_vec = ts * 0 + value
            else:
                raise ValueError(
                    'stim_type must be one of ["wave", "pulse", "square", "const"]'
                )
            self.stim[idx] = stim_vec
            self.stim_shown[idx] = True
            self.stim_extents[stim_index] = ts.max() - ts.min()

        self.stim[np.bitwise_not(self.stim_shown)] = 0.0

        return self

    def signal(self, **kwargs):
        self._reset_signal()
        if not np.any(self.stim_shown):
            return self

        kwargs.update(
            {
                "sampling_interval": self.sampling_interval,
                "seed": kwargs.get("seed", self.seed),
                "peak": kwargs.get("peak", max(3.0, self.stim_values.max())),
            }
        )

        lif = LIF(**kwargs)

        self._lif_data = lif.run(self.stim, frame="polars")

        self.membrane_voltage = (
            self._lif_data.select(pl.col("membrane_v")).to_numpy().flatten()
        )

        self.spike_times = (
            self._lif_data.select([pl.col("elapsed_t").filter(pl.col("spike_b"))])
            .to_numpy()
            .flatten()
        )

        return self

    def STS(self, delay=0.02):
        if not np.any(self.spike_times):
            return np.empty(0)

        step_back = int(round(delay / self.sampling_interval))
        sts = np.zeros((len(self.spike_times), step_back))
        for i, t in enumerate(self.spike_times):
            idx = self._nearest_ts_idx(t, self.time)
            stim_set = self.stim[max(0, idx - step_back) : idx]
            sts[i, -len(stim_set) :] = stim_set
        self.sts = sts
        return self.sts

    def get_waveforms(self, span=0.01):
        if not np.any(self.spike_times):
            return np.empty(0)

        steps = int(round(span / self.sampling_interval / 2.0))
        steps = max(1, steps)
        freqs = []

        stepsize = steps * 2 + 1
        signals = np.empty((len(self.spike_times), stepsize))
        signals.fill(np.NaN)
        for i, spike in enumerate(self.spike_times):
            idx = self._nearest_ts_idx(spike, self.time)
            left = idx - steps
            right = idx + steps + 1
            spike_range = np.arange(left, right)
            spike_range[
                np.bitwise_or(spike_range < 0, spike_range > len(self.time) - 1)
            ] = -1
            sig = np.tile(np.NaN, len(spike_range))
            past_stim_onsets = self.stim_onsets[spike > self.stim_onsets]
            if np.any(past_stim_onsets):
                spike_stim = past_stim_onsets[
                    self._nearest_ts_idx(spike, past_stim_onsets)
                ]

                # self.stim_shown[spike_range]
                freqs.append(self.stim_values[self.stim_onsets == spike_stim])
                sig[spike_range >= 0] = self.membrane_voltage[
                    spike_range[spike_range >= 0]
                ]
            else:
                freqs.append(np.NaN)

            signals[i, :] = sig

        self.waveform = gsmoother(np.nanmean(signals, 0))
        return self.waveform

    def plot(self):
        df = pd.DataFrame(self._lif_data.to_numpy(), columns=self._lif_data.columns)
        p = (
            gg.ggplot(gg.aes(x="elapsed_t", y="membrane_v"), data=df)
            + gg.geom_area(gg.aes(y="stim_s"), fill="#8d9ab2")
            + gg.geom_line(color="#e36e527f", size=1)
            + gg.labs(
                x="time(s)",
                y="membrane voltage and stimulus",
                title="Signal recording given stimulus",
            )
        )
        p
        return p

    def plot_waveform(self):
        df = pd.DataFrame(
            dict(
                time=np.arange(len(self.waveform)) * self.sampling_interval,
                waveform=self.waveform,
            )
        )
        p = (
            gg.ggplot(gg.aes(x="time", y="waveform"), data=df)
            + gg.geom_line(color="#e36e527f", size=1.5)
            + gg.labs(
                x="time(s)",
                y="signal (mean)",
                title="Average waveform centered around spikes",
            )
        )
        p
        return p
