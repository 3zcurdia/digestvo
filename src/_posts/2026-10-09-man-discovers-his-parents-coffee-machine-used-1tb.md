---
layout: post
title: "Man discovers his parents' coffee machine used 1TB of data in 10 days"
date: 2026-10-09 08:51:10 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://www.dexerto.com/entertainment/man-discovers-his-parents-coffee-machine-used-1tb-of-data-in-10-days-3416399/"
hn_url: "https://news.ycombinator.com/item?id=49995495"
summary: >-
  A man auditing his parents' home network found their smart Keurig coffee
  machine had generated a full terabyte of traffic in just ten days, and
  shared the discovery in a viral X post. He says he has worked in IT for more
  than ten years and helps his parents manage their internet setup remotely.
  After the post gained attention, he clarified that most of the traffic
  stayed inside the house rather than crossing his internet uplink, and called
  it "likely a bug with this unit" that saturated his access point. Rather
  than dig deeper, he unplugged the machine and is buying his parents a new
  coffee maker.
---

Most commenters treat the episode as proof that consumer IoT does not belong on
a normal home network, and several answer with practical exits: a separate IoT
VLAN, an ESPhome dongle, or a fifteen-year-old dumb Moccamaster. The substantive
fight is over what the terabyte actually was. Grombobulous argues it cannot be
deliberate, because no manufacturer would pay to ingest a terabyte every two
weeks from millions of machines, and mindslight does the arithmetic — 1.1MB/sec
is roughly 17,000 sixty-four-byte probes per second, more than an ESP32-class
chip can even push — before conceding it still smells like a bug. The sharpest
objection comes from altairprime, relaying the original X thread: the volume
mostly stayed local, so the scandal is not the bandwidth but that the machine
scans your household to build data Keurig sells to advertisers. That reframing
splits the thread on consent — handing a device your Wi-Fi password is implied
consent, several say, against the view that ordinary buyers cannot be expected
to know their coffee maker is mapping the house.
