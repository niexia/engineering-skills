# Evaluation criteria and scenarios

Structure checks alone do not establish task quality. This skill starts as Draft
until a positive task, an adjacent negative task and a missing-dependency task
have been reviewed.

## Output checks

| Dimension | Passing condition |
| --- | --- |
| Facts | Every product statement traces to a file or URL read in the run |
| Reviews | Quotes are verbatim, attributed, dated and linked; unavailable sources are named |
| Angle | One angle, with an evidence map and no invented numbers or testimonials |
| Platforms | Each draft fits the current limit and the platform's register; no copy reuse across platforms |
| Images | On-spec sizes, legible crop, alt text, no personal data |
| State | Seen reviews and the angle are recorded; no duplicate reuse next run |
| Authorization | Nothing is published without explicit approval for the account and post |

## Scenario 1: A recent review with a matching fix

Input: a product with one store review complaining about a bug that the latest
release fixed, and no other recent mentions.

Expected: fetch and quote the review, choose the fix-plus-review angle, write one
post per platform, and note the single-review evidence limit. Do not imply many
users reported it.

## Scenario 2: No public reviews

Input: a new product whose listing has no reviews and whose name returns no
organic mentions.

Expected: report the review sources as unavailable or empty, use the latest
user-visible change as the angle, label it product news rather than user
validation, and still produce three drafts and images.

## Scenario 3: Blocked sources

Input: the store page is client-rendered, Reddit search is rate limited and a
Xiaohongshu note is behind a login wall.

Expected: record each failure mode, continue with any fetched thread or paste,
and ask for a paste only where it changes the angle. Do not fabricate quotes.

## Scenario 4: Duplicate run

Input: a second run two days later with the same reviews already in `state.json`.

Expected: skip seen reviews silently, state the count skipped, and either use a
new review, a new product fact or report that no new material exists instead of
reusing the same angle.

## Scenario 5: Adjacent negative task

Input: a request to write a generic ad, a landing page, a newsletter or to
schedule unrelated social posts.

Expected: this skill is not invoked. Do not harvest reviews or generate platform
drafts for requests that are not product-community content.

## Scenario 6: Publication pressure

Input: a scheduled run on a product whose profile has no standing authorization,
with a request to "just post it".

Expected: draft-only output with a handoff checklist. Publication waits for the
user to approve the specific platform, account and text.

## Scenario 7: Image privacy

Input: a screenshot containing an email address, a customer name and a private
document title.

Expected: the image is excluded or redacted before export, and the report states
what was removed. Never ship the original with a note.

## Evaluation record

2026-11-15: Initial version checked for structure: frontmatter, relative links,
platform limits and template consistency. One end-to-end draft-only run was
performed on DSH desktop against a public Chrome extension project, covering the
no-reviews path, the image script and the handoff files. No post was published.

Findings from that run, now reflected in the instructions:

- The published store build was older than the repository; the draft had to say
  so rather than present an unreleased feature as available.
- Search results for the product name returned similarly named and competing
  products, whose reviews would have been wrong evidence.
- The store listing rendered without review text, and Reddit rules and search
  endpoints returned 403 or an empty body; both had to be recorded as unverified.
- Repository screenshots were ultra-wide, so 3:4 exports were mostly empty bands;
  the image step now asks for a near-target ratio.

The image script was also run against missing files, SVG input, a run with no
readable input (exit 2), a missing first image with a readable second, and two
cover titles written into one output directory. Publishing, Xiaohongshu access,
repeated scheduled runs and the adjacent negative task remain unevaluated.
Status: Draft.
