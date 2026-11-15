---
name: product-community-content
description: Turn a product's repository, listing and recent user reviews into platform-native X, Xiaohongshu and Reddit posts with prepared images. Use for recurring product content, launch posts and review-driven updates. Do not use for generic copywriting, paid ads or unrelated social scheduling.
---

# Product Community Content

One run turns one product and its recent user feedback into three platform-native
drafts plus prepared images. Each run finds one supportable angle, writes it three
ways, and leaves a handoff the user can publish.

Drafts by default. Publishing needs explicit authorization for the named accounts
and posts; see [Publishing](#publishing).

## Run setup

Inputs: the product (a readable project directory or public URL), an optional work
directory, and the platforms. Default platforms: X, Xiaohongshu, Reddit.

Keep per-product state in `<workdir>/.social-content/`, defaulting to the product
root:

```text
.social-content/
├── profile.md        # Positioning, audiences, links, constraints
├── state.json        # Seen reviews, past angles, published URLs
└── runs/2026-11-15/  # One folder per run
```

On the first run, create `profile.md` from
[the profile template](assets/profile-template.md) and fill it from the
project. A scheduled run must not wait for answers: record gaps in the profile,
continue with verifiable material, and ask in the report only for fields that
block every angle.

## 1. Establish product facts

Read the README, manifest or package metadata, changelog and releases, the store
or product listing, recent commits, and the project's images.

Record in the run brief:

- one-sentence description, the audience it serves, three differentiators
- the latest user-visible change with its date
- whether the repository is ahead of the published build; never describe
  unreleased work as available
- canonical links (site, listing, repository, support)
- available images with paths and what each shows

Every statement traces to a file or URL read in this run. Do not infer user
counts, ratings, rankings, benchmarks or revenue. Absent facts stay absent.

## 2. Harvest recent user reviews

Read [sources and evidence](references/sources-and-evidence.md) for query
patterns, access limits and deduplication. Collect reviews from the last 30 days
by default, or since `state.json.last_run` when that is later.

For each review record the platform, URL, date, rating when present, a short
verbatim quote, topic and sentiment. Keep the quote in its original language.

- Prefer specific, recent, on-topic feedback, including a complaint that the
  latest change addresses.
- Keep only reviews of this product. Reviews of a similarly named or competing
  product are not evidence, even when the category matches.
- Drop abusive content, personal data and anything a reviewer marked private.
- Never create, paraphrase into, or extend a quote. A review you could not fetch
  is not a review.
- Mark blocked sources (login wall, client-rendered page, rate limit) as
  unavailable and continue with the rest.
- Write seen review URLs into `state.json` so the next run skips them.

## 3. Choose one angle

Pick one primary angle for the run, supported by at least one fetched review or
one verifiable product fact. State it with an evidence map:

| Claim | Evidence | Risk |
| --- | --- | --- |
| What the post asserts | Review URL or file path | Overclaim, unsupported comparison |

Reject angles that need invented numbers, testimonials, comparisons or urgency.
Do not reuse an angle from the last two runs; prefer new feedback or a new
user-visible change. When no usable review exists, use the latest user-visible
change as the angle and say reviews were unavailable. Do not simulate user
enthusiasm.

## 4. Write platform drafts

Read [platform rules](references/platforms.md) before writing. Write each
platform from the angle rather than translating one post into three; audience,
register, length and link policy differ.

- X: one short post, an optional thread of up to four, one image, plain voice,
  minimal hashtags, no engagement bait.
- Xiaohongshu: a Chinese note with a concrete personal angle, a scannable body,
  modest emoji, relevant topics and a 3:4 cover.
- Reddit: a post for one subreddit that leads with the problem or the change,
  discloses authorship, follows that subreddit's current rules, and drops
  marketing adjectives.

Attribute a quoted review as written and keep its platform and date. Disclose that
the author builds the product. Never fake scarcity, users or endorsements.

Write the copy exactly as it will be pasted: one line per paragraph, with only
intentional line breaks. Do not invent first-person details on the user's behalf
— habits, counts, stories — and do not fill them with placeholders; use a
factual framing or leave a clearly marked gap in the draft.

## 5. Prepare images

Use [the image script](scripts/prepare_images.py) to export each chosen image at
1600×900 (X), 1080×1440 (Xiaohongshu) and 1200×630 (Reddit), plus an optional
cover. Run it once per cover language when the platforms need different titles.
Prefer an image whose ratio is near the target: an ultra-wide screenshot
letterboxes into a thin strip at 3:4, so take a fresh capture or use `cover`
instead of shipping mostly empty bands.
Check that the crop or letterbox keeps the product legible, write alt text, and
remove personal data, private document titles, customer names and emails before
export.

If the script cannot run, export with the host's image tools and state the sizes
actually produced.

## 6. Write the run output

```text
runs/YYYY-MM-DD/
├── brief.md          # Facts, reviews, angle, evidence map, gaps
├── x.md              # Copy, character count, image, alt text
├── xiaohongshu.md    # Title, body, topics, image list
├── reddit.md         # Subreddit, title, body, rule notes
├── publish.md        # Per-platform handoff checklist
└── assets/           # Exported images
```

Use [the post template](assets/post-template.md) for the draft files.
`publish.md` lists per platform the account, the copy source, images with alt
text, destination, disclosure line and post-publish check. It does not publish.

When a run folder already exists for today, write to `runs/YYYY-MM-DD-2/` rather
than overwriting an earlier run.

Update `state.json` with `last_run`, new seen reviews and the angle. Add a
`published` entry only after a post exists, with its URL.

## 7. Report to the user

Report concisely: sources consulted and unavailable, reviews found with links, the
chosen angle, the files written, and the decisions the user still owns. Do not
paste all drafts into the conversation; name the files.

## Publishing

Publish only when the user authorizes the specific platform, account and post. Use
the host's authorized tools and record the resulting URL in `state.json`. A
scheduled run stays draft-only unless the profile records standing authorization
for that account, and even then stop before an irreversible action you cannot
verify. External publication and messaging otherwise require user authorization.

## Quality bar

- Every claim in a draft traces to the evidence map.
- Review quotes are verbatim, attributed and short.
- Nothing unreleased is described as available.
- No invented metrics, testimonials, urgency or platform rules.
- Each platform reads as natively written for it.
- Images are on spec, legible and free of personal data.
- The voice matches the profile; unavailable sources are named, not papered over.
