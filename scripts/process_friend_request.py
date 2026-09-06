#!/usr/bin/env python3
"""
Process friend link request from GitHub Issue.
- Extract JSON from issue body
- Validate fields and link reachability
- Append to friends.json (or update if exists)
- Commit and push changes
- Comment and close issue on success, or comment error on failure
"""

import json
import re
import sys
from pathlib import Path
import requests
from github import Github, GithubException

# Configuration
FRIENDS_FILE = Path("friends.json")
TIMEOUT = 10
HEADERS = {"User-Agent": "FriendLinkProcessor/1.0 (GitHub Action)"}


def extract_json_from_body(body: str):
    """Extract first JSON object (or array) from issue body."""
    # Try to find a code block with json
    json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(json_pattern, body)
    for block in matches:
        try:
            data = json.loads(block.strip())
            return data
        except json.JSONDecodeError:
            continue
    # Fallback: try to parse whole body as JSON
    try:
        return json.loads(body.strip())
    except json.JSONDecodeError:
        return None


def check_url(url: str) -> bool:
    """Return True if URL is reachable (HTTP status < 400)."""
    try:
        with requests.get(
            url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True
        ) as resp:
            return resp.ok
    except requests.RequestException:
        return False


def validate_entry(entry: dict):
    """Validate a single friend entry. Return (is_valid, error_message)."""
    required_fields = ["name", "link", "description", "avatar"]
    for field in required_fields:
        if field not in entry:
            return False, f"缺少字段: {field}"
    name = entry.get("name", "").strip()
    if not name:
        return False, "网站名称不能为空"
    links = entry.get("link")
    if isinstance(links, str):
        links = [links]
    if not isinstance(links, list) or not links:
        return False, "link 必须是字符串数组，且至少包含一个 URL"
    # Check at least one link is reachable
    alive = False
    for url in links:
        if check_url(url):
            alive = True
            break
    if not alive:
        return False, "所有链接均无法访问（HTTP 状态码 >=400 或连接超时）"
    # Optional: check avatar
    avatar = entry.get("avatar", "")
    if avatar and not check_url(avatar):
        # Not fatal, just warn
        print(f"Warning: avatar unreachable: {avatar}")
    # All good
    return True, None


def main():
    repo_full = os.environ.get("REPO_FULL_NAME")
    issue_num = int(os.environ.get("ISSUE_NUMBER", "0"))
    token = os.environ.get("GITHUB_TOKEN")

    if not token or not repo_full or not issue_num:
        print("Missing environment variables")
        sys.exit(1)

    g = Github(token)
    repo = g.get_repo(repo_full)
    issue = repo.get_issue(issue_num)

    # Extract JSON
    entry = extract_json_from_body(issue.body)
    if entry is None:
        issue.create_comment(
            """> [!CAUTION]
> 无法从 Issue 内容中解析 JSON 数据。
> 请确保你提供了正确的 JSON 格式（可使用 ```json 代码块）。"""
        )
        issue.edit(state="closed")
        sys.exit(0)

    # If user provided an array, take the first element (or process multiple? We'll take first for simplicity)
    if isinstance(entry, list):
        if len(entry) == 0:
            issue.create_comment(
                """> [!CAUTION]
> JSON 数组为空，至少需要一个友链对象。"""
            )
            issue.edit(state="closed")
            sys.exit(0)
        entry = entry[0]

    # Validate
    valid, err_msg = validate_entry(entry)
    if not valid:
        issue.create_comment(
            f"""> [!CAUTION]
> 友链验证失败：
>
> {err_msg}
>
> 请修正后重新提交 Issue（关闭当前 Issue 再新建）。"""
        )
        issue.edit(state="closed")
        sys.exit(0)

    # Update friends.json
    # Clone the repository locally (already checked out)
    if not FRIENDS_FILE.exists():
        # Create empty array
        friends = []
    else:
        with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
            friends = json.load(f)
            if not isinstance(friends, list):
                friends = []

    # Check for duplicate (by name or link)
    exists = False
    for existing in friends:
        if existing.get("name") == entry["name"]:
            exists = True
            break
        existing_links = existing.get("link", [])
        if isinstance(existing_links, str):
            existing_links = [existing_links]
        # If any link overlaps
        if any(
            link in existing_links
            for link in (
                entry["link"] if isinstance(entry["link"], list) else [entry["link"]]
            )
        ):
            exists = True
            break
    if exists:
        issue.create_comment(
            """> [!NOTE]
> 该友链（相同名称或链接）已存在于 `friends.json` 中，无需重复添加。"""
        )
        issue.edit(state="closed")
        sys.exit(0)

    # Append new entry
    friends.append(entry)

    # Write back
    with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(friends, f, ensure_ascii=False, indent=2)

    # Commit and push using GitHub API or git commands
    import subprocess

    try:
        subprocess.run(
            ["git", "config", "user.name", "github-actions[bot]"], check=True
        )
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "github-actions[bot]@users.noreply.github.com",
            ],
            check=True,
        )
        subprocess.run(["git", "add", str(FRIENDS_FILE)], check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Add friend link: {entry['name']} (via issue #{issue_num})",
            ],
            check=True,
        )
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        issue.create_comment(
            f"""> [!WARNING]
> 验证通过，但提交到仓库时失败：
>
> {e}
>
> 请手动合并或通知管理员。"""
        )
        issue.edit(state="closed")
        sys.exit(0)

    # Comment success and close issue
    comment = f"""> [!TIP]
> 友链添加成功！
>
> **{entry['name']}** 已加入 `friends.json`。
> 感谢你的支持！"""
    issue.create_comment(comment)
    issue.edit(state="closed")


if __name__ == "__main__":
    import os

    main()