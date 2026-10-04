---
layout: page
title: Videos
prose: false
description: >-
  Videos worth the watch, with the key insights pulled out of each one so you
  can decide before pressing play.
summary: >-
  Things I watched and would watch again. Each one carries the points that
  actually mattered, so you can read the argument or go watch it argued.
---

<%= render Shared::VideoList.new(videos: collections.videos.resources) %>