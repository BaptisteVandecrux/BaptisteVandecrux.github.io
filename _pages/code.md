---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
---

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; background: #f9f9f9; margin-bottom: 2em;">

  <a href="https://github.com/BaptisteVandecrux" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none; color: inherit;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="28" />
    <strong>Visit my GitHub profile</strong>
  </a>
  <img src="https://github-readme-stats.vercel.app/api?username=BaptisteVandecrux&show_icons=true&hide=issues&theme=default" alt="GitHub stats" style="max-width: 100%;" />
  <img src="https://github-contributions-api.deno.dev/BaptisteVandecrux.svg" alt="GitHub contribution graph" style="border: 1px solid #ddd; border-radius: 6px; padding: 8px; background: #fff; max-width: 100%;" />

</div>


### Selected repositories:
{% include base_path %}

{% for post in site.code reversed %}
  {% include archive-single.html %}
{% endfor %}