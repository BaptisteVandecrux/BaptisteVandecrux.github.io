---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include publication_stats.md %}


{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
