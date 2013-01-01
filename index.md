---
layout: page
title: Home
tagline: start here.
---
{% include JB/setup %}

## PDFs

<table class="pdfs table table-striped table-bordered">
	<thead>
		<tr><th>Date</th><th>Title</th><th>PDF</th><th>Source</th></tr>
	</thead>
	<tbody>
  {% for post in site.posts %}
    {% if post.category == 'pdf' and post.page_url != "" and post.local_pdf != "" %} 
    <tr><td>{{ post.date | date_to_string }}</td><td>{{ post.title }}</td><td><a href="{{ post.local_pdf | replace: '../hrwgc-pdf/data/', 'data-src/pdf/' }}">PDF</a></td><td><a href="{{ post.page_url }}">Source</a></td></tr>
    {% endif %}
  {% endfor %}
</tbody>
</table>

### Recent posts

<!-- <ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul> -->
