---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
---

<a href="https://github.com/BaptisteVandecrux" target="_blank" style="display: inline-flex; align-items: center; gap: 8px;">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="28" />
  <strong>Visit my GitHub profile</strong>
</a>

<img src="https://github-readme-stats.vercel.app/api?username=BaptisteVandecrux&show_icons=true&hide=issues&theme=default" alt="GitHub stats" />

<!-- Green square contribution graph on light background -->
<img src="https://github-contributions-api.deno.dev/BaptisteVandecrux.svg" alt="GitHub contribution graph" style="border: 1px solid #ddd; border-radius: 6px; padding: 8px; background: #fff;" />
### Selected repositories:
{% include base_path %}

{% for post in site.code reversed %}
  {% include archive-single.html %}
{% endfor %}