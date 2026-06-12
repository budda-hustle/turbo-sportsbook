#!/usr/bin/env python3
"""
Downloads all Figma CDN images from homepage.html,
renames them to safe filenames, saves to assets/images/,
and produces index.html with relative paths.
"""

import re, os, urllib.request, shutil

BASE = "/sessions/gracious-youthful-allen/mnt/TurboSportsbook home"
HTML_IN  = f"{BASE}/homepage.html"
HTML_OUT = f"{BASE}/index.html"
IMG_DIR  = f"{BASE}/assets/images"
os.makedirs(IMG_DIR, exist_ok=True)

# UUID → safe filename mapping
NAMES = {
    "4079676d-d097-41f6-93a8-be187859cf9f": "header-mobile.png",
    "851e3776-19d6-453f-a37f-39666792f64f": "icon-search-vec.png",
    "bd64e901-be51-4d57-95a4-1b6ca6f0bcfd": "icon-mybets.png",
    "ef047c77-3a4d-4182-9bbc-fa099b03e240": "icon-settings.png",
    "5a3d05a4-922d-4af2-b670-086a616ae0bc": "hero-banner-bg.png",
    "fe63203c-5134-4c01-8e9e-4f25154e6351": "icon-popular.png",
    "4a954766-ffa1-4610-873f-e0755452ccfa": "icon-arrow-down-vec.png",
    "4a66bfb8-53d8-43d2-9778-a11a8c9599de": "icon-basketball.png",
    "ffa09a70-1fb6-4a7f-9f92-e2f0b38cdc23": "icon-fav-blank-vec.png",
    "88a3dcf9-9d78-4949-b529-22c34c1d8f8d": "team-orlando-magic.png",
    "eb039887-6a74-41de-890d-ac9796a1c66e": "team-indiana-pacers.png",
    "e5641f46-66ba-4403-b7d1-89423751a2a2": "icon-arrow-right-vec.png",
    "704dd180-cca4-4beb-bae8-373842c53ba4": "icon-insights-vec.png",
    "67bfb4c9-0f2a-4933-b15a-88acdf5d2569": "icon-stream-vec.png",
    "f5fcad9a-1101-492d-bddf-75b3bc79e52f": "team-miami-heat.png",
    "ddb9f2d5-ef09-4df6-a0c4-d196dd1d855e": "team-detroit-pistons.png",
    "e956016d-fff2-41da-9ef7-ae0d6ccc3aad": "icon-baseball.png",
    "8105bf66-ea1b-4b25-8ea0-63ca3b160a20": "icon-insights-base.png",
    "d1d176e9-787d-42f4-b566-e59da104f80f": "icon-hot-vec.png",
    "7825e65a-15c1-4a77-991c-40d770cde6d8": "team-ny-yankees.png",
    "54589d76-54c4-426b-a3f2-a64ebafa35e3": "team-la-dodgers.png",
    "ece6289a-3eb3-4391-9557-ecf4d3fd81f9": "icon-arrow-right-swipe-vec.png",
    "302c1309-6d25-4a0e-b7b9-91b45b4cfd74": "icon-live-tag.png",
    "dcc5c7ae-e5fe-4411-8587-af65d3d77dc6": "icon-coming-up.png",
    "a9ba4a7d-53d0-4848-9685-c43a118728a3": "icon-fav-tag-vec.png",
    "eb994d0a-c2c8-49ae-ba2a-539db4802758": "icon-turbo-rocket-vec.png",
    "fd96ee48-ef04-424b-9d8e-938aa4e9a1ad": "icon-arrow-right-turbo-vec.png",
    "eb4f1a7c-a759-4f3c-bcf4-627494fe0297": "team-combo-1.png",
    "1824c7b0-9d6c-4bc0-887b-a811e1fbc982": "team-combo-2.png",
    "da43b0c5-0e6e-4aa8-a758-cd2a241cda91": "team-combo-3.png",
    "484b7cff-b371-4b22-bb0c-492409c669e5": "team-combo-4.png",
    "cc56d4f0-29f7-4db2-a13a-49b5406c1177": "team-combo-5.png",
    "d0f9df43-fdbb-4ab4-ab29-d974c94efd07": "icon-american-football.png",
    "e80cad91-1ec6-47ef-ba33-f07fe13a0ee2": "team-houston-texans.png",
    "5a8822b9-76a2-4b87-9681-26a6c094cf36": "icon-live-vec.png",
    "6e48260b-f2ae-4354-ac6d-2a3540074489": "icon-insights-live-vec.png",
    "6e1bedaf-ad1e-4d3e-88e4-c51e374060f3": "icon-stream-live-vec.png",
    "e942778c-e2cf-4246-96e5-1748a5a33270": "icon-fav-live-vec.png",
    "392a768b-3a34-47db-aadd-0dc761d5c172": "team-boston-celtics.png",
    "d09018fc-997a-491c-9af9-a9d9a8558593": "team-milwaukee-bucks.png",
    "b7426c90-8050-4fe6-af13-d54057f808fd": "icon-hot-live-vec.png",
    "427911b2-6381-4d5d-99d3-0e2fd3b113d1": "team-ny-knicks.png",
    "fec1fef8-ae44-4210-91e2-89ce86bb2b4b": "team-cleveland-cavs.png",
    "d19b1c19-82bb-4de6-997c-72c0fe20a544": "icon-arrow-right-live-vec.png",
    "4c6d1d3d-0ebf-4f94-a67d-937bf5c8cdf6": "leaderboard-hero-bg.png",
    "b5bd3b5a-2482-4892-bcef-2e5aa5460e24": "leaderboard-places-bg.png",
    "00599fa7-6590-44a3-a9c4-a510ad18a22f": "avatar-odds-master.png",
    "5002286a-632d-437a-a267-aa1ed7e84060": "cup-silver.png",
    "2739a8e1-ae42-4d9f-a82e-810b8f941730": "avatar-lucky-slip.png",
    "d460756e-00bf-4830-b38b-810b0111757a": "cup-gold.png",
    "49cc341e-36d0-4831-9312-f27efe9f87d3": "cup-bronze.png",
    "9ee33c0c-2906-49ad-93aa-750217043814": "icon-hot-top-events.png",
    "28790b07-8a7d-4889-81d2-e5d48255458d": "icon-basketball-te.png",
    "9549d813-f173-4cad-bb15-f80c548bbcc5": "icon-insights-te-vec.png",
    "4f1a9d1a-1a28-454f-8b1a-b30bd29dca0e": "icon-hot-te-card-vec.png",
    "05fa9f76-567d-4c80-a55b-267d08acfce7": "icon-fav-te-vec.png",
    "cd2312d4-19c8-4930-b5ae-940d7e87062b": "team-boston-celtics-2.png",
    "26a2919c-2ca2-4cac-9788-0e7ebc166856": "team-milwaukee-bucks-2.png",
    "ccd18159-647b-4f34-a40d-9cc8b017d04e": "icon-arrow-right-te-vec.png",
    "dcc57b09-e308-44ab-a4c1-0851e14aa819": "icon-stream-te-vec.png",
    "c7f99de3-70b5-4b91-b729-0eb13bb425a3": "team-ny-knicks-2.png",
    "f24f2910-f554-4f44-b812-9f3c8f34b79a": "team-cleveland-cavs-2.png",
    "25e28eb1-1490-4e3b-86da-2c846d7c5861": "icon-betbuilder.png",
    "7ac2424d-dbcd-4448-b112-6ecf7c1bc406": "icon-close-vec.png",
    "2d9da508-0a44-4777-8827-bff6c3d23ffa": "team-barcelona.png",
    "bda8ee59-af74-4c95-8625-9f1ae181928b": "team-psg.png",
    "e539d56f-63e7-41a6-9e24-e3e2dd6b5888": "icon-arrow-right-bb-vec.png",
    "5b793cdb-a7b9-47ef-a6c6-c94f0df7f973": "icon-football.png",
    "6b495089-b3f7-451c-bf8d-2e7fb6e95efc": "btn-see-all-football-bg.png",
    "07b9c26b-4830-4a09-9e0e-ae9480a30196": "icon-hot-football-vec.png",
    "677cb11a-5353-4d0c-bc48-57195f082717": "icon-fav-football-vec.png",
    "ba169886-378c-494a-a4de-c506e2bcb912": "team-mexico.png",
    "15f31b98-7fd0-4678-a18a-d35eb632e8bf": "team-south-africa.png",
    "8a3090ea-863c-4200-8515-86b27efdc32a": "icon-arrow-right-football-vec.png",
    "a28ebc7b-4467-4308-82de-5eb86ec2445c": "team-south-korea.png",
    "af97f85a-1a5f-402e-9a04-2f49972b2cc8": "team-czech-republic.png",
    "d2ae54b3-9ea6-4ba1-8347-862078bc871a": "footer-mobile.png",
    "72fd5590-43a6-4452-97b4-00226b2b0ece": "icon-quickbet-vec.png",
    "78e97e9b-7f45-43ac-8c18-8797a60af7b1": "icon-slots-vec.png",
    "787f03ca-b43a-420f-98f7-0664439998c7": "swipe-bet-animation.png",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

print(f"Downloading {len(NAMES)} images...")
ok, fail = 0, 0
for uuid, fname in NAMES.items():
    url = f"https://www.figma.com/api/mcp/asset/{uuid}"
    dest = f"{IMG_DIR}/{fname}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r, open(dest, "wb") as f:
            f.write(r.read())
        ok += 1
        print(f"  ✓ {fname}")
    except Exception as e:
        fail += 1
        print(f"  ✗ {fname} — {e}")

print(f"\nDownloaded: {ok}, Failed: {fail}")

# Replace all URLs in HTML
with open(HTML_IN, "r", encoding="utf-8") as f:
    html = f.read()

replaced = 0
for uuid, fname in NAMES.items():
    old = f"https://www.figma.com/api/mcp/asset/{uuid}"
    new = f"assets/images/{fname}"
    if old in html:
        html = html.replace(old, new)
        replaced += 1

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nReplaced {replaced} URLs → index.html written")
# Verify no Figma URLs remain
remaining = re.findall(r'figma\.com/api', html)
print(f"Remaining Figma URLs: {len(remaining)}")
