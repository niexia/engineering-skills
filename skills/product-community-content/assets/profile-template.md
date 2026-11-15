# Product profile

Keep this file beside the product's content work, not in the skill library.
Fill only what can be sourced; write `unknown` for gaps and resolve it when the
answer affects the draft.

## Product

- Name:
- One sentence:
- Category:
- Distribution (extension store, app store, web, self-hosted):
- Repository:
- Listing:
- Site:
- Support or community:

## Audience

- Primary:
- Secondary:
- Not for:

## Positioning

- Problem solved:
- Three differentiators:
- Closest alternatives, stated factually and without disparagement:

## Voice

- Language, per platform:
- Register:
- Words and claims to avoid:
- Claims that need a source in every run:

## Images

| Path or URL | Shows | Public and cleared |
| --- | --- | --- |

## Channels

| Platform | Account | Rules or limits | Self-promotion policy |
| --- | --- | --- | --- |
| X | | | |
| Xiaohongshu | | | |
| Reddit | r/ | read the rules page during the run | |

## Publishing

- Default mode: `draft`
- Standing authorization: none. If granted, record the platform, account, scope
  and date; the run may then publish within that scope.

## State

`state.json` in the same folder:

```json
{
  "product": "",
  "last_run": "YYYY-MM-DD",
  "seen_reviews": [{ "url": "", "first_seen": "YYYY-MM-DD" }],
  "angles": [
    { "date": "YYYY-MM-DD", "angle": "", "evidence": [""], "platforms": ["x"] }
  ],
  "published": [
    { "date": "YYYY-MM-DD", "platform": "x", "url": "", "angle": "" }
  ]
}
```

Prune `seen_reviews` older than a year and keep the file small enough to read
in one pass.
