---
layout: page
title: Topics
prose: false
summary: >-
  Every story is filed under one topic. Follow a topic to read the rest.
---

<%
  tags = TagTaxonomy.index(collections.posts.resources)
%>

<% if tags.any? %>
  <ul class="m-0 list-none divide-y divide-border-color p-0" role="list">
    <% tags.each do |tag| %>
      <li class="group relative flex items-baseline justify-between gap-4 py-4 has-[a:focus-visible]:outline-2 has-[a:focus-visible]:outline-action-color has-[a:focus-visible]:outline-offset-4">
        <h2 class="m-0 font-serif text-[1.375rem] leading-[1.2] font-[650] tracking-[-0.005em] text-balance text-heading-color">
          <a class="text-heading-color no-underline after:absolute after:inset-0 after:content-[''] focus-visible:outline-none group-hover:text-action-color" href="<%= tag[:path] %>"><%= tag[:display] %></a>
        </h2>
        <span class="font-meta text-sm leading-[1.6] text-muted-color"><%= tag[:count] %> <%= tag[:count] == 1 ? "story" : "stories" %></span>
      </li>
    <% end %>
  </ul>
<% else %>
  <p class="text-muted-color">No topics yet.</p>
<% end %>
