---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
---

<div style="border: 1px solid #ccc; border-radius: 6px; padding: 16px; background: #f9f9f9; max-width: 720px; margin-bottom: 2em;">

  <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 1em;">
    <a href="https://github.com/BaptisteVandecrux" target="_blank" style="text-decoration: none;">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="110" />
    </a>
    <img src="https://github-readme-stats.vercel.app/api?username=BaptisteVandecrux&show_icons=true&hide=issues&theme=default" alt="GitHub stats" style="max-width: 100%; height: auto;" />
  </div>

  <div style="display: flex; align-items: center;">
    <img src="https://github-contributions-api.deno.dev/BaptisteVandecrux.svg" alt="GitHub contribution graph" style="border: 1px solid #ddd; border-radius: 6px; padding: 8px; background: #fff; max-width: 100%;" />
  </div>

</div>



### Selected repositories:
{% include base_path %}

{% for post in site.code reversed %}
  {% include archive-single.html %}
{% endfor %}