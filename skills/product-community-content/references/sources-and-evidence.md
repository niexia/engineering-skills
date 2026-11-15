# Sources and evidence

## Access rules

- Use public pages, public search results and the product's own repository.
- Read only as an unidentified reader. Do not log in as the user, solve login
  walls, bypass rate limits or scrape account data.
- Do not collect private messages, support tickets, emails, order data or
  reviewer profiles. A public handle may appear only next to its quote.
- Stop when the budget is spent: 10 searches, 15 reviews or 8 minutes of
  collection, whichever comes first. Five strong reviews are enough.

## Where to look

| Source | Query or URL | Notes |
| --- | --- | --- |
| Chrome Web Store | `site:chromewebstore.google.com "<product>"`, then the listing URL from the profile | Reviews render client-side; open the listing and read what is visible in this run |
| Reddit | `site:reddit.com "<product>"`, `"<product>" review`, `"<product>" (bug OR issue OR alternative)` | Search results give thread URLs; open the thread and read comments |
| GitHub | `repo:<owner>/<repo> is:issue sort:created-desc`, `repo:<owner>/<repo> is:discussion`, public API `/repos/<owner>/<repo>/issues?state=all&sort=created` | Unauthenticated API allows 60 requests per hour; prefer recent threads over exhaustiveness |
| X | `site:x.com "<product>"`, `"<product>" (extension OR app OR tool)` | Logged-in only; treat snippets as unverified |
| Xiaohongshu | `site:xiaohongshu.com "<product>"`, `"<product>" 体验 OR 测评 OR 好用吗` | Login wall; ask the user to paste note text and date when it matters |
| App stores | `"<product>" site:apps.apple.com OR site:play.google.com` | Same client-rendering limits as the Chrome listing |

Load the category-specific places too: the subreddit for the product's category,
the relevant community forum and any public Discord or forum mirrors that search
engines index.

## Evidence grades

| Grade | Meaning | Allowed use |
| --- | --- | --- |
| Verified | The public page was opened in this run | Quote verbatim, with platform and date |
| Aggregated | A rating or count was visible on a listing in this run | Cite with the date observed; do not invent per-review quotes |
| Unverified | Only a search snippet was seen | Context for choosing where to look; do not quote or build the angle on it |
| Project fact | A file or URL read in this run | State as product fact, not as user opinion |

A rating without the review text is not evidence for a specific complaint.

## Recording

| Platform | Date | URL | Rating | Quote | Topic | Sentiment |
| --- | --- | --- | --- | --- | --- | --- |

Keep quotes short—one or two sentences—and in the original language. Preserve
spelling and punctuation; use `[…]` for an omission and never join separate
sentences into one quote.

## Selection

Prefer, in order:

1. Recent feedback about the change this run covers.
2. Specific experience: what the person did, what broke, what saved time.
3. A complaint that is fair and that the latest change answers.
4. Contrast with the previous behaviour, when a reviewer describes it.

Exclude duplicate posts across subreddits, review farms, competitor marketing,
reviews of a similarly named or competing product, and comments that only restate
the listing text. A search for a short product name often returns a different
product; check the listing URL or the product name in the review before quoting.

## Deduplication

Normalize the URL by dropping query strings and fragments, then compare it with
`state.json.seen_reviews`. When the same review appears under two URLs, keep the
first and treat the repeated text as already seen. Skip matches silently and
mention only the count in the brief.

## When sources fail

Record the failure mode in `brief.md` (`login wall`, `client-rendered`,
`rate limited`, `no public mentions`) and keep going. If no review can be
fetched, the run may still ship the latest-change angle, clearly labelled as
product news rather than user validation. Never invent a review, a rating, a user
count or a quotation to fill the gap.
