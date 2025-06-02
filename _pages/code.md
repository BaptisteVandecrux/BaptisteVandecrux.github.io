---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
---

<img src="https://github-readme-stats.vercel.app/api?username=BaptisteVandecrux&show_icons=true&hide=issues" />
![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=BaptisteVandecrux&theme=github)
{% include base_path %}

{% for post in site.code reversed %}
  {% include archive-single.html %}
{% endfor %}
