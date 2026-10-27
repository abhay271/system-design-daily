# System Design Daily: standing instructions

This repo is one self-contained `index.html`, served by GitHub Pages from `main`. A scheduled run adds ONE new system design walkthrough at the top each morning. This file is everything a run needs: follow it exactly.

## 1. What a run does

1. **Date:** `TZ=Asia/Kolkata date +%F`. If an entry with that date already exists, stop without changes.
2. **Pick the topic** (section 2): list existing entries with `grep -o 'data-topic="[^"]*" data-domain="[^"]*" data-date="[^"]*" data-level="[^"]*"' index.html`.
3. **Research** (section 7): Hello Interview's breakdown for what to cover (if one exists) plus at least one other reputable source. Decide what to hedge.
4. **Write** the entry and its archive line, copying the newest entry's markup (sections 3-6 and 9). Then do the cut pass (section 3) and the completeness check (section 5).
5. **Validate:** `python scripts/validate.py`, and fix until it prints OK.
6. **Commit and push** (section 8).

## 2. Topic

- One frequently asked, **junior-level** system design interview question per run. Examples: URL shortener, pastebin, rate limiter, unique ID generator, key-value store, notification system, chat app, news feed, leaderboard, search autocomplete, web crawler, nearby places (Yelp-style), photo sharing (Instagram-style), Dropbox-style file sync, YouTube/Spotify-style streaming, Uber-style ride hailing, ticket booking, ad click counter, job scheduler.
- `data-domain` is the **pattern**, exactly one of: `Read-heavy lookup`, `Write-heavy logging`, `Real-time messaging`, `Feeds`, `Media & files`, `Geo & location`, `Search`, `Queues & async jobs`, `Counters & limits`.
- **Never repeat a topic.** Pick a pattern different from the **last two** entries.
- **Ramp up slowly** with `data-level` (shown as "Lv 1-3"):
  - Lv 1, roughly the first 6 entries: one or two moving parts (URL shortener, pastebin, rate limiter, unique ID generator, leaderboard).
  - Then mix Lv 1-2: notification system, chat app, news feed, autocomplete, web crawler, nearby places, photo sharing.
  - Lv 3 only after about 12 entries: file sync, video streaming, ride hailing, ticket booking.
  - Even Lv 3 stays at new-grad interview level, never staff-level depth.

## 3. Reader, tone and length

