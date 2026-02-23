# Whop marketing kit (seller-only)

This folder is **for you (seller)** to create Whop listing visuals + social posts.

It is placed under `tools/` so it is **excluded from the customer release ZIP** by `tools/release_zip.ps1`.

## 1) Add the shared banner image

1. Put your *old bot image* here:
   - `tools/whop_marketing/assets/old-bot.png`

PNG works best. If you only have JPG, rename it to `old-bot.jpg` and update the `<img>` path in `banner_shared.html`.

## 2) Generate the shared banner

Open `banner_shared.html` in a browser.

- It’s designed as a single “master” at **1920×1080**.
- It also contains safe crop guides for:
  - **1200×630** (link preview)
  - **1500×500** (wide header)

Export by taking a screenshot or using your browser’s “Save as PDF” then converting to PNG.

## 3) Screenshot checklist

Use `screenshot_shotlist.md` to capture consistent, no-secrets screenshots.

## 4) Copy/paste posts

Use `post_copy.md` for:

- Whop listing description (compliant, no profit promises)
- Launch post
- FAQ snippets
