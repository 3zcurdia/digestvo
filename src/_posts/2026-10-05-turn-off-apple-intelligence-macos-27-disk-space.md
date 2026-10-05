---
layout: post
title: "Turn off Apple Intelligence on macOS 27 and get its disk space back"
date: 2026-10-05 09:09:57 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://github.com/omlahore/RemoveMacAI"
hn_url: "https://news.ycombinator.com/item?id=49957116"
summary: >-
  macOS 27 no longer ships a single switch for Apple Intelligence, and its
  downloaded models stay on disk even after the features are turned off.
  RemoveMacAI is a small Apple-silicon CLI that applies Apple's own
  restriction keys through a configuration profile, deletes the foundation,
  image-generation, Spatial Photos and Clean Up models via the asset service,
  and redirects their downloads to a closed local port so macOS never fetches
  them again. The whole thing is reversible with removemacai revert. It
  installs through a curl-piped script or a Homebrew tap, and every release is
  built by GitHub Actions with a verifiable build-provenance attestation.
---

Most commenters land on the install method rather than the tool: the README's
curl pipe to bash one-liner drew the loudest reply, kicking off a long argument
over whether piping a stranger's script into a shell is actually worse than npm
install or pip install. The sharpest objection runs both ways. Defenders note
the script only fetches a SHA-256-checked, attestation-verified binary from the
same repo, and that package managers already execute arbitrary setup.py and
postinstall code anyway, so the outrage is theatre. Critics counter that a
mutable server-side script defeats the shared-artifact property that makes a
fixed release zip auditable once for everyone, and that the intended audience is
developers with enterprise credentials in their environment. A second split is
over whether the prize justifies the trouble: owners of 256GB laptops call 14GB
of models 10-20% of their disk, while others say Apple Intelligence just works
now and only people who cannot spare the storage care.
