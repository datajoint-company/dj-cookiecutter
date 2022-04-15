{% raw %}
{%
   include-markdown "../README.md"
   comments=false
   start="<!--intro-start-->"
   end="<!--intro-end-->"
   heading-offset=0
%}
{%
   include-markdown "../README.md"
   rewrite-relative-urls=false
   comments=false
   start="<!--install-start-->"
   end="<!--install-end-->"
   heading-offset=0
%}
{%
   include-markdown "../README.md"
   comments=false
   start="<!--rest-of-doc-start-->"
   end="<!--rest-of-doc-end-->"
   heading-offset=0
%}{% endraw %}
