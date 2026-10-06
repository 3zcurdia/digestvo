---
layout: page
title: All stories
prose: false
---

<%= render Shared::PostList.new(posts: collections.posts.resources) %>

<p class="mt-8 border-t border-border-color pt-4 font-meta text-sm leading-[1.6] font-semibold">
  <a class="text-action-color no-underline underline-offset-[0.18em] focus-visible:rounded-[2px] focus-visible:outline-2 focus-visible:outline-action-color focus-visible:outline-offset-[3px]" href="<%= relative_url '/tags' %>">Browse by topic<span aria-hidden="true">&nbsp;&rarr;</span></a>
</p>
