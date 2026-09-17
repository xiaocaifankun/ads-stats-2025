#!/usr/bin/env python3
"""
llm-wiki 本地辅助工具：不需要 LLM 即可运行的结构化检查。

用法：
    python scripts/llm-wiki lint [wiki_dir]        # 健康检查：死链 / 孤儿页 / 缺 frontmatter
    python scripts/llm-wiki index [wiki_dir]       # 重建 wiki/index.md 目录
    python scripts/llm-wiki stats [wiki_dir]       # 统计页面数量

默认 wiki_dir 为 ./wiki
"""

import os
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SKIP = {"index.md", "log.md"}
# 文档示例中的占位链接，不视为死链
PLACEHOLDERS = {"category/page-name", "title", "date", "filename"}


def collect_pages(wiki: Path) -> dict:
    """返回 {相对路径(无扩展名): 绝对路径}"""
    pages = {}
    for md in wiki.rglob("*.md"):
        rel = md.relative_to(wiki).with_suffix("").as_posix()
        pages[rel] = md
    return pages


def parse_links(text: str) -> list:
    return [m.strip() for m in LINK_RE.findall(text)]


def has_frontmatter(text: str) -> bool:
    return bool(FM_RE.match(text))


def lint(wiki: Path) -> int:
    pages = collect_pages(wiki)
    all_text = {k: v.read_text(encoding="utf-8") for k, v in pages.items()}

    # 收集所有出链与入链
    out_links = {}   # page -> set(link)
    in_links = {k: set() for k in pages}
    dead = []        # (page, link)
    no_fm = []

    for page, text in all_text.items():
        if page not in SKIP and page not in ("log",) and not has_frontmatter(text):
            no_fm.append(page)
        links = set()
        for link in parse_links(text):
            # 归一化：去掉锚点、允许省略目录前缀
            target = link.split("#")[0].strip().strip("/")
            links.add(target)
            if target in PLACEHOLDERS or "{{" in target:
                continue
            if target and target not in pages and not target.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf")):
                # 允许指向 raw/ 或 assets 的非 wiki 路径
                if not target.startswith(("raw/", "assets/")):
                    dead.append((page, target))
        out_links[page] = links

    for page, links in out_links.items():
        for link in links:
            if link in in_links:
                in_links[link].add(page)

    # index/log 等导航文件天然无入链，不算孤儿
    NAV = {"overview", "conventions", "index", "log"}
    orphans = [p for p in pages if p not in SKIP and not in_links[p] and p not in NAV]

    print(f"\n{'='*52}\n  LLM Wiki Lint Report\n{'='*52}")
    print(f"页面总数: {len(pages)}")

    print(f"\n[1] 死链 (目标页面不存在): {len(dead)}")
    for page, link in dead:
        print(f"    {page}.md  ->  [[{link}]]")
    if not dead:
        print("    (无)")

    print(f"\n[2] 孤儿页 (无入链): {len(orphans)}")
    for p in orphans:
        print(f"    {p}.md")
    if not orphans:
        print("    (无)")

    print(f"\n[3] 缺 frontmatter: {len(no_fm)}")
    for p in no_fm:
        print(f"    {p}.md")
    if not no_fm:
        print("    (无)")

    issues = len(dead) + len(orphans) + len(no_fm)
    print(f"\n{'='*52}")
    print(f"  合计问题: {issues}")
    print(f"{'='*52}\n")
    return issues


def stats(wiki: Path) -> None:
    pages = collect_pages(wiki)
    by_type = {}
    for page, path in pages.items():
        if page in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        t = "unknown"
        if m:
            tm = re.search(r"^type:\s*(\S+)", m.group(1), re.MULTILINE)
            if tm:
                t = tm.group(1)
        by_type[t] = by_type.get(t, 0) + 1
    print(f"\n页面总数: {len(pages)}")
    for t, n in sorted(by_type.items()):
        print(f"  {t:14s} {n}")
    print()


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "lint"
    wiki = Path(args[1]) if len(args) > 1 else Path("wiki")

    if not wiki.exists():
        print(f"错误: 找不到 wiki 目录: {wiki}")
        sys.exit(1)

    if cmd == "lint":
        sys.exit(1 if lint(wiki) else 0)
    elif cmd == "stats":
        stats(wiki)
    elif cmd == "index":
        print("index 重建需要 LLM 生成摘要，请让 agent 执行：'刷新 index.md'")
    else:
        print(f"未知命令: {cmd}\n可用: lint | stats | index")


if __name__ == "__main__":
    main()