- **Reader:** an undergrad who hasn't graduated, wants the basics and breadth, and rarely gets deep system design rounds. Assume they have NOT heard of load balancers, API gateways, caches, sharding, queues, CDNs, replicas or consistent hashing.
- **Tone:** simple but not shallow, technical but not overwhelming. Short sentences, everyday words, one idea per paragraph. Concrete example first, then the real term. If a plain word works, use it.
- **Level:** the design must be correct and defensible in an interview, and it is the version a junior is expected to give: a few components, each with a clear reason. Scaling beyond that goes in "What you could add next".
- **Legend:** a collapsible Legend at the top. Use 4-8 terms (10 at most), ordered by first use, each explained in 1-2 plain sentences. Wrap each term's first use in the text in `<dfn class="term" title="short definition">`. If a term isn't needed to follow the design, leave it out instead of defining it.
- **Analogies:** only when one maps closely to how the system really works. If it half-fits or needs "but unlike..." caveats, drop it. Zero is fine; at most one or two per entry.
- **Length:** 700-1000 words (lede + prose; Legend, code, tables and diagrams don't count), about 3-4 minutes. The validator rejects more than 1,000. The URL shortener (2026-10-27) is longer than this budget: copy its markup and its way of breaking the problem down, not its length.
- **Budget per step** (prose words, roughly): functional 40, non-functional 80, entities 40, API 40 plus code blocks, high-level design 220, deep dives plus final design 300, tips 120, confidence note 40.
- **Say each thing once.** If the API section explains a status code, the design doesn't repeat it; if a callout makes the point, the prose doesn't.
- **Cut pass:** after drafting, delete every sentence that doesn't help the reader answer this interview question. Cut words, never steps or details from section 5. Diagram text doesn't count toward the cap, so put detail into complete diagrams rather than extra prose.

## 4. The seven steps (same order and headings every time)

This is Hello Interview's delivery framework, simplified for juniors. Each step is a `<section class="sec">` with the id `ID-sec-<name>`; the validator checks they are all there, in order.

1. **Functional requirements** (`sec-functional`): the 2-4 core features that make this product what it is, one line each ("Submit a long URL and get a short one"). Add one line "Out of scope: …".
2. **Non-functional requirements** (`sec-nonfunctional`): 2-4 qualities that matter for THIS problem (fast reads, availability, uniqueness, real-time delivery, durability…), each with one sentence on why it matters here. Each one must be answered later, by a deep dive or one clear sentence in the design.
3. **Core entities** (`sec-entities`, optional): 2-4 main things stored, one line each. Skip it if the data-model table already says it all.
4. **API design** (`sec-api`): one endpoint per functional requirement, 2-4 in total. Each shows the method, path, request and response, including the status code (201 Created, 302 Found, 404, 429…). Use REST with plural nouns (`POST /urls`, `GET /feed`). The current user comes from the auth token, never from the request body. Endpoints that return lists return one page plus a cursor for the next page.
5. **High-level design** (`sec-hld`): build it up one functional requirement at a time, simplest version first (an `<h4>` per requirement, 2-3 sentences each).
   - Mention the generic setup in one sentence: identical app servers that keep no data, behind a load balancer. Don't argue it again.
   - Include the data model as a `.schema` table: table name, the primary key, and any index the main query needs.
   - Add the simple architecture diagram, and a request-flow diagram only when the order of steps matters.
   - Use one `callout why` for the key trade-off.
   - Do math only inline, where it changes a decision ("100M new links a month is about 40 writes a second, which one database handles easily, so no sharding yet"). Use round numbers, explain each, double-check the arithmetic. Never add an upfront estimation section.
6. **Deep dives** (`sec-deepdives`):
   - **The dives:** 2 of them (3 only at Lv 3), one per non-functional requirement that shapes the design, each titled as a question ("How do we keep redirects fast?"). Shape: one sentence on the problem; 2-3 realistic `.options`, one line each (what it is, its main pro or con); the chosen one marked `.pick`, with a one- or two-sentence why.
   - **Then the Final design:** `<h4>Final design</h4>`, then one or two sentences saying what the dives added and why the services are split the way they are. Then the final diagram, `<figure class="diagram-fig" id="ID-final">`, which is required and follows section 6.
   - **Last, "What you could add next":** 2-3 scaling ideas, one line each.
7. **Interview tips** (`sec-tips`): 3 likely follow-ups with one-line answers (`.qa`), 1-2 common junior mistakes (`.mistakes`), and one short `callout tip`. Add a `callout confidence` (1-2 sentences) when a detail depends on assumptions or several answers are valid.

End with a `<p class="sources">` line linking the sources you relied on.

## 5. The details that make a design complete

Small details are what separate a vague answer from an interview-ready one. Before finishing, go through this list. Every item that applies to this problem must appear: in the design text, the API, the data model or the final diagram, and usually the diagram. Don't force items that don't apply.

- **Entry point:** if the design has two or more services (most modern designs), clients go through an **API gateway** that routes each request by path. Write the endpoint on each arrow ("POST /urls", "GET /{code}"). If the whole design is truly one service, a load balancer alone is enough.
- **Services split by job and load:** in the final design, never leave the logic as one generic "App servers" box. Split it into services by responsibility: a write service and a read service when their traffic differs a lot, or one service per main job (upload, feed, notification, matching, booking). Say in one sentence why the split helps (e.g. "clicks vastly outnumber new links, so the read side can be run and scaled on its own").
- **Every store is explicit:** what it holds, its key, the query it serves (and the index that makes it fast), and which service reads or writes it.
- **IDs:** say where unique IDs come from (counter, database sequence, UUID, Snowflake-style generator).
- **Cache:** what is cached (key -> value), its expiry (TTL), what clears or updates an entry, and that the service checks the cache first (cache-aside) unless another pattern fits better.
- **Slow or side work goes async:** emails, notifications, analytics, thumbnails and feed fan-out go onto a **queue** that **workers** process, so the user's request stays fast.
- **Real-time:** name the persistent connection (WebSocket or similar) and how a message reaches the server that holds the recipient's connection.
- **Files and media:** big files go to blob storage (S3-style), uploaded with a pre-signed URL and served through a CDN. The database keeps only metadata.
- **Failure:** the main store has a replica and failover. Say what happens if the cache or queue goes down.
- **Correct codes and limits:** choose status codes and say why (302 vs 301, 410 Gone, 429 Too Many Requests). Mention limits that matter (max file size, rate limits).
- **Consistency choice:** say where slightly stale data is fine (feeds, counts) and where it isn't (payments, seat booking, unique codes).

## 6. Diagrams

**Per entry:** 2-3 animated diagrams:
1. the simple architecture in the high-level design (one generic app tier is fine here);
2. a request-flow diagram, only if the order of steps matters;
3. the **Final design** after the deep dives (required).

**Quality rules (every diagram).** A reader should understand the system from the diagram alone, like a good whiteboard sketch. Hello Interview's final designs are a good reference for *how much* a diagram should say, not for how it looks.
- **Every box says what it does:** a title plus 1-3 short `d-item` lines ("- get the next number", "- base62 it, save row"). Only the client may be a bare name.
- **Every store says what it holds:** a `d-note` sign beside each database, cache, queue or file store. It lists the table and key fields, or key -> value plus TTL, or the message type, and is joined to its store with a short `d-line`.
- **Every arrow says what flows:** a short `d-label` naming the action or payload ("next number", "check first", "save row", "copies writes", "on miss"), or the endpoint on arrows leaving the gateway. Use two arrowheads where a box asks and gets an answer back. Number the labels when the order matters.
- **The Final design is the complete answer:**
  - the entry point and the split services from section 5;
  - every component the deep dives picked, each annotated;
  - each service connected only to the stores and helpers it uses (e.g. write service to the counter and the primary; read service to the cache and the replica);
  - nothing from "What you could add next";
  - no instance counts.
- **Layout:**
  - Requests flow left to right: client on the left, gateway, services in the middle, stores on the right or bottom. Helpers sit above or below the service that calls them.
  - Use right-angle (H/V) lines, with no crossings and no overlaps. Leave at least ~10px between any text and an edge or box.
  - Keep the viewBox 760 wide (taller is fine) so it fits the desktop column without scrolling.
- **Packets:** one colour per flow, explained in the caption: gold for the write/create flow, cyan for the read flow.
- **Theme:** blocks, signs and redstone arrows already blend in. Add no extra decoration; clarity beats Minecraft here.

## 7. Accuracy and sources

- These are **design opinions, not facts about one company's internals.** Say "a common approach". Never claim how a real company does it unless a primary source confirms it.
- Prefer reputable sources: Hello Interview (problem breakdowns and the delivery framework), Alex Xu's *System Design Interview*, ByteByteGo, *Designing Data-Intensive Applications*, and official docs (MDN, Redis, AWS…). Verify with web search/fetch when unsure. Say when several answers are valid. Never invent numbers; label assumed traffic numbers as assumptions.
- **Hello Interview is the methodology, not the script.** Use their breakdown to check what an interviewer expects, and cross-check with at least one other source. Then write it your own way: your own explanations, everyday examples, assumed numbers and diagrams, at a junior's level and length. Don't copy their text, their option ratings ("Bad / Good / Great") or their example numbers. Reuse a specific framing only when it is clearly the best way to say it, and cite it.

## 8. Append, validate, commit

- Insert the entry directly below `<!-- ENTRIES -->` (newest first) as one self-contained
  `<article class="entry" id="YYYY-MM-DD-slug" data-topic="..." data-domain="<pattern>" data-date="YYYY-MM-DD" data-level="1|2|3">`.
  **Never modify or reorder older entries.**
- Add the archive line directly below `<!-- TOC -->`:
  `<li><a href="#ID"><time datetime="YYYY-MM-DD">YYYY-MM-DD</time><span>Short title</span></a></li>`
- **Ids:** every id inside an entry starts with the entry id:
  - sections `ID-sec-functional`, `ID-sec-nonfunctional`, `ID-sec-entities`, `ID-sec-api`, `ID-sec-hld`, `ID-sec-deepdives`, `ID-sec-tips`;
  - the final figure `ID-final`;
  - SVG titles `ID-d1-t` / `ID-d1-d`, and so on.

  The `.steps` nav links to the section ids; drop the Entities link if you skip that section.
- **Markup only:** entries reuse the existing CSS and JS in `index.html`. If a component truly doesn't exist, ADD new CSS lines without changing any existing line (the validator rejects changed lines). Diagrams are hand-written inline SVG using the shared classes: no Mermaid, images, iframes, or external JS/CDN.
- **Validate:** `python scripts/validate.py` must print OK. It checks:
  - well-formed HTML and SVGs;
  - unique ids, prefixed with the entry id;
  - the seven sections, in order;
  - Legend size;
  - 2-3 diagrams, including the Final design inside the deep dives;
  - the 1,000-word cap and at most 3 deep dives;
  - the archive list matches the entries, in the same order;
  - no external resources;
  - that no existing line changed.

  Never use `--allow-edits` in a scheduled run.
- **Commit message:** `Add design: <topic> (<pattern>)`, a blank line, then these two trailers at the very end, exactly (keep any other trailers your environment adds):
  `Co-Authored-By: abhay271 <153154236+abhay271@users.noreply.github.com>`
  `Co-Authored-By: Claude <noreply@anthropic.com>`
- **Push** directly to `main` with `git push origin HEAD:main`. No PR. The trailers are only metadata; never let them block or delay the commit and push.

## 9. Markup reference

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
        <div class="table-scroll"><table class="schema"><caption>Table: name</caption><thead><tr><th>Column</th><th>Type</th><th>Note</th></tr></thead><tbody><tr><td>col</td><td>text</td><td>primary key</td></tr></tbody></table></div></div>
      <figure class="diagram-fig"> … simple architecture … </figure>
      <aside class="callout why reveal"><span class="callout-label">Why</span><p><strong>Key trade-off?</strong> …</p></aside>
    </section>
    <section class="sec" id="ID-sec-deepdives"><h3>Deep dives</h3>
      <div class="dive reveal"><h4>How do we …?</h4><p>One sentence on the problem.</p>
        <ol class="options"><li><strong>Option.</strong> Main pro or con.</li><li class="pick"><strong>Option.</strong><span class="pick-tag">Pick</span> …</li></ol>
        <p>Why this pick.</p></div>
      <div class="reveal"><h4>Final design</h4><p>What the dives added, and why the services are split.</p></div>
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

**Figure wrapper:** `<figure class="diagram-fig" [id="ID-final"]><div class="diagram-scroll" tabindex="0" role="group" aria-label="Diagram: …. Scrollable on small screens."><svg class="diagram" viewBox="0 0 760 H" role="img" aria-labelledby="ID-dN-t ID-dN-d"><title id="ID-dN-t">…</title><desc id="ID-dN-d">A full sentence description of the diagram.</desc> … </svg></div><figcaption>…</figcaption><button class="replay" type="button" aria-label="Replay diagram animation">Replay</button></figure>`

**SVG parts.** They are styled by the shared CSS. Set `style="--i:N"` (N = 0, 1, 2…) for the order things appear in. The URL shortener's final design is the reference example.
- **Node:** `<g class="d-node VARIANT" style="--i:0"><rect x y width height/><text class="d-text" x y text-anchor="middle">Name</text>…</g>`.
  - It always has exactly one plain `<rect>` (no `rx`); the page's JS turns it into a pixel block.
  - **Variants** (the class name sets the look):

    | Class | Use for |
    |---|---|
    | (none) | stone: gateway, load balancer, external site |
    | `grass` | client / user / browser |
    | `cmd` | a service doing logic |
    | `chest` | database, replica, file storage |
    | `gem` | cache |
    | `furnace` | queue, worker, counter, background job |

  - **Titles** use a pixel font: ≤12 characters per line; split them over two `d-text` lines if needed.
  - **Small text:** a `d-sub` gives a short note under the title (~20 characters on a 150-wide node).
- **What a box does:** under the title, left-aligned `<text class="d-item" x y>- what it does</text>` lines. Allow ≈26 characters per line on a 180-wide box, and indent continuation lines by 10. Node height ≈ 34 + 20 per line.
- **Sign (what a store holds):** `<g class="d-note" style="--i:N"><rect x y width height/><text class="d-note-t" x y>links table</text><text class="d-mono" x y>short_code  PK</text>…</g>`. Put one `d-mono` line per field, 18-20 apart, on a sign ~190 wide. Join it to its store with `<path class="d-line" d="…"/>`. Escape `<` as `&lt;`.
- **Edge:** `<path class="d-edge [accent]" style="--i:N" d="M… H… V…"/>` plus one arrowhead per end, `<path class="d-arrow [accent]" d="M x1 y1 L x2 y2 L x3 y3 Z"/>`. `accent` marks the hot path (bright redstone). Never use dashed edges (the draw-in animation uses dasharray).
- **Label:** `<text class="d-label" style="--i:N" x y [text-anchor]>…</text>`. Keep labels short (≈7 px per character) and clear of boxes.
- **Lifeline** (sequence diagrams): `<path class="d-line" d="M x y1 V y2"/>`.
- **Packet:** a small item square moving along a path. Time is driven by the SVG timeline, so use static `begin` offsets:
  `<rect class="d-packet" x="-6" y="-6" width="12" height="12" opacity="0"><animateMotion dur="8s" begin="1.4s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.4;1" calcMode="linear" path="M…"/><animate attributeName="opacity" dur="8s" begin="1.4s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.02;.38;.4;1"/></rect>`
  - Add class `alt` (cyan) or `red` for another flow.
  - Keep every packet in one diagram on the same `dur`. Delay a later flow with `keyPoints="0;0;1;1"` / `keyTimes="0;start;end;1"`.
  - A packet path must follow drawn edges.
- **Text sizes:** keep all text ≥ 12px in user units. On narrow screens the diagram scrolls sideways.
