---
layout: page
title: All stories
prose: false
---

<%= render Shared::PostList.new(posts: collections.posts.resources) %>
