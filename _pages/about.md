---
permalink: /
title: "Data-oriented Economist, PhD"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---


<p><strong>Technical Skills:</strong> {% include data/skill-list.html categories="programming,cloud-tools" %}</p>

## Education

<ul>
{% for e in site.data.education %}{% include data/education-item.html item=e %}{% endfor %}
</ul>

## Work Experience

{% for x in site.data.experience %}{% include data/experience-item.html item=x %}{% endfor %}

## Projects

{% assign public_projects = site.data.projects | where_exp: "p", "p.audience contains 'public'" %}
{% for p in public_projects %}
<p><strong>{{ p.title }}</strong>: {{ p.summary | markdownify | remove: "<p>" | remove: "</p>" }} {% if p.id == "rare-earth-africa" %}<a href="/portfolio/">Learn more</a>{% else %}<a href="/projects/">Learn more</a>{% endif %}</p>
{% endfor %}


