"""
Fetches recent posts/reposts from a LinkedIn profile using the unofficial
`linkedin-api` package (https://github.com/tomquirk/linkedin-api) and
merges any new ones into _data/linkedin_posts.yml, used by the /news/
page. Meant to run on a schedule via
.github/workflows/fetch_linkedin_posts.yml.

IMPORTANT -- read before using:
  * This is NOT an official LinkedIn API. It authenticates as your own
    account using a copied browser session cookie, which is against
    LinkedIn's Terms of Service for automated access and can get an
    account flagged or restricted. Only run this against your own
    account, knowing that risk.
  * `linkedin-api`'s exact response shape has changed across versions
    and can change again without notice, since it's reverse-engineered
    from LinkedIn's private "Voyager" API. The URN-extraction logic
    below covers the response shapes seen in recent versions, but if
    LinkedIn changes something, this script needs a matching update --
    it has not been run against a live account here to confirm the
    exact JSON shape at the time you use it.
  * The queue-based path (_data/linkedin_posts_queue.txt +
    process_linkedin_queue.py) keeps working independently of this
    script, so pasting a URL by hand is always a safe fallback if this
    breaks.

Setup (do this yourself -- nothing here should ever hold your password):
  1. Log into linkedin.com in a normal browser.
  2. Open dev tools > Application/Storage > Cookies > https://www.linkedin.com.
  3. Copy the value of the `li_at` cookie (and `JSESSIONID`, whose value
     is wrapped in double quotes -- keep those quotes).
  4. In the GitHub repo settings, add two Actions secrets:
       LINKEDIN_LI_AT        = the li_at value
       LINKEDIN_JSESSIONID   = the JSESSIONID value (with its quotes)
  5. These cookies expire (li_at typically lasts about a year, but can
     be invalidated sooner e.g. by a password change) -- when the
     workflow starts failing to authenticate, repeat steps 1-4.
"""
import os
import re
from datetime import date

import yaml
from linkedin_api import Linkedin

PUBLIC_ID = "baptiste-vandecrux-962bba40"
DATA_FILE = "_data/linkedin_posts.yml"
POST_COUNT = 30

DATA_HEADER = """# List of LinkedIn posts/reposts featured on /news/.
#
# Entries are added automatically either by fetch_linkedin_posts.py
# (scheduled scrape) or by pasting a URL into
# _data/linkedin_posts_queue.txt. Don't edit this file by hand unless
# you're fixing a bad entry -- your changes will otherwise just be
# merged with whatever the next automated run finds.
"""

ACTIVITY_ID_RE = re.compile(r"urn:li:(?:activity|share|ugcPost):(\d+)")


def build_linkedin_client():
    li_at = os.environ["LINKEDIN_LI_AT"]
    jsessionid = os.environ["LINKEDIN_JSESSIONID"]
    return Linkedin(
        username="",
        password="",
        cookies={"li_at": li_at, "JSESSIONID": jsessionid},
    )


def extract_urn(post):
    """
    Best-effort extraction of a post's activity URN from whatever shape
    `get_profile_posts` hands back. LinkedIn's internal API nests this
    differently across versions, so check a few known locations.
    """
    candidates = [
        post.get("urn"),
        post.get("updateMetadata", {}).get("urn"),
        post.get("entityUrn"),
        post.get("value", {}).get("com.linkedin.voyager.feed.render.UpdateV2", {}).get("urn"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        match = ACTIVITY_ID_RE.search(str(candidate))
        if match:
            return f"urn:li:activity:{match.group(1)}"
    return None


def load_existing_posts():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        data = None
    return data or []


def main():
    api = build_linkedin_client()

    try:
        raw_posts = api.get_profile_posts(public_id=PUBLIC_ID, post_count=POST_COUNT)
    except Exception as exc:  # noqa: BLE001 -- surfacing the real cause matters more here
        raise SystemExit(
            "Fetching posts failed -- this is most likely an expired session "
            "cookie (refresh LINKEDIN_LI_AT / LINKEDIN_JSESSIONID in the "
            "repo's Actions secrets, see the setup instructions at the top "
            f"of this file) or a change in linkedin-api's response shape. "
            f"Original error: {exc!r}"
        ) from exc

    posts = load_existing_posts()
    known_urns = {p["urn"] for p in posts if isinstance(p, dict) and "urn" in p}

    today = date.today().isoformat()
    added = []

    for raw_post in raw_posts:
        urn = extract_urn(raw_post)
        if urn is None or urn in known_urns:
            continue
        posts.append({"urn": urn, "date": today})
        known_urns.add(urn)
        added.append(urn)

    if not added:
        print("No new posts found.")
        return

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(DATA_HEADER)
        yaml.safe_dump(posts, f, sort_keys=False, allow_unicode=True)

    print(f"Added {len(added)} new post(s): {', '.join(added)}")


if __name__ == "__main__":
    main()
