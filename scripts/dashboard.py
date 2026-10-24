#!/usr/bin/env python3
"""Rewrite README dashboard blocks from live GitHub contribution data.

Fills <!-- DASH:START --> ... <!-- DASH:END --> with stats the built-in
contribution graph doesn't show.
Stdlib only. Env: GH_TOKEN (required), GH_USER (default: repo owner), README (default: README.md).
"""
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "Echo-Smith"
README = os.environ.get("README", "README.md")
OUT = os.environ.get("OUT", README)

QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from,to:$to){
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar{ weeks{ contributionDays{ date weekday contributionCount } } }
      commitContributionsByRepository(maxRepositories:100){
        repository{ name url isPrivate }
        contributions{ totalCount }
      }
    }
  }
}"""

WEEKDAYS = "日一二三四五六"


def gql(variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]["contributionsCollection"]


def pad(text, width):
    """Left-justify by display width (CJK / emoji count as 2 columns)."""
    w = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
    return text + " " * max(1, width - w)


def bar(n, top, width=24):
    return "█" * max(1, round(n / top * width)) if n else ""


def main():
    now = dt.datetime.now(dt.timezone.utc)
    start = (now - dt.timedelta(days=89)).replace(hour=0, minute=0, second=0, microsecond=0)
    cc = gql({"login": USER, "from": start.isoformat(), "to": now.isoformat()})

    weeks = cc["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    last7 = sum(counts[-7:])
    prior = counts[:-7]
    prior_avg7 = sum(prior) / max(1, len(prior)) * 7

    active = sum(1 for d in days if d["contributionCount"] > 0)
    best = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        best = max(best, run)
    busiest = max(days, key=lambda d: d["contributionCount"])
    by_wd = [0] * 7
    for d in days:
        by_wd[d["weekday"]] += d["contributionCount"]
    fav_wd = max(range(7), key=lambda i: by_wd[i])

    commits = cc["totalCommitContributions"]
    prs = cc["totalPullRequestContributions"]
    repos = cc["commitContributionsByRepository"]
    public = [r for r in repos if not r["repository"]["isPrivate"]]
    private_commits = sum(r["contributions"]["totalCount"] for r in repos if r["repository"]["isPrivate"])
    public.sort(key=lambda r: -r["contributions"]["totalCount"])
    top = public[:4]
    rest = sum(r["contributions"]["totalCount"] for r in public[4:])

    # rule-based captions
    total = len(days)
    if active == 0:
        active_cap = "键盘在冬眠"
    elif active / total >= 0.7:
        active_cap = "基本住在 GitHub 上了"
    elif active / total >= 0.4:
        active_cap = "一半时间在写，一半时间在想写什么"
    else:
        active_cap = "灵感是间歇泉"
    streak_cap = "第 %d 天在睡觉" % (best + 1) if best else "连更？不存在的"
    week_trend = "最近 7 天在加速 🚀" if last7 >= prior_avg7 else "最近 7 天在蓄力 🔋"
    pr_cap = "平均 %.1f 天一个" % (total / prs) if prs else "PR 还在路上"
    top_share = (top[0]["contributions"]["totalCount"] / commits) if (top and commits) else 0
    top_cap = f"{top[0]['repository']['name']} 吃掉了 {top_share:.0%} 的 commit，偏心得很明显" if top_share >= 0.5 else "雨露均沾"

    stamp = now.strftime("%Y-%m-%d")
    lines = [
        f"<sub>🤖 GitHub Actions 每天自动刷新 · 最近一次：{stamp} UTC · 窗口：近 90 天 · 热力图请看楼下官方版</sub>",
        "",
        f"> 近况：{week_trend}",
        "",
        "| 指标 | 数值 | 点评 |",
        "| --- | --- | --- |",
        f"| commit | **{commits}** | {top_cap} |",
        f"| PR | **{prs}** | {pr_cap} |",
        f"| 有贡献的天数 | **{active} / {total}** | {active_cap} |",
        f"| 最长连更 | **{best} 天** | {streak_cap} |",
        f"| 单日最高 | **{busiest['contributionCount']}**（{busiest['date']}，周{WEEKDAYS[busiest['weekday']]}） | 周{WEEKDAYS[fav_wd]} = 本人战斗日 |",
        "",
        "**commit 去哪了**",
        "",
        "```text",
    ]
    peak_repo = top[0]["contributions"]["totalCount"] if top else 1
    for r in top:
        n = r["contributions"]["totalCount"]
        name = r["repository"]["name"]
        label = "本页（对，就是这页）" if name.lower() == USER.lower() else name
        lines.append(f"{pad(label, 24)}{bar(n, peak_repo):<25} {n}")
    if rest:
        lines.append(f"{pad('其他公开仓库', 24)}{bar(rest, peak_repo):<25} {rest}")
    if private_commits:
        lines.append(f"{pad('🔒 私有（不告诉你是啥）', 24)}{bar(private_commits, peak_repo):<25} {private_commits}")
    lines += ["```", "", "<sub>commit / PR 来自 GitHub contributionsCollection；天数与单日统计全部贡献类型。</sub>"]
    full = "\n".join(lines)

    text = open(README, encoding="utf-8").read()
    pat = re.compile(r"(<!-- DASH:START -->)(.*?)(<!-- DASH:END -->)", re.S)
    text = pat.sub(lambda m: f"{m.group(1)}\n{full}\n{m.group(3)}", text)
    open(OUT, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
