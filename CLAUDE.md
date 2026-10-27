# System Design Daily: standing instructions

This repo is one self-contained `index.html` (served by GitHub Pages from `main`). Each scheduled run adds ONE new system design walkthrough at the top. Everything you need is in this file.

## Content spec

### Topic
- Each run, pick ONE frequently asked, **junior-level** system design interview question. Examples: URL shortener, pastebin, rate limiter, unique ID generator, key-value store, notification system, chat app, news feed, leaderboard, search autocomplete, web crawler, nearby places (Yelp-style), photo sharing (Instagram-style), Dropbox-style file sync, YouTube/Spotify-style streaming, Uber-style ride hailing, ticket booking, ad click counter, job scheduler.
- `data-domain` is the design **pattern**. Use exactly one of these names: `Read-heavy lookup`, `Write-heavy logging`, `Real-time messaging`, `Feeds`, `Media & files`, `Geo & location`, `Search`, `Queues & async jobs`, `Counters & limits`.
- Before choosing, read every existing entry's topic and pattern: `grep -o 'data-topic="[^"]*" data-domain="[^"]*" data-date="[^"]*" data-level="[^"]*"' index.html`. **Never repeat a topic.** Pick a pattern different from the **last two** entries.
- **Ramp up slowly** with `data-level` (shown as "Lv 1-3"): roughly the first 6 entries are Lv 1 (one or two moving parts: URL shortener, pastebin, rate limiter, unique ID generator, leaderboard); then mix Lv 1-2 (notification system, chat app, news feed, autocomplete, web crawler, nearby places, photo sharing); Lv 3 only after about 12 entries (file sync, video streaming, ride hailing, ticket booking). Even Lv 3 must stay at new-grad interview level: never staff-level depth.

### Audience and tone
- Reader: an undergrad who hasn't graduated, wants the **basics and breadth**, and rarely gets deep system design rounds. Assume they have NOT heard of load balancers, caches, sharding, queues, CDNs, replicas or consistent hashing.
- Simple but not shallow; technical but not overwhelming. Short sentences, everyday words, one idea per paragraph. Concrete example first, then the real term. If a plain word works, use it.
- The design must be correct and defensible in an interview, but it is the **simple version a junior is expected to give**: a few components, each with a clear reason. Scaling ideas go in the "What you could add next" box, not in the main design.
- Assume the generic scaling answer (identical app servers that keep no data, behind a load balancer, e.g. on EC2). Mention it in one sentence in the high-level design and don't re-argue it.
- **Legend:** every entry has a collapsible Legend at the top explaining each new or non-obvious term in 1-2 plain sentences, 4-10 terms, ordered by first use. Wrap each term's **first use** in the text with `<dfn class="term" title="short definition">`.
- **Analogies must earn their place:** use one only if it maps closely to how the system really works. If it half-fits or needs "but unlike..." caveats, drop it. Zero is fine; at most one or two per entry; never one per section.
- **Length:** 700-1000 words of prose (lede + prose, not counting Legend, code, tables, diagrams), about 3-4 minutes. The validator rejects new entries over 1,000 words. See "Same coverage, less content" below.

### Required structure (same order, same headings, every entry)
Modelled on Hello Interview's delivery framework ("System Design in a Hurry"), simplified for juniors.

1. **Functional requirements** (`sec-functional`): only the 2-4 core features that make this product what it is, one line each (e.g. "Submit a long URL and get a short one"). Optionally one line "Out of scope: ...".
2. **Non-functional requirements** (`sec-nonfunctional`): 2-4 qualities that matter for THIS problem, each with one sentence on why it matters here.
3. **Core entities** (`sec-entities`, optional, only if helpful): 2-4 main things stored, one line each.
4. **API design** (`sec-api`): 2-4 endpoints (method, path, request, response), one per functional requirement.
5. **High-level design** (`sec-hld`): built up step by step, one functional requirement at a time, simplest version first. Include the simple data model (a `.schema` table), the architecture diagram and a request-flow diagram.
6. **Deep dives** (`sec-deepdives`): very basic, 2 of them (3 only at Lv 3), one per non-functional requirement that actually shapes the design (or a genuinely tricky part), each titled as a question ("How do we keep redirects fast?"). Show 2-3 realistic options as `.options`, mark the chosen one `.pick`, and say why. After the dives comes the **Final design**: a short `<h4>Final design</h4>` with one sentence, then the final diagram (`<figure class="diagram-fig" id="ID-final">`) showing the complete system with everything the deep dives added. End the section with the "What you could add next" box (2-3 scaling ideas, one line each).
7. **Interview tips** (`sec-tips`): 3 likely follow-ups with one-line answers (`.qa`), 1-2 common junior mistakes (`.mistakes`), and one short `callout tip`.

- **No upfront back-of-the-envelope section.** Do math only INLINE where it changes a design decision ("100M new URLs a month is about 40 writes a second, which one database handles easily, so no sharding yet"). Round numbers, explain each, double-check the arithmetic, and skip math that doesn't affect a decision.
- **Diagrams:** 2-3 animated diagrams per entry: (1) the simple architecture in the high-level design, (2) a request-flow diagram only when the order of steps matters, and (3) the required **Final design** after the deep dives. Every diagram follows "Diagram quality" below.
- Use the `callout why` for the key trade-off, and a `callout confidence` where a detail depends on assumptions or where several answers are valid.

### Same coverage, less content
The goal is the URL shortener entry's quality and coverage with roughly a quarter less text. That launch entry (2026-10-27) is longer than the current budget: copy its markup and its way of breaking the problem down, not its length. Cut words, never steps.
- **Coverage stays complete:** every functional requirement gets an endpoint and a step in the high-level design; every non-functional requirement that shapes the design is answered by a deep dive or one clear sentence in the design; the key trade-off gets the `callout why`. Nothing in the 7 steps is skipped (only Core entities is optional).
- **Budget per section** (prose words, roughly): functional 40, non-functional 80, entities 40 (or skip and let the data-model table cover it), API 40 plus the code blocks, high-level design 220 (2-3 sentences per step, one table, one inline math line if it changes a decision), deep dives 280 total, tips 120, confidence note 40 (only if needed).
- **Deep dive shape:** one sentence on the problem, the options as one line each (what it is, its main pro or con), the pick with a one- or two-sentence why. No extra paragraphs, no second "downside" paragraph unless the interview really needs it.
- **Say each thing once.** If the API section explains a status code, the design doesn't repeat it; if a callout makes the point, the prose doesn't.
- **Legend:** 4-8 terms. Fewer new terms is a feature: if a term isn't needed to follow the design, leave it out instead of defining it.
- **Diagrams:** the simple architecture plus the Final design; add the request-flow diagram only when the order of steps really matters. Diagram text does not count toward the word cap, so make diagrams complete rather than adding prose.
- **Cut pass:** after drafting, re-read and delete every sentence that doesn't help the reader answer this interview question, then check the coverage list above again.

### Accuracy
- These are **design opinions, not facts about one company's internals.** Say "a common approach". Never claim how a real company does it unless verified from a primary source.
- Prefer reputable sources: Hello Interview (problem breakdowns and the delivery framework), Alex Xu's *System Design Interview*, ByteByteGo, *Designing Data-Intensive Applications*, official docs (MDN, Redis, etc.). Verify with web search/fetch when unsure. Say when several answers are valid. Never invent numbers; label assumed traffic numbers as assumptions.
- **Hello Interview is the methodology, not the script.** Use their breakdown of the problem (if one exists) to check what an interviewer expects you to cover, and cross-check with at least one other source. Then write it your own way: your own explanation, everyday examples, assumed numbers and diagrams, at a junior's level and length. Don't copy their text, their option ratings ("Bad / Good / Great") or their example numbers. Reuse a specific framing only when it is clearly the best way to say it, and cite it.
- End with a `<p class="sources">` line linking what you relied on.

## Append rules

- **Date:** use today's date in India time: `TZ=Asia/Kolkata date +%F` (the routine runs at 06:37 IST). If an entry with that date already exists, stop without changes.
- Insert the new entry as one self-contained
  `<article class="entry" id="YYYY-MM-DD-slug" data-topic="..." data-domain="<pattern>" data-date="YYYY-MM-DD" data-level="1|2|3">`
  directly below the `<!-- ENTRIES -->` marker (newest first). **Never modify or reorder older entries.**
- Add it to the archive directly below the `<!-- TOC -->` marker:
  `<li><a href="#ID"><time datetime="YYYY-MM-DD">YYYY-MM-DD</time><span>Short title</span></a></li>`
- All CSS and JS live once in `index.html`; entries add **markup only**, reusing existing classes. If a needed component truly doesn't exist, ADD new CSS lines without changing any existing line (the validator rejects changed lines).
- Diagrams are hand-written inline SVG using the shared classes. No Mermaid, no images, no iframes, no external JS or CDN. Google Fonts are already set up.
- **Use the newest entry as your template**: copy its markup structure exactly and change the content.
- Every `id` inside an entry starts with the entry id: sections are `ID-sec-functional`, `ID-sec-nonfunctional`, `ID-sec-entities`, `ID-sec-api`, `ID-sec-hld`, `ID-sec-deepdives`, `ID-sec-tips`; SVG titles are `ID-d1-t` / `ID-d1-d`, etc. The `.steps` nav at the top links to those section ids (drop the Entities link if you skip that section).
- **Validate before committing:** `python scripts/validate.py`. It checks well-formed HTML, SVGs (parse, title/desc, viewBox), unique and prefixed ids, the required sections in order, Legend term count, 2-3 diagrams including the Final design after the deep dives, TOC/article order, no external resources, and (via `git diff`) that no existing line changed. Fix everything it reports. Never use `--allow-edits` in a scheduled run.
- **Commit message:** `Add design: <topic> (<pattern>)`, then a blank line, then these two trailer lines at the very end, exactly (keep any other trailers your environment adds):
  `Co-Authored-By: abhay271 <153154236+abhay271@users.noreply.github.com>`
  `Co-Authored-By: Claude <noreply@anthropic.com>`
- Push directly to `main`: `git push origin HEAD:main`. Do not open a PR. The trailers are only metadata; never let them block or delay the commit and push.

## Component reference (entry markup)

```html
<article class="entry" id="2026-10-27-url-shortener" data-topic="URL shortener" data-domain="Read-heavy lookup" data-date="2026-10-27" data-level="1">
  <header class="entry-head">
    <div class="entry-meta">
      <span class="chip">Read-heavy lookup</span>
      <span class="level" title="Difficulty: level 1 of 3">Lv 1</span>
      <time datetime="2026-10-27">27 Oct 2026</time>
      <span class="read"><span class="read-time">5</span> min read</span>
    </div>
    <h2 class="entry-title">Design a URL shortener</h2>
    <p class="lede">What the product does, in one everyday example, and why it is a good interview question.</p>
    <nav class="steps" aria-label="Sections of this design"><a href="#ID-sec-functional">Features</a> … <a href="#ID-sec-tips">Tips</a></nav>
  </header>
  <div class="prose">
    <details class="legend"><summary>Legend <span class="hint">N terms used below</span></summary>
      <dl><div><dt>Term</dt><dd>One or two plain sentences.</dd></div> …</dl></details>
    <section class="sec reveal" id="ID-sec-functional"><h3>Functional requirements</h3>
      <ul class="reqs"><li>One line.</li></ul><p class="out">Out of scope: …</p></section>
    <section class="sec reveal" id="ID-sec-nonfunctional"><h3>Non-functional requirements</h3>
      <ul class="reqs nfr"><li><strong>Quality.</strong> Why it matters here.</li></ul></section>
    <section class="sec reveal" id="ID-sec-entities"><h3>Core entities</h3>
      <ul class="entities"><li><strong>Thing:</strong> what it holds.</li></ul></section>
    <section class="sec reveal" id="ID-sec-api"><h3>API design</h3>
      <div class="api-list"><div class="api">
        <div class="api-sig"><span class="method">POST</span><code>/things</code></div>   <!-- method classes: (none)=POST, get, put, patch, delete -->
        <p>What it does.</p>
        <div class="io"><div><span class="io-l">Request body</span><pre>{ … }</pre></div><div><span class="io-l">Response 201 Created</span><pre>{ … }</pre></div></div>
      </div></div></section>
    <section class="sec" id="ID-sec-hld"><h3>High-level design</h3>
      <div class="reveal"><p>…</p><h4>1. First requirement</h4><p>…</p>
        <div class="table-scroll"><table class="schema"><caption>Table: name</caption><thead><tr><th>Column</th><th>Type</th><th>Note</th></tr></thead><tbody><tr><td>col</td><td>text</td><td>…</td></tr></tbody></table></div></div>
      <figure class="diagram-fig"> … see below … </figure>
      <aside class="callout why reveal"><span class="callout-label">Why</span><p><strong>Key trade-off?</strong> …</p></aside>
    </section>
    <section class="sec" id="ID-sec-deepdives"><h3>Deep dives</h3>
      <div class="dive reveal"><h4>How do we …?</h4><p>…</p>
        <ol class="options"><li><strong>Option.</strong> Pros and cons.</li><li class="pick"><strong>Option.</strong><span class="pick-tag">Pick</span> …</li></ol>
        <p>Why this pick.</p></div>
      <div class="reveal"><h4>Final design</h4><p>One sentence on what the deep dives added.</p></div>
      <figure class="diagram-fig" id="ID-final"> … the complete, annotated system … </figure>
      <div class="next reveal"><h4>What you could add next</h4><ul class="next-list"><li>…</li></ul></div>
    </section>
    <section class="sec reveal" id="ID-sec-tips"><h3>Interview tips</h3>
      <dl class="qa"><div><dt>Follow-up question?</dt><dd>One-line answer.</dd></div></dl>
      <h4>Common mistakes</h4><ul class="mistakes"><li>…</li></ul>
      <aside class="callout tip"><span class="callout-label">Interview tip</span><p>…</p></aside>
      <aside class="callout confidence"><span class="callout-label">Confidence note</span><p>…</p></aside>
    </section>
    <p class="sources">Sources: …</p>
  </div>
</article>
```

Diagram figure: `<figure class="diagram-fig"><div class="diagram-scroll" tabindex="0" role="group" aria-label="Diagram: …. Scrollable on small screens."><svg class="diagram" viewBox="0 0 760 300" role="img" aria-labelledby="ID-d1-t ID-d1-d"><title id="ID-d1-t">…</title><desc id="ID-d1-d">…</desc> … </svg></div><figcaption>…</figcaption><button class="replay" type="button" aria-label="Replay diagram animation">Replay</button></figure>`

### Diagram quality: make every diagram feel complete
A reader should understand the system from the diagram alone, without the prose. Think of a good whiteboard sketch (Hello Interview's final designs are a good reference for *how much* a diagram should say), drawn in this site's style.
- **Every box says what it does,** not just its name: a title plus 1-3 short `d-item` lines of what it does in this design ("- new link: get a number," / "base62 it, save the row"). A plain one-word box is only fine for the client and the load balancer.
- **Every data store says what it holds:** put a `d-note` "sign" next to each database, cache, queue or file store listing the table name and key fields, or the cache key -> value and TTL, joined to the store with a short `d-line`.
- **Every arrow says what flows:** a short `d-label` verb or payload ("next number", "check first", "read/write", "copies writes"). Use two arrowheads where a box both asks and gets an answer. Number the labels ("1. …", "2. …") when order matters.
- **Layout:** requests flow left to right (client on the left, storage on the right or bottom). Helpers sit above or below the box that calls them. No crossing lines, nothing overlapping, at least ~10px between any text and an edge or another box. Keep the viewBox 760 wide (taller is fine) so it fits the column without scrolling on desktop.
- **The Final design shows the chosen answer:** every component the deep dives picked, each annotated, and nothing from "What you could add next".
- Packets: one colour per flow (gold = the write/create flow, cyan = the read/follow flow), explained in the caption.
- Theme: blocks, signs and redstone arrows already blend in. Don't add extra decoration; clarity beats Minecraft here.

SVG parts (styled by shared CSS; set `style="--i:N"` for the order things appear, N = 0,1,2…):
- **Node:** `<g class="d-node VARIANT" style="--i:0"><rect x y width height/><text class="d-text" x y text-anchor="middle">Name</text><text class="d-sub" …>small note</text></g>`. Always exactly one plain `<rect>` (no `rx`); the page's JS turns it into a blocky pixel block. Variants: (none) = stone, generic box such as a load balancer or external site; `grass` = client / user / browser; `cmd` = app server or service doing the logic; `chest` = database or file storage; `gem` = cache; `furnace` = queue, worker, counter or background job. Node titles use a pixel font: keep them short (≤12 characters per line; split into two `d-text` lines if needed) and keep `d-sub` notes to ~20 characters for a 150-wide node.
- **Edge:** `<path class="d-edge [accent]" style="--i:1" d="…"/>` plus arrowhead `<path class="d-arrow [accent]" style="--i:1" d="M x1 y1 L x2 y2 L x3 y3 Z"/>`. Use right-angle paths (H/V). `accent` = the main/hot path (bright redstone). Never dashed edges (the draw-in animation uses dasharray).
- **Lifeline** (sequence diagrams): `<path class="d-line" style="--i:0" d="M x y1 V y2"/>`.
- **What a box does:** inside a node, under its `d-text` title, add left-aligned lines `<text class="d-item" x y>- what it does</text>` (≈30 characters per line for a 200-wide box; indent continuation lines by 10). Make the node tall enough: about 30 + 20 per line.
- **What a store holds (sign):** `<g class="d-note" style="--i:N"><rect x y width height/><text class="d-note-t" x y>links table</text><text class="d-mono" x y>short_code  PK</text>…</g>`, one `d-mono` line per field, 18-20 apart; ~190 wide. Join it to its store with `<path class="d-line" d="…"/>`. Escape `<` as `&lt;`.
- **Label:** `<text class="d-label" style="--i:2" …>`.
- **Packet** (a small item square moving along a path; time is driven by the SVG timeline, so use static `begin` offsets):
  `<rect class="d-packet" x="-6" y="-6" width="12" height="12" opacity="0"><animateMotion dur="7s" begin="1s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear" path="M…"/><animate attributeName="opacity" dur="7s" begin="1s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.02;.68;.7;1"/></rect>`
  Add class `alt` (cyan) or `red` for a second kind of packet, and say what each colour means in a label or the caption. Keep all packets in one diagram on the same `dur`. A request-flow diagram can use one continuous path that zig-zags along the messages.
- Keep text ≥ 12px in user units and labels clear of nodes and edges. On narrow screens the diagram scrolls sideways (min-width set in CSS).

## Run checklist

1. List existing topics, patterns, dates and levels → choose a new topic, a pattern different from the last two, and the right level.
2. Research with web search/fetch (Hello Interview breakdown if one exists for what to cover, plus at least one more reputable source). Decide what to hedge.
3. Write the entry (Legend, all required sections in order, the simple architecture diagram, the Final design after the deep dives, and a request flow only if needed) + TOC line, copying the newest entry's markup. Check every diagram against "Diagram quality". Then do the cut pass from "Same coverage, less content".
4. `python scripts/validate.py` → fix until OK.
5. Commit with the message format and trailers above, then `git push origin HEAD:main`.
