---
layout: post
title: "What I Self-Host"
date: 2026-10-15 09:41:50 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: "https://viceconsole.fyi/blog/2026/10/10/what-i-self-host/"
lobsters_url: "https://lobste.rs/s/j4tlzg/what_i_self_host"
share_text: "One EUR 180 mini PC runs 28 self-hosted services — but who watches the self-hosted watcher?"
summary: >-
  Fed up with streaming services and their engagement tricks, the author moved
  nearly everything onto one Beelink mini PC — an Intel N100 with 16 GB RAM
  bought for EUR 180 — and now runs 28 self-hosted services: 17 native
  binaries and 11 Podman containers, all managed by systemd. The inventory
  spans Jellyfin, Immich, Frigate with 8 IP cameras, Home Assistant, Caddy,
  Vaultwarden, and Restic backups, with htop showing only 7.5 GB of memory in
  use. His ground rules: expose nothing to the public internet (his ISP sits
  behind CGNAT), prefer single-binary native services over compose stacks, and
  no Docker at all.
---

Most commenters land on the article's one blind spot: self-hosting Uptime Kuma,
because the monitor dies with the machine it watches. The sharpest objection is
markerz's — a full disk or a power cut takes the self-hosted prober down with
everything else, which is why he keeps monitoring in the cloud. The replies
answer with specifics: a tiny Oracle always-free VPS used exclusively for
probing, a healthchecks.io dead-man's switch that alerts when the prober stops
checking in, and technomancy's most-upvoted idea — self-hosters trading
monitoring and backups with each other as mutual aid instead of buying B2
storage. A second argument runs over Tailscale: readers fear dependence on it,
one switched to plain WireGuard for a two-server setup, and Headscale users
report every release forces a config-file edit.
