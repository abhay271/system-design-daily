#!/usr/bin/env python3
"""Validate index.html before committing a new system design entry.

Checks: balanced/well-formed HTML, every diagram <svg> parses as XML and has title+desc,
unique ids (and every id inside an entry is prefixed with that entry's id), required
article attributes, the required sections in the fixed order, a Legend with 4-10 terms,
1-3 diagrams per entry, TOC <-> article consistency, no external scripts/images, and that
no existing line of index.html was modified or removed (git diff vs HEAD).
Exit code 0 = OK, 1 = problems found.

`--allow-edits` skips only the "no existing line changed" check. It is for a human
deliberately changing the shared shell (CSS/JS); scheduled runs must never use it.
"""
import html as htmllib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "index.html"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# required section ids (suffixes after "<entry-id>-"), in this exact order; entities is optional
SECTIONS = ["sec-functional", "sec-nonfunctional", "sec-entities", "sec-api", "sec-hld", "sec-deepdives", "sec-tips"]
OPTIONAL = {"sec-entities"}
# entries after the longer launch entry follow the tighter budget in CLAUDE.md
BUDGET_FROM, MAX_WORDS, MAX_DIVES = "2026-10-28", 1000, 3
errors = []


def err(msg):
    errors.append(msg)


html = PATH.read_text(encoding="utf-8")


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            err(f"unexpected </{tag}> at line {self.getpos()[0]}")
            return
        top, pos = self.stack[-1]
        if top != tag:
            err(f"</{tag}> at line {self.getpos()[0]} does not match <{top}> opened at line {pos[0]}")
            # try to recover
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()


p = P()
p.feed(html)
for tag, pos in p.stack:
    err(f"<{tag}> opened at line {pos[0]} never closed")

# duplicate ids
seen = set()
for i in p.ids:
    if i in seen:
        err(f"duplicate id: {i}")
    seen.add(i)

# svgs
svgs = [s for s in re.findall(r"<svg\b.*?</svg>", html, flags=re.S) if re.search(r'class="diagram[ "]', s[:200])]
if not svgs:
    err("no diagram SVG found")
for n, s in enumerate(svgs, 1):
    try:
        root = ET.fromstring(s.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1) if "xmlns" not in s[:200] else s)
    except ET.ParseError as e:
        err(f"svg #{n} is not well-formed XML: {e}")
        continue
    ns = "{http://www.w3.org/2000/svg}"
    if root.find(f"{ns}title") is None or root.find(f"{ns}desc") is None:
        err(f"svg #{n} missing <title> or <desc>")
    if root.get("role") != "img" or not root.get("aria-labelledby"):
        err(f"svg #{n} needs role=\"img\" and aria-labelledby")
    if not root.get("viewBox"):
        err(f"svg #{n} missing viewBox")
    for el in root.iter():
        cls = el.get("class") or ""
        if el.tag.endswith("path") and "d-edge" in cls and not el.get("d"):
            err(f"svg #{n} edge without d")
        if ("d-node" in cls.split() or "d-note" in cls.split()) and el.find(f"{ns}rect") is None:
            err(f"svg #{n} has a .d-node/.d-note without a <rect> (they are drawn from their rect)")

# articles
arts = re.findall(r"<article class=\"entry\"([^>]*)>", html)
toc = re.findall(r'<li><a href="#([^"]+)">', html)
art_ids = []
for a in arts:
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
    for k in ("id", "data-topic", "data-domain", "data-date"):
        if not attrs.get(k):
            err(f"article missing {k}: {a[:80]}")
    art_ids.append(attrs.get("id"))
    if attrs.get("id") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", attrs["id"]):
        err(f"bad article id format: {attrs['id']}")
    if attrs.get("id") and attrs.get("data-date") and not attrs["id"].startswith(attrs["data-date"]):
        err(f"article id {attrs['id']} does not start with its data-date {attrs['data-date']}")

