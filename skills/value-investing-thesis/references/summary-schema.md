# Summary card schema

`scripts/make_summary_card.py` accepts a JSON object and renders a one-page
summary card. Required fields are marked with `*`. Unknown fields are ignored.
Keep the text short: the card is a summary, not the report.

## Example

```json
{
  "company": "Example Co",
  "ticker": "EXM",
  "market": "HK",
  "as_of": "2026-11-15",
  "currency": "HKD",
  "price": "142.1",
  "market_cap": "1,892亿 HKD",
  "verdict": "WATCH",
  "verdict_line": "Good business, fair price; wait for a better pitch.",
  "locale": "en",
  "scores": {
    "business": 4,
    "moat": 3,
    "management": 4,
    "valuation": 3,
    "risk": 3
  },
  "metrics": [
    {"label": "P/E (2026E)", "value": "20-22x"},
    {"label": "Dividend yield", "value": "1.8%"},
    {"label": "Net cash", "value": "142亿"},
    {"label": "Revenue growth", "value": "+23.8%"},
    {"label": "Net margin", "value": "30.0%"},
    {"label": "ROE (TTM)", "value": "71%"}
  ],
  "layers": [
    {"label": "Stable core", "text": "China offline: -5-10% in Q3; ~450 stores; 82m members."},
    {"label": "Cyclical", "text": "Overseas retail reset; inventory destocking."},
    {"label": "Bubble", "text": "China online -45-50%; resale premium gone."}
  ],
  "bull": [
    "The offline base is stable and cash-generative.",
    "The IP portfolio is broader than one character.",
    "A lower base makes 2027 comparisons easier."
  ],
  "bear": [
    "Normalized earnings may be 30-40% below the peak.",
    "Overseas stores carry fixed costs and inventory risk.",
    "A new global hit is not guaranteed."
  ],
  "lenses": {
    "buffett": "Narrow moat: brand and IP matter, but switching costs are low.",
    "duan": "Buy the business, not the character; watch the culture and the price.",
    "munger": "Invert: if the fad never returns, what is the floor?"
  },
  "decision": {
    "buy_zone": "110-120",
    "watch_zone": "120-160",
    "avoid_zone": ">200 without a new hit",
    "position": "<=5%",
    "expected_return": "+18% at 120"
  },
  "footer": "Not investment advice. Figures are illustrative."
}
```

## Field rules

| Field | Required | Rule |
|---|---|---|
| `company` | yes | Display name, 1-40 characters. |
| `ticker` | yes | Exchange ticker, 1-16 characters. |
| `market` | no | Exchange or market label. |
| `as_of` | yes | ISO date of the data cutoff. |
| `currency` | no | Currency code or label. |
| `price` | no | Number or string. Use "n/a" when missing. |
| `market_cap` | no | Short string with unit. |
| `verdict` | yes | `BUY`, `WATCH` or `PASS`. |
| `verdict_line` | yes | One sentence, <= 140 characters. |
| `locale` | no | `en` (default) or `zh`. |
| `scores` | yes | Five integers 1-5: business, moat, management, valuation, risk. |
| `metrics` | yes | 1-6 items (4-6 preferred); label <= 18 chars, value <= 14 chars. |
| `layers` | yes | Exactly 3 items; each text <= 90 chars. |
| `bull` | yes | 1-3 items (2-3 preferred); each <= 80 chars. |
| `bear` | yes | 1-3 items (2-3 preferred); each <= 80 chars. |
| `lenses` | yes | One line each for `buffett`, `duan`, `munger`; <= 110 chars. |
| `decision` | yes | `buy_zone`, `watch_zone`, `avoid_zone`, `position`, `expected_return`. |
| `footer` | no | Disclaimer or data note. |

`locale: "zh"` switches the card's section labels to Chinese. The values can be
in any language; a CJK font is required for Chinese glyphs.

## Rendering notes

- The script wraps text and shrinks it within each panel. It does not rewrite
  content. If a bullet is too long, shorten the JSON instead of relying on the
  shrink step.
- The PNG card is 1600 × 2280 px. It is designed for portrait chat display. The
  SVG fallback uses the same width with a dynamic height.
- PNG output requires Pillow. Without Pillow, the script writes an SVG fallback
  and prints a warning.
- Font resolution order: `--font`, `SUMMARY_CARD_FONT`, common CJK system fonts,
  then Pillow's default font. If Chinese renders as boxes, pass a CJK font path.
- The script exits non-zero on missing required fields or invalid scores, and
  prints the field name.
