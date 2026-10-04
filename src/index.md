---
layout: default
---

<%= render Shared::PostList.new(posts: collections.posts.resources, limit: 10, lead: true, more_url: relative_url("/posts")) %>
