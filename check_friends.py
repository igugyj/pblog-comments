#!/usr/bin/env python3
"""
Friend link health check script.
Reads friends.json, pings each link; if at least one link responds successfully,
the entry is kept; otherwise moved to friends.unlink.json.
"""
import json
import sys
from pathlib import Path
import requests

INPUT_FILE = Path("friends.json")
PASS_FILE = Path("friends.json")          # passed entries
FAIL_FILE = Path("friends.unlink.json")   # fully unreachable entries
TIMEOUT = 10
HEADERS = {"User-Agent": "FriendLinkChecker/1.0 (GitHub Action)"}


def check_url(url: str) -> bool:
    """Return True if URL can be reached (HTTP status < 400), else False."""
    try:
        with requests.get(url, headers=HEADERS, timeout=TIMEOUT,
                          allow_redirects=True, stream=True) as resp:
            return resp.ok
    except requests.RequestException:
        return False


def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: {INPUT_FILE} not found")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        try:
            friends = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON - {e}")
            sys.exit(1)

    if not isinstance(friends, list):
        print("ERROR: friends.json should contain a JSON array")
        sys.exit(1)

    passed, failed = [], []

    for entry in friends:
        name = entry.get("name", "Unknown")
        links = entry.get("link", [])
        if not links:
            print(f"[SKIP] {name}: no links provided")
            failed.append(entry)
            continue

        print(f"[CHECK] {name} ({len(links)} link(s))")
        alive = False
        for url in links:
            if check_url(url):
                print(f"  [OK]    {url}")
                alive = True
                break
            else:
                print(f"  [FAIL]  {url}")

        if alive:
            passed.append(entry)
        else:
            print(f"  --> All links dead, moving to unlink list")
            failed.append(entry)

    with open(PASS_FILE, "w", encoding="utf-8") as f:
        json.dump(passed, f, ensure_ascii=False, indent=2)
    print(f"\nPassed: {len(passed)} friends saved to {PASS_FILE}")

    with open(FAIL_FILE, "w", encoding="utf-8") as f:
        json.dump(failed, f, ensure_ascii=False, indent=2)
    print(f"Failed: {len(failed)} friends saved to {FAIL_FILE}")


if __name__ == "__main__":
    main()