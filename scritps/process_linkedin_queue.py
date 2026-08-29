"""
Reads newly pasted LinkedIn post URLs from _data/linkedin_posts_queue.txt,
extracts each post's LinkedIn URN, and appends new entries to
_data/linkedin_posts.yml (used by the /news/ page). The queue file is
then cleared back to just its header comment.

No LinkedIn login, session cookie, or API access is used here -- this
only parses the public post URL you paste in; it never fetches anything
from LinkedIn. Run from the repo root, e.g. via
.github/workflows/process_linkedin_queue.yml whenever
_data/linkedin_posts_queue.txt changes.
"""
import re
from datetime import date

import yaml

QUEUE_FILE = "_data/linkedin_posts_queue.txt"
DATA_FILE = "_data/linkedin_posts.yml"

QUEUE_HEADER = """# Paste LinkedIn post URLs here, one per line, whenever you want a new
# post added to https://baptistevandecrux.github.io/news/
#
# Example:
# https://www.linkedin.com/posts/baptiste-vandecrux_some-post-activity-7123456789012345678-abCd
#
# A GitHub Action picks these up automatically, converts them into the
# format the News page needs, appends them to linkedin_posts.yml, and
# clears this file. Nothing else needs to change by hand.
"""

DATA_HEADER = """# List of LinkedIn posts/reposts featured on /news/.
#
# Entries are added automatically two ways:
#   - a daily scheduled scrape (scritps/fetch_linkedin_posts.py, see
#     .github/workflows/fetch_linkedin_posts.yml)
#   - pasting a URL into _data/linkedin_posts_queue.txt as a manual
#     fallback (scritps/process_linkedin_queue.py, see
#     .github/workflows/process_linkedin_queue.yml)
#
# Don't edit this file by hand unless fixing a bad entry -- routine
# changes will just get merged with the next automated run.
"""

# Matches a URN pasted directly (e.g. copied out of an embed code).
URN_RE = re.compile(r"urn:li:(?:activity|share|ugcPost):\d+")
# Matches the numeric id in a normal LinkedIn post URL:
# .../posts/someone_some-slug-activity-7123456789012345678-abCd
ACTIVITY_ID_RE = re.compile(r"activity[-:](\d{6,})")


def extract_urn(line):
    """Return a LinkedIn URN string parsed from a pasted line, or None."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    match = URN_RE.search(line)
    if match:
        return match.group(0)

    match = ACTIVITY_ID_RE.search(line)
    if match:
        return f"urn:li:activity:{match.group(1)}"

    return None


def urn_id(urn):
    """
    The numeric id in a LinkedIn activity URN encodes a timestamp (like a
    Twitter/Discord snowflake id), so a bigger number means a more recent
    post. Stored alongside the urn so the News page can sort by it
    directly instead of relying on whatever date a post happened to be
    added to this file (which, for anything backfilled, is not the same
    as when it was actually posted).
    """
    match = re.search(r"(\d+)$", urn)
    return int(match.group(1)) if match else 0


def load_existing_posts():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        data = None
    return data or []


def main():
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue_lines = f.readlines()
    except FileNotFoundError:
        print(f"No queue file found at {QUEUE_FILE}, nothing to do.")
        return

    posts = load_existing_posts()
    known_urns = {p["urn"] for p in posts if isinstance(p, dict) and "urn" in p}

    today = date.today().isoformat()
    added = []
    skipped = []

    for line in queue_lines:
        urn = extract_urn(line)
        if urn is None:
            continue
        if urn in known_urns:
            skipped.append(urn)
            continue
        posts.append({"urn": urn, "id": urn_id(urn), "date": today})
        known_urns.add(urn)
        added.append(urn)

    if not added:
        print("No new post URLs found in the queue.")
        if skipped:
            print(f"({len(skipped)} already-known URL(s) ignored.)")
        return

    # Backfill `id` on any older entries that predate this field, and keep
    # the file itself sorted newest-first for readability.
    for post in posts:
        if isinstance(post, dict) and "id" not in post and "urn" in post:
            post["id"] = urn_id(post["urn"])
    posts.sort(key=lambda p: p.get("id", 0), reverse=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(DATA_HEADER)
        yaml.safe_dump(posts, f, sort_keys=False, allow_unicode=True)

    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        f.write(QUEUE_HEADER)

    print(f"Added {len(added)} new post(s): {', '.join(added)}")
    if skipped:
        print(f"Ignored {len(skipped)} already-known URL(s).")


if __name__ == "__main__":
    main()
