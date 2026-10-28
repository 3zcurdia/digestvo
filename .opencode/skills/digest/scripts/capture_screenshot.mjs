#!/usr/bin/env node
/**
 * Capture one article's initial viewport as a social-card screenshot.
 *
 * Usage:
 *     node capture_screenshot.mjs <article-url> <output.jpg>
 *
 * The image is exactly 1200x630, the dimensions declared by the site's
 * Open Graph metadata. The browser lives inside node_modules, so run
 * `PLAYWRIGHT_BROWSERS_PATH=0 npx playwright install chromium` once after a
 * fresh `npm install`.
 */

import fs from "node:fs/promises";
import path from "node:path";

if (!process.env.PLAYWRIGHT_BROWSERS_PATH) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = "0";
}

const [urlArg, outputArg] = process.argv.slice(2);

if (!urlArg || !outputArg) {
  console.error("usage: capture_screenshot.mjs <article-url> <output.jpg>");
  process.exit(2);
}

let url;
try {
  url = new URL(urlArg);
} catch {
  console.error(`capture failed: not a URL: ${urlArg}`);
  process.exit(2);
}
if (url.protocol !== "http:" && url.protocol !== "https:") {
  console.error(`capture failed: unsupported URL scheme: ${url.protocol}`);
  process.exit(2);
}

const output = path.resolve(outputArg);
if (path.extname(output).toLowerCase() !== ".jpg") {
  console.error(`capture failed: output must be a .jpg file: ${outputArg}`);
  process.exit(2);
}

const WIDTH = 1200;
const HEIGHT = 630;
const NAV_TIMEOUT_MS = 30_000;
const SETTLE_MS = 1_200;

let browser;
try {
  const { chromium } = await import("playwright");
  await fs.mkdir(path.dirname(output), { recursive: true });
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1,
    colorScheme: "light",
    locale: "en-US",
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  await page.goto(url.href, {
    waitUntil: "domcontentloaded",
    timeout: NAV_TIMEOUT_MS,
  });
  // Advertising and analytics rarely finish, and none of them decide what the
  // headline looks like, so only the load event gets a bounded wait. The short
  // settle gives late hero images and web fonts a chance to paint.
  await page.waitForLoadState("load", { timeout: 5_000 }).catch(() => {});
  await page.evaluate(() => document.fonts?.ready).catch(() => {});
  await page.waitForTimeout(SETTLE_MS);
  await page.screenshot({
    path: output,
    type: "jpeg",
    quality: 85,
    animations: "disabled",
    caret: "hide",
  });
  const stat = await fs.stat(output);
  if (stat.size < 1024) {
    throw new Error(`screenshot is implausibly small (${stat.size} bytes)`);
  }
  await context.close();
  console.log(`${url.href} -> ${output} (${WIDTH}x${HEIGHT}, ${stat.size} bytes)`);
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  const hint = message.includes("Executable doesn't exist")
    ? "\nRun: PLAYWRIGHT_BROWSERS_PATH=0 npx playwright install chromium"
    : "";
  console.error(`capture failed: ${message}${hint}`);
  process.exitCode = 1;
} finally {
  await browser?.close().catch(() => {});
}
