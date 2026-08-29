---
layout: archive
title: "News"
permalink: /news/
author_profile: true
---

A feed of my posts and reposts from LinkedIn.

{% assign posts = site.data.linkedin_posts %}

{% if posts and posts.size > 0 %}
{% assign posts = posts | sort: "id" | reverse %}
<div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: center;">
  {% for post in posts %}
  <div style="flex: 1 1 400px; max-width: 504px;">
    <iframe src="https://www.linkedin.com/embed/feed/update/{{ post.urn }}" height="{{ post.height | default: 500 }}" width="100%" frameborder="0" allowfullscreen="" title="LinkedIn post" style="border-radius: 6px; display: block; width: 100%;"></iframe>
  </div>
  {% endfor %}
</div>
{% else %}
<p><em>No posts featured yet — check back soon, or follow me directly on <a href="https://www.linkedin.com/in/baptiste-vandecrux-962bba40/?locale=en_US" target="_blank">LinkedIn</a>.</em></p>
{% endif %}
