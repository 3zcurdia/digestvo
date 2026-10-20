---
layout: page
title: Temas
prose: false
summary: >-
  Cada historia está archivada en un tema. Sigue un tema para leer el resto.
---

<%
  tags = TagTaxonomy.index(collections.posts.resources)
%>

<% if tags.any? %>
  <ul data-pagefind-ignore class="m-0 list-none divide-y divide-border-color p-0" role="list">
    <% tags.each do |tag| %>
      <li class="group relative flex items-baseline justify-between gap-4 py-4 card-focus">
        <h2 class="m-0 font-serif text-[1.375rem] leading-[1.2] font-[650] tracking-[-0.005em] text-balance text-heading-color">
          <a class="link-card group-hover:text-action-color" href="<%= tag[:path] %>"><%= tag[:display] %></a>
        </h2>
        <span class="font-meta text-sm leading-[1.6] text-muted-color"><%= tag[:count] %> <%= tag[:count] == 1 ? "historia" : "historias" %></span>
      </li>
    <% end %>
  </ul>
<% else %>
  <p class="text-muted-color">Aún no hay temas.</p>
<% end %>
