---
layout: post
title: "Shipping JPEG XL in Chrome"
date: 2026-10-07 09:11:08 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://developer.chrome.com/blog/jpeg-xl-in-chrome"
hn_url: "https://news.ycombinator.com/item?id=49991227"
summary: >-
  Chrome is shipping JPEG XL decoding starting in Chrome 155, reversing the
  removal it made back in Chrome 110. The post explains that the decoder is
  jxl-rs, a pure Rust rewrite of the libjxl decoder, chosen because image
  decoders parse untrusted bytes inside the renderer and the Chromium rule of
  two pushes memory-safe code. Matching the speed of C required stabilizing a
  Rust SIMD feature and building a SIMD abstraction layer inspired by Google's
  Highway, with performance numbers tracked on a public dashboard. Chrome
  credits Interop 2026 developer feedback for the decision and recommends
  trying both AVIF and JPEG XL.
---

Most commenters land on the view that the reversal is being forced from outside
Google: the PDF Association picked JXL as the next PDF image format, so browsers
that want to render PDFs need a decoder anyway, and exposing that decoder to img
tags too is free. The sharpest objection is to the cynical internal-politics
story - that JXL was dropped to protect AVIF/WebP and revived so someone can
claim a promotion - because Google employees wrote the spec, the reference
decoder and jxl-rs, and Chrome's original deprecation notice never cited
security or AVIF as the reason. The counter-theory, pushed hardest by a couple
of commenters, is that another giant C codec was simply a liability worth owning
until the Rust rewrite made it cheap, since libjxl had a long bug history and
Project Zero had warned against insecure decoders. A smaller fight breaks out
over codec quality: one commenter insists AVIF still wins below one bit per
pixel, another reports the opposite for tiny thumbnails.
