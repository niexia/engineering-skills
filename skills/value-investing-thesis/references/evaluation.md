# Evaluation criteria and scenarios

These inputs are independently fictional and contain no real companies, people or
market data. They support rule walkthroughs; they do not establish independent
Agent execution.

## Output checks

| Dimension | Passing condition |
| --- | --- |
| Verdict | One of BUY, WATCH or PASS, supported by the evidence and scoring rules |
| Facts | Material claims cite a source and date; unavailable data is marked, not invented |
| Business model | Revenue drivers, unit economics and the stable/cyclical/bubble split are explicit |
| Three lenses | Buffett, Duan and Munger each contribute a distinct question and evidence |
| Normalized earnings | A bridge from reported profit to owner earnings, with adjustments labeled |
| Valuation | Bear/base/bull cases, implied returns and a reverse-DCF cross-check |
| Risk | A pre-mortem with ranked causes, early warnings and responses |
| Decision | Buy/watch/avoid zones, position size, expected return and sell rules |
| Image | A valid PNG or SVG exists, is readable at chat size and has no clipped text |
| Integrity | No invented quote, number, date or management intention |

## Scenario 1: Positive task

Input: A listed consumer company with volatile earnings. The user asks whether it
is a long-term investment and requests a summary image.

Expected: Invoke the skill. Build the fact base, split the three layers, score the
five dimensions with evidence, normalize earnings, show three valuation cases,
state a verdict and zones, and produce a valid summary card. The note separates
reported figures from estimates.

## Scenario 2: Adjacent negative task

Input: The user asks for a short-term trade, a next-week price target, or a
technical-analysis setup.

Expected: Do not invoke the long-term thesis workflow as if it answered the
question. Explain that the skill is for long-term business analysis, and offer the
long-term thesis instead. Do not invent a price target.

## Scenario 3: Missing price or share count

Input: The company has filed annual results but the current price or diluted share
count is unavailable.

Expected: Complete the qualitative and normalized-earnings work. Mark valuation as
unavailable, explain what is missing, and still produce the card with "n/a" in the
valuation fields. Do not invent a market cap.

## Scenario 4: Conflict between narrative and cash flow

Input: Revenue and reported profit are growing, but inventory days and receivables
days are rising faster than revenue, and operating cash flow is falling.

Expected: Flag the working-capital build. Separate the stable core from channel
stuffing or pull-forward. Lower the business-quality or risk score, and explain
the evidence. Do not accept the growth narrative at face value.

## Scenario 5: A great business at an expensive price

Input: A high-ROIC, wide-moat company trading at 45 times normalized earnings.

Expected: Score business and moat high, valuation low. The verdict is WATCH, not
BUY. State the price zone at which the expected return becomes adequate, and
explain that a great business can still be a poor investment at the wrong price.

## Scenario 6: Missing image tooling

Input: Pillow is unavailable in the runtime.

Expected: Run the script; it writes an SVG fallback and prints a warning. Verify
the SVG is well-formed, embed it, and tell the user that PNG conversion needs an
image tool. Do not skip the image.

## Scenario 7: User asks to copy a famous investor's position

Input: The user says "a well-known investor bought it, so it must be good" and asks
for a buy decision.

Expected: Treat the position as one data point, not proof. Rebuild the thesis from
primary sources, state the investor's actual reasoning if it is public, and warn
that copying a position without the same time horizon, position size and
information set is not the same investment.

## Scenario 8: Chinese output and font

Input: The user writes in Chinese and requests a Chinese summary card.

Expected: Write the note in Chinese, set `"locale": "zh"`, pass a CJK font if the
default fails, and verify the image for missing-glyph boxes. The card labels are
Chinese; values remain in the user's language.

## Evaluation record

2026-11-15: Initial version authored. The summary-card script was run on the
fictional `assets/example-summary.json` with Pillow 12.3.0 on macOS; it produced a
1600×2280 PNG (about 197 KB). The SVG fallback was rendered and parsed as
well-formed XML. Validation errors for a missing `verdict` and an out-of-range
score returned exit code 2. A Chinese card was rendered separately with a CJK font
and checked for missing glyphs. After adding price and market-cap to the header and
moving the expected-return line, the PNG and SVG were re-rendered and the Chinese
card was checked again.

Independent Agent behavior evaluation, the positive and negative scenarios above,
and user acceptance remain pending. Status remains Draft. Future records should
include host, date, outputs, and corrections after failures.
