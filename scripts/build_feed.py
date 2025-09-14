import os
from pathlib import Path
import datetime
import email.utils
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Read podcast info from environment variables
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My Podcast")
PODCAST_AUTHOR = os.getenv("PODCAST_AUTHOR", "Unknown Author")
PODCAST_DESCRIPTION = os.getenv("PODCAST_DESCRIPTION", "")
PODCAST_OWNER_EMAIL = os.getenv("PODCAST_OWNER_EMAIL", "")
PODCAST_CATEGORY = os.getenv("PODCAST_CATEGORY", "Technology")

# Your GitHub Pages base URL
BASE_URL = "https://mr-shire.github.io/Barbaraawi"

# Where MP3s are stored after yt-dlp
DOWNLOADS_DIR = Path("downloads")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

# Create RSS root
rss = Element("rss", version="2.0", attrib={
    "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"
})
channel = SubElement(rss, "channel")

# Basic channel info
SubElement(channel, "title").text = PODCAST_TITLE
SubElement(channel, "link").text = BASE_URL
SubElement(channel, "description").text = PODCAST_DESCRIPTION
SubElement(channel, "language").text = "en-us"
SubElement(channel, "itunes:author").text = PODCAST_AUTHOR
SubElement(channel, "itunes:summary").text = PODCAST_DESCRIPTION
owner = SubElement(channel, "itunes:owner")
SubElement(owner, "itunes:name").text = PODCAST_AUTHOR
SubElement(owner, "itunes:email").text = PODCAST_OWNER_EMAIL
SubElement(channel, "itunes:category").set("text", PODCAST_CATEGORY)
SubElement(channel, "itunes:explicit").text = "no"

# Loop through MP3 files and add episodes
for mp3_file in sorted(DOWNLOADS_DIR.glob("*.mp3"), reverse=True):
    file_size = mp3_file.stat().st_size
    pub_date = email.utils.format_datetime(datetime.datetime.utcnow())

    item = SubElement(channel, "item")
    SubElement(item, "title").text = mp3_file.stem
    SubElement(item, "description").text = mp3_file.stem
    SubElement(item, "pubDate").text = pub_date
    SubElement(item, "guid").text = mp3_file.stem
    enclosure = SubElement(item, "enclosure")
    enclosure.set("url", f"{BASE_URL}/downloads/{mp3_file.name}")
    enclosure.set("length", str(file_size))
    enclosure.set("type", "audio/mpeg")

# Save feed
output_file = OUTPUT_DIR / "podcast.xml"
ElementTree(rss).write(output_file, encoding="utf-8", xml_declaration=True)
print(f"✅ RSS feed written to {output_file}")

