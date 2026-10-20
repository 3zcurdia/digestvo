---
layout: page
title: Todas las historias
prose: false
search: true
---

<%= render Shared::Search.new %>

<div data-search-archive>
  <%= render Shared::PostList.new(posts: collections.posts.resources) %>

  <p class="mt-8 border-t border-border-color pt-4 font-meta text-sm leading-[1.6] font-semibold">
    <a class="link-accent focus-ring" href="<%= relative_url '/tags' %>">Explorar por tema<span aria-hidden="true">&nbsp;&rarr;</span></a>
  </p>
</div>
