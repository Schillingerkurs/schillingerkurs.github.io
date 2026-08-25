---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
redirect_from:
  - /publications
---
{% include base_path %}

# Working paper

Please [email](mailto:fs.egb@cbs.dk) me for the latest drafts.

{% assign working_papers = site.data.publications | where_exp: "p", "p.status == 'working_paper'" %}
{% for p in working_papers %}{% include data/publication-item.html item=p %}{% endfor %}

# Under review

{% assign under_review = site.data.publications | where_exp: "p", "p.status == 'under_review'" %}
{% for p in under_review %}{% include data/publication-item.html item=p %}{% endfor %}
