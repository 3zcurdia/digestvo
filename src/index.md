---
layout: default
---

<%= render Shared::PostList.new(posts: collections.posts.resources, lead: true, more_url: relative_url("/posts"), latest_day: true) %>
