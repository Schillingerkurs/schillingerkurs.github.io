---
layout: archive
title: "Teaching"
permalink: /teaching_ta/
author_profile: true
redirect_from:
  - /teach
---
{% include base_path %}

# Teaching experience

I have taught as a Teaching Assistant the following undergraduate courses on political economy and statistical methods.

<ul>
{% for t in site.data.teaching %}{% include data/teaching-item.html item=t %}{% endfor %}
</ul>
