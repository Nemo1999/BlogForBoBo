---
layout: page
title: "所有討論"
permalink: /discussions/
---

# 👁️ 所有哲學討論

按時間順序排列的完整對話記錄。

{% assign sorted_discussions = site.discussions | sort: 'date' | reverse %}

{% for discussion in sorted_discussions %}
## [{{ discussion.title }}]({{ discussion.url | relative_url }})

**日期**: {{ discussion.date | date: "%Y年%m月%d日" }}

{% if discussion.excerpt %}
{{ discussion.excerpt | strip_html | truncate: 200 }}
{% endif %}

{% if discussion.categories.size > 0 %}
**分類**: 
{% for category in discussion.categories %}
{{ category }}{% unless forloop.last %}, {% endunless %}
{% endfor %}
{% endif %}

{% if discussion.tags.size > 0 %}
**標籤**: 
{% for tag in discussion.tags %}
{{ tag }}{% unless forloop.last %}, {% endunless %}
{% endfor %}
{% endif %}

---
{% endfor %}

## 按分類瀏覽

{% assign categories = site.discussions | map: 'categories' | flatten | uniq | sort %}

{% for category in categories %}
### {{ category }}
{% for discussion in site.discussions %}
{% if discussion.categories contains category %}
- [{{ discussion.title }}]({{ discussion.url | relative_url }}) ({{ discussion.date | date: "%Y-%m-%d" }})
{% endif %}
{% endfor %}
{% endfor %}

## 按標籤瀏覽

{% assign tags = site.discussions | map: 'tags' | flatten | uniq | sort %}

{% for tag in tags %}
### {{ tag }}
{% for discussion in site.discussions %}
{% if discussion.tags contains tag %}
- [{{ discussion.title }}]({{ discussion.url | relative_url }}) ({{ discussion.date | date: "%Y-%m-%d" }})
{% endif %}
{% endfor %}
{% endfor %}

---

[返回首頁](/)