---
layout: archive
title: "Projects"
permalink: /projects/
author_profile: true
---
{% include base_path %}

{% assign featured = site.data.projects | where_exp: "p", "p.id == 'mining-licenses-africa'" | first %}
{% include data/project-item.html item=featured %}

---

# Other projects

{% assign other_projects = site.data.projects | where_exp: "p", "p.id != 'mining-licenses-africa' and p.id != 'rare-earth-africa'" %}
{% for p in other_projects %}{% include data/project-item.html item=p %}{% endfor %}


