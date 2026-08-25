---
layout: archive
title: "Portfolio"
permalink: /portfolio/
author_profile: true
---
{% include base_path %}

{% assign rare_earth = site.data.projects | where_exp: "p", "p.id == 'rare-earth-africa'" | first %}
{% include data/project-item.html item=rare_earth %}

The search included the following keywords:

<ul>
{% for k in rare_earth.search_keywords %}<li>{{ k }}</li>{% endfor %}
</ul>
