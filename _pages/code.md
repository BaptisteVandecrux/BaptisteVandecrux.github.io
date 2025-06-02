---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
---

<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: center;">
  <div style="flex: 0 0 auto; display: flex; align-items: center;">
    <a href="https://github.com/BaptisteVandecrux" target="_blank" style="text-decoration: none;">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="110" />
    </a>
  </div>

  <div style="flex: 1 1 auto; display: flex; justify-content: center;">
    <img src="https://github-readme-stats.vercel.app/api?username=BaptisteVandecrux&show_icons=true&hide=issues&theme=default" alt="GitHub stats" style="max-width: 100%; height: auto;" />
  </div>
    <img src="https://github-contributions-api.deno.dev/BaptisteVandecrux.svg" alt="GitHub contribution graph" style="border: 1px solid #ddd; border-radius: 6px; padding: 8px; background: #fff; max-width: 100%;" />

</div>


### Selected repositories:
{% include base_path %}

{% for post in site.code reversed %}
  {% include archive-single.html %}
{% endfor %}