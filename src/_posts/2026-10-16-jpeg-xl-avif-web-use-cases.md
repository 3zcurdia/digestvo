---
layout: post
title: "JPEG XL vs AVIF for web use-cases"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://jakearchibald.com/2026/jpeg-xl-vs-avif/"
lobsters_url: "https://lobste.rs/s/uejdwj/jpeg_xl_vs_avif_for_web_use_cases"
share_text: "AVIF beats JPEG XL by 15–25% on photos — unless the metric is lying to you"
summary: >-
  Jake Archibald benchmarked AVIF against JPEG XL (libjxl and jixel encoders)
  across photos, screenshots, illustrations, transparency, HDR, and lossless
  after JPEG XL landed in all major browsers. AVIF produced smaller lossy
  files in almost every web case, typically 15–25% smaller than JPEG XL for
  photos and far smaller for screenshots and transparency. JPEG XL won for
  lossless compression and for losslessly shrinking existing JPEGs by 9–20%.
  The verdict: default to AVIF 4:4:4 for web images, and try jixel JPEG XL
  only when AVIF yields an unusually large file.
---

Most commenters land on a tidy split — AVIF for images you ship, JPEG XL for
masters and lossless archives — because Archibald's numbers show AVIF 15–25%
smaller on photos and far ahead on screenshots and alpha, while JPEG XL
dominates lossless. The sharpest objection concerns the SSIMULACRA2 metric
biasing results toward AVIF, because a commenter re-ran the comparison under
Butteraugli and found JPEG XL winning at high quality and narrowing the
mid-quality gap, with the author conceding the newer jixel encoder shows visible
artifacts the metric misses. A second argument over methodology questions
serving 1598px-wide images scaled down by CSS, since downscaling hides artifacts
that fullscreen viewing reveals. The most useful correction is that a picture
element does not let the browser pick the best format, so shipping every format
is wasted effort compared with tuning one.
