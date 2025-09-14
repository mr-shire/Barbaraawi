import os
from pathlib import Path
import datetime
import email.utils
from xml.etree.ElementTree import Element, SubElement, ElementTree

PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My Podcast")
PODCAST_AUTHOR = os.getenv("PODCAST_AUTHOR", "Unknown Author")
PODCAST_DESCRIPTION = os.getenv("PODCAST_DESCRIPTION", "")
PODCAST_OWNER_EMAIL = os.getenv("PODCAST_OWNER_EMAIL", "")
PODCAST_CATEGORY = os.getenv("PODCAST_CATEGORY", "Society & Culture")
IA_BUCKET_IDENTIFIER = os.getenv("IA_BUCKET_IDENTIFIER", "")

DOWNLOADS_DIR = Path("downloads")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rss = Element("rss", version="2.0", attrib={
    "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"
})
channel = SubElement(rss, "channel")

# Core channel tags
SubElement(channel, "title").text = PODCAST_TITLE
SubElement(channel, "link").text = f"https://archive.org/details/{IA_BUCKET_IDENTIFIER}"
SubElement(channel, "language").text = "en-us"
SubElement(channel, "itunes:author").text = PODCAST_AUTHOR
SubElement(channel, "itunes:summary").text = PODCAST_DESCRIPTION
SubElement(channel, "description").text = PODCAST_DESCRIPTION
SubElement(channel, "itunes:explicit").text = "no"

# Owner
owner = SubElement(channel, "itunes:owner")
SubElement(owner, "itunes:name").text = PODCAST_AUTHOR
SubElement(owner, "itunes:email").text = PODCAST_OWNER_EMAIL

# Category
cat = SubElement(channel, "itunes:category")
cat.set("text", PODCAST_CATEGORY)

# Optional: lastBuildDate
SubElement(channel, "lastBuildDate").text = email.utils.format_datetime(datetime.datetime.utcnow())

# Episodes from local downloads dir (already uploaded to IA by the time we build)
items = sorted(DOWNLOADS_DIR.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)

for mp3 in items:
    size = mp3.stat().st_size
    pub_date = email.utils.format_datetime(datetime.datetime.utcfromtimestamp(mp3.stat().st_mtime))

    item = SubElement(channel, "item")
    SubElement(item, "title").text = mp3.stem
    SubElement(item, "description").text = mp3.stem
    SubElement(item, "pubDate").text = pub_date

    url = f"https://archive.org/download/{IA_BUCKET_IDENTIFIER}/{mp3.name}"
    SubElement(item, "guid").text = url
    enc = SubElement(item, "enclosure")
    enc.set("url", url)
    enc.set("length", str(size))
    enc.set("type", "audio/mpeg")

# Write feed
out_path = OUTPUT_DIR / "podcast.xml"
ElementTree(rss).write(out_path, encoding="utf-8", xml_declaration=True)
print(f"RSS written: {out_path}")
