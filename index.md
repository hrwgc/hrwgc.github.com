---
layout: page
title: Home
tagline: start here.
---
{% include JB/setup %}

## Recent posts


<table class="pdfs table table-striped table-bordered">
	<thead>
		<tr><th>Date</th><th>Title</th></tr>
	</thead>
	<tbody>
  {% for post in site.posts %}
    <tr><td>{{ post.date | date_to_string }}</td><td><a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></td></tr>
  {% endfor %}
</tbody>
</table>


<!-- <ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul> -->