# per-entry structure
for m in re.finditer(r'<article class="entry" id="([^"]+)".*?</article>', html, flags=re.S):
    aid, body = m.group(1), m.group(0)
    for i in re.findall(r'\sid="([^"]+)"', body):
        if i != aid and not i.startswith(aid + "-"):
            err(f"entry {aid}: id '{i}' must be prefixed with '{aid}-'")
    found = [s for s in re.findall(r'<section class="sec[^"]*" id="' + re.escape(aid) + r'-(sec-[a-z]+)"', body)]
    for s in found:
        if s not in SECTIONS:
            err(f"entry {aid}: unknown section id '{aid}-{s}'")
    for s in SECTIONS:
        if s not in OPTIONAL and s not in found:
            err(f"entry {aid}: missing required section <section class=\"sec\" id=\"{aid}-{s}\">")
    order = [s for s in found if s in SECTIONS]
    if order != sorted(order, key=SECTIONS.index) or len(order) != len(set(order)):
        err(f"entry {aid}: sections out of order or repeated: {order} (expected order {SECTIONS})")
    leg = re.search(r'<details class="legend".*?</details>', body, flags=re.S)
    if not leg:
        err(f"entry {aid}: missing Legend (<details class=\"legend\">)")
    else:
        if leg.start() > body.find(f'id="{aid}-sec-functional"'):
            err(f"entry {aid}: Legend must come before the first section")
        n_terms = len(re.findall(r"<dt>", leg.group(0)))
        if not 4 <= n_terms <= 10:
            err(f"entry {aid}: Legend has {n_terms} terms (need 4-10)")
        if len(re.findall(r'<dfn class="term" title="[^"]+">', body)) < min(n_terms, 4):
            err(f"entry {aid}: wrap each legend term's first use in <dfn class=\"term\" title=\"...\">")
    n_svg = len(re.findall(r'<svg class="diagram[ "]', body))
    if not 2 <= n_svg <= 3:
        err(f"entry {aid}: has {n_svg} diagrams (need 2-3, including the final design)")
    final = body.find(f'<figure class="diagram-fig" id="{aid}-final">')
    if not body.find(f'id="{aid}-sec-deepdives"') < final < body.find(f'id="{aid}-sec-tips"'):
        err(f"entry {aid}: needs the Final design diagram <figure class=\"diagram-fig\" id=\"{aid}-final\"> after the deep dives (inside sec-deepdives)")
    if aid[:10] >= BUDGET_FROM:
        # same count as the page's read time: lede + prose, minus diagrams, code, tables and Legend
        text = re.sub(r"<(svg|pre|table|details)\b.*?</\1>", " ", body, flags=re.S)
        lede = re.search(r'<p class="lede">.*?</p>', text, flags=re.S)
        prose = text[text.find('<div class="prose">'):]
        words = len(htmllib.unescape(re.sub(r"<[^>]+>", " ", (lede.group(0) if lede else "") + prose)).split())
        if words > MAX_WORDS:
            err(f"entry {aid}: {words} words of prose (max {MAX_WORDS}); do the cut pass in CLAUDE.md")
        n_dives = len(re.findall(r'<div class="dive\b', body))
        if n_dives > MAX_DIVES:
            err(f"entry {aid}: {n_dives} deep dives (max {MAX_DIVES})")

if art_ids != sorted(art_ids, key=lambda x: x[:10], reverse=True):
    err("articles are not newest-first")
if len(toc) != len(set(toc)):
    err("duplicate TOC entries")
if toc != art_ids:
    err(f"TOC must list the same entries in the same order as the articles: toc={toc} articles={art_ids}")
if html.count("<!-- ENTRIES -->") != 1 or html.count("<!-- TOC -->") != 1:
    err("markers <!-- ENTRIES --> and <!-- TOC --> must each appear exactly once")
for url in re.findall(r'<script[^>]+src="([^"]*)"', html):
    err(f"external script not allowed: {url}")
if re.search(r"mermaid", html, re.I):
    err("mermaid is not allowed; diagrams are hand-written inline SVG")
for url in re.findall(r'<link[^>]+href="(https?://[^"]+)"', html):
    if not url.startswith(("https://fonts.googleapis.com", "https://fonts.gstatic.com")):
        err(f"external stylesheet/resource not allowed (Google Fonts only): {url}")
if re.search(r"<img\b|<iframe\b", html):
    err("image files / iframes are not allowed; use inline SVG")

# older content unchanged
if "--allow-edits" not in sys.argv:
    try:
        out = subprocess.run(["git", "diff", "HEAD", "--unified=0", "--", "index.html"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        removed = [l for l in out.splitlines() if l.startswith("-") and not l.startswith("---")]
        if removed:
            err(f"{len(removed)} existing line(s) modified/removed (only additions allowed). First: {removed[0][:100]}")
    except Exception as e:  # not a repo yet, no HEAD, etc.
        print(f"note: git diff check skipped ({e})")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(arts)} article(s), {len(svgs)} svg(s), {len(p.ids)} ids, all checks passed")
