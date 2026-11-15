# Accuracy playbook

The skill is designed to produce a defensible view, not a precise one. Accuracy
fails in five predictable ways:

1. **Invented numbers** — a plausible figure with no source.
2. **Stale data** — a price, filing or consensus treated as current when it is not.
3. **Mismatched data** — different periods, currencies, share bases or accounting
   definitions combined into one ratio.
4. **Arithmetic errors** — market cap, EV, P/E, margins, scenario values or
   expected returns that do not reconcile.
5. **Narrative overreach** — a strong story attached to weak evidence.

Every section below addresses one or more of these failures.

## 1. Evidence labels

Every load-bearing figure or claim carries exactly one label. A claim is
load-bearing when removing it changes the conclusion.

| Label | Use for | Must carry |
|---|---|---|
| `FACT` | A figure reported in a primary document, or returned by a data tool for a closed period | Document, page/table, period, currency, unit |
| `COMPANY CLAIM` | Guidance, market size, market share or any statement the company makes about itself that nothing independent confirms | Venue and date |
| `ESTIMATE` | Consensus or single-analyst figure | Vintage and analyst count or name |
| `MODEL` | A figure you computed from labelled inputs | Formula and inputs |
| `JUDGEMENT` | Your view, not a measurement | One-clause reason |
| `ASSUMPTION` | An input chosen without evidence because the work needs a number | Basis and sensitivity |
| `NEEDS SOURCE` | A figure the analysis needs but does not have | What was searched and what would supply it |

`NEEDS SOURCE` is a drafting label. Before delivery it is either resolved or the
claim is removed. Do not soften an unsupported claim into a hedge; a hedge reads
as knowledge to everyone downstream.

### Reader-facing wording

| Behind the claim | Write it as | Do not write |
|---|---|---|
| Two or more top-tier sources agree | A flat statement with a source note | "confirmed by multiple sources" unless true |
| One top-tier source | A flat statement naming the source | "clearly", "obviously" |
| Company claim | "the company reports", "management guides to" | The figure stated as an outcome |
| Consensus | "consensus of N analysts as of [date]" | "will", "is expected to" with no source |
| Your model | "our model implies", inputs shown | "the fair value is" with no range |
| Judgement | "we think", "our read is", with the reason | "the market is wrong" with no evidence |
| Assumption | "assuming X, then Y", with sensitivity | The figure carried into a headline unlabelled |
| Nothing | The claim does not appear | A hedged version of the claim |

Precision tracks evidence. A figure that descends from an assumption is written
to two significant figures at most. A range beats a point wherever the range is
what you actually know.

## 2. Source hierarchy

Use the hierarchy for the claim family, not one global list.

### Financials, segments and valuation

1. The filing itself: annual report, interim report, 10-K/10-Q/20-F, proxy,
   exchange announcement.
2. Regulator or exchange data: XBRL facts, filing index, ownership disclosures.
3. Company investor materials: results presentation, earnings call transcript.
   Label `COMPANY CLAIM` unless the figure is also in the filing.
4. Reputable financial press or data vendor. Label with the outlet and date.
5. Sell-side research. Label `ESTIMATE` with the vintage.
6. Social media, blogs, forums. Use only as a lead, never as the source of a
   material number.

The filing beats the deck, the deck beats a news summary. When a data vendor and
the filing disagree, the filing is the number; the vendor figure is a
normalization difference worth naming.

### Where to find primary filings

| Market | Primary source |
|---|---|
| US | SEC EDGAR: 10-K, 10-Q, 8-K, 20-F, 6-K, DEF 14A |
| Hong Kong | HKEXnews: annual/interim results, announcements, disclosure of interests |
| Mainland China | CNINFO, SSE and SZSE disclosure pages |
| UK | Companies House, LSE Regulatory News Service |
| Japan | TDnet, EDINET |
| Europe | National company registers and the issuer's IR filing page |
| Other | The exchange's disclosure page and the issuer's IR site |

Use the regulator or exchange copy when available. An IR PDF that matches the
filing is acceptable; an IR summary that omits the notes is not a substitute for
the filing.

### Market data

1. Exchange quote or a live market-data feed.
2. Official closing price from the exchange.
3. A vendor's delayed quote. Label the delay.

A price quoted inside an article dates from the article. Pull the level from a
price source, not from the article.

### Events, guidance, ownership and regulation

1. The primary document: filing, contract, docket, regulator decision, transcript.
2. The company or issuer announcement.
3. A reliable news report with outlet, time and date confidence.
4. Commentary. Label as commentary, never as the event.

### Industry size and market share

1. A regulator, trade association or audited industry database.
2. A named research house with a dated report.
3. Company investor materials. Label `COMPANY CLAIM`.
4. Press summaries. Use only with the original vintage.

## 3. Freshness and as-of

Every figure carries an **as-of** date: the moment the figure is true as of, not
the moment it was pulled. Record both when they differ.

| Data | Fresh while | Refresh on |
|---|---|---|
| Intraday price or FX | Under a minute during the session | Any statement of a current level |
| Close, market cap, price-based multiples | The trading day it was pulled | The next open |
| Consensus estimates | Seven days | The print, pre-announcement or guidance change |
| Reported financials | Until the next scheduled report | A later filing or restatement |
| Company guidance | Until the next guidance event | Any filing or call that revises it |
| Ownership and institutional holdings | The quarter it reports for | The next filing window |
| Short interest | Until the next publication | The next settlement date |
| Industry size and share | Twelve months, always with vintage | A newer study or structural change |
| News and event claims | The day | Any later development |

### Six staleness states

- `live`: inside the threshold and verified this turn.
- `current`: inside the threshold, pulled earlier this session.
- `aging`: past the threshold, usable for direction; say so beside the figure.
- `stale`: past the threshold and load-bearing; refresh it or drop the claim.
- `superseded`: a newer print, filing or revision exists; use the newer figure.
- `unknown`: the as-of cannot be established. Treat it as `NEEDS SOURCE`.

A boolean "fresh/stale" is not enough; a figure one minute past its threshold and
one two quarters past it are different problems.

## 4. Units, currency, period and share base

Put a header on the analysis before any number:

```text
Company:        [name]
Ticker:         [exchange: ticker]
Price as of:    [date, currency]
Market cap:     [value, currency, date]
Fiscal year:    [end date; 52/53-week?]
Reporting unit: [millions, billions; currency]
Share base:     [basic/diluted; weighted average/period-end]
Accounting:     [IFRS/US GAAP/other; lease convention]
```

Rules:

- Do not mix currencies. Convert at a stated rate and date, or keep the original
  currency and label it.
- Do not mix units. A figure in millions and a figure in billions in the same
  ratio is an error.
- Do not mix periods. A FY figure and a TTM figure in the same margin is an error.
- Do not mix share bases. Market cap uses shares outstanding; EPS uses diluted
  weighted-average shares. State which.
- Distinguish percentage from percentage point. A margin moving from 20% to 25%
  is +5 percentage points, or +25% relative.
- Distinguish reported, constant-currency and organic growth.
- For 52/53-week fiscal years, state the week count; do not compare a 53-week
  year with a 52-week year without adjustment.
- For acquisitions or divestitures, separate organic from inorganic growth.
- For banks and insurers, use the appropriate metrics (NIM, cost/income, CET1,
  ROE, book value), not EV/EBITDA.
- Every metric in a table or summary card carries its own period (`FY25`, `1H26`,
  `TTM`, `2026E`). The header as-of is the analysis cutoff, not the period of each
  metric. A forward P/E and a trailing margin in the same row are a period
  mismatch.

## 5. Conflict register

When two sources disagree on a material figure, do not average and do not pick
silently. Write a row:

| Claim | Source A | Source B | Selected | Why | What settles it |
|---|---|---|---|---|---|
| FY2025 revenue | 371.2 (annual report) | 372.0 (data vendor) | 371.2 | Filing beats vendor; difference is a normalization adjustment | Reconciliation note in the filing |

Two failures are invisible in the finished report: averaging two disagreeing
sources produces a third number nobody reports, and a silent pick leaves the
reader unable to tell a resolved conflict from an unnoticed one.

If both sources are the same tier and nothing settles it, carry both values and
mark the claim `NEEDS SOURCE` while drafting. If the claim is load-bearing, the
conclusion is not ready.

## 6. Arithmetic checks

Run `scripts/check_numbers.py` on a `checks.json` file before publishing. The
script compares the value used in the analysis with the value you recomputed from
the formula and prints `PASS`, `FAIL` or `SKIP`. It exits non-zero on failure or
when no checks ran.

Minimum checks for a typical company:

| Check | Formula |
|---|---|
| Market cap | price × diluted shares (or shares outstanding; state basis) |
| Enterprise value | market cap + total debt + preferred + minority interest + lease liabilities + underfunded pension - cash and non-operating investments |
| Net cash | cash + deposits + short-term investments - total debt |
| P/E | price / diluted EPS, or market cap / net profit |
| Earnings yield | 1 / P/E |
| FCF | operating cash flow - capex |
| FCF yield | FCF / EV (state if using market cap) |
| Gross margin | gross profit / revenue |
| Operating margin | operating profit / revenue |
| Net margin | net profit / revenue |
| ROE | net profit / average equity |
| ROIC | NOPAT / average invested capital |
| Revenue growth | current / prior - 1 |
| CAGR | (end / start)^(1/n) - 1 |
| Inventory days | average inventory / COGS × 365 |
| Receivables days | average receivables / revenue × 365 |
| Cash conversion | operating cash flow / net profit |
| Dividend payout | dividends / net profit, or DPS / EPS |
| Buyback yield | buyback / market cap |
| Net debt / EBITDA | net debt / EBITDA |
| Scenario probabilities | sum to 1.00 |
| Expected return | Σ(probability × return) |
| Per-share value | equity value / diluted shares |
| Bull/base/bear ordering | bull > base > bear for value and return |
| Segment sum | sum of segments = total, within the disclosed reconciliation |

For each check, state whether leases, minorities, pensions and associates are
included. Do not mix conventions.

### Common EV mistakes

- Including lease liabilities while using EBITDA that already deducts rent
  (double count). Pick one convention and state it.
- Adding minority interest to EV but forgetting to subtract it from equity value.
- Treating all cash as excess; some cash is operating.
- Ignoring underfunded pensions or environmental liabilities.
- Using book value of debt when market value is materially different.
- Using market cap of one share class when there are multiple classes.
- Adding associates or cross-holdings to EV without a consistent treatment.

### Common per-share mistakes

- Dividing by basic shares when diluted shares are materially higher.
- Ignoring options, RSUs and convertibles.
- Using period-end shares for a weighted-average metric.
- Double-counting buybacks: reducing share count and adding the cash spent back
  to equity value.
- Mixing a per-share value in one currency with a price in another.

## 7. Accounting quality

Check the cash, not just the earnings.

| Test | What to compare | Red flag |
|---|---|---|
| Cash conversion | OCF / net profit over 3-5 years | Persistently below 0.8 |
| Receivables | Receivable growth vs revenue growth | Receivables growing much faster |
| Inventory | Inventory growth vs revenue growth; inventory days | Inventory build without a demand explanation |
| Revenue quality | Reported revenue vs cash collected; deferred revenue | Revenue recognized before cash or delivery |
| One-offs | "Non-recurring" items across years | The same add-back every year |
| Capitalization | Capex vs opex; capitalized development | Routine costs moved below the line |
| SBC | SBC / revenue; diluted share growth | Rising SBC treated as non-expense |
| Leases | Lease liabilities vs lease expense | Off-balance-sheet or inconsistent treatment |
| Pensions | Funded status; discount rate | Underfunded obligation ignored |
| Related parties | Sales/purchases with related parties | Material related-party revenue |
| Auditor | Auditor changes, qualifications, restatements | Change without explanation |
| Segment reconciliation | Segment sum vs total | Unexplained "other" or elimination |

A red flag is a question, not a verdict. Investigate before concluding fraud or
quality problems.

## 8. Valuation discipline

- Use a range, not a point. Show the sensitivity to the two assumptions that
  matter most.
- Cross-check the multiple against a reverse DCF: what growth and margin does the
  current price imply?
- Compare with at least one durable peer. State why the peer is comparable and
  where the analogy breaks.
- Do not apply a terminal multiple to peak earnings. Normalize first.
- Do not double-count growth: a high growth rate and a high terminal multiple
  together are usually a sign of optimism.
- Do not add net cash to an EV-based value and then subtract debt again.
- For a company with negative earnings, use revenue/EBITDA/unit economics, not a
  meaningless P/E.
- For a cyclical, use mid-cycle margins, not the latest peak or trough.
- For a pre-revenue company, use a probability-weighted milestone approach and
  state the dilution.
- For a bank or insurer, use P/B and ROE, not EV/EBITDA.

### Scenario rules

- Probabilities sum to 1.00.
- The bear case is a real operating scenario, not a price target.
- The bull case states what has to go right, not just the upside.
- The base case is the most likely operating path, not the average of the bull
  and bear cases.
- Expected value = Σ(probability × return). Recompute it; do not estimate it.
- Include the probability of permanent capital loss, not just the expected return.
- If the expected value is attractive only because of a low-probability bull case,
  say so.

## 9. Narrative discipline

### Consensus vs variant perception

State:

- What the market currently believes (consensus).
- What you believe differently (variant perception).
- Why the market may be wrong.
- What evidence would prove you wrong.

If you cannot articulate a variant perception, the conclusion is "no edge" or
"watch", not "buy". A correct description of a great company is not an
investment thesis if the price already reflects it.

### Ticker-swap test

Read the thesis with the company name replaced by its closest competitor. If the
argument still reads as plausible, it is generic. Add company-specific evidence
or lower the confidence.

### Strongest bear case

Write the bear case as if you held it. Do not strawman it. Include:

- The single assumption that, if wrong, breaks the thesis.
- The mechanism by which the market would re-rate the stock lower.
- An estimated drawdown, not just a direction.
- The early warning that would tell you it is happening.

### Falsification

Before publishing, write:

- What would change the verdict.
- Which 2-4 metrics you will track.
- The threshold at which you would sell or revisit.
- The date of the next evidence update.

## Base rates, look-ahead and forecast accountability

### Base rates and mean reversion

- Most high growth rates and peak margins mean-revert. Use the industry's
  historical distribution, not the latest year.
- A 50% growth rate is unlikely to persist for a decade. A 30% net margin at a
  cyclical peak is not a normalized margin.
- Ask what happened to similar businesses after their peak: how many sustained
  the growth, and what was the base rate of failure?
- Use a range of outcomes; do not anchor on the last three years.
- For a company with a single product, customer or IP, look up the base rate of
  concentration-driven drawdowns, not just the growth rate.

### No look-ahead

- Use only information available as of the analysis date.
- If you use a later filing or event, label it as a subsequent event and do not
  let it contaminate the historical comparison.
- For backtests, use point-in-time data, not restated data.
- Do not assume management knew then what is known now.

### Forecast accountability

- Save the dated thesis, estimates and checks.
- On the next update, compare prior estimates with actuals and state the error.
- Classify the error: data, assumption, model or narrative.
- Update the base rate, not just the forecast. A forecast that was wrong for a
  structural reason should change the process, not only the number.

## 10. Confidence calibration

Grade the overall analysis, and the key assumptions separately.

| Grade | Meaning | Evidence standard |
|---|---|---|
| A | High confidence | Primary sources, arithmetic checked, key assumptions triangulated, thesis tested against a strong bear case |
| B | Medium confidence | Mostly primary sources, one or two unresolved estimates, one material uncertainty |
| C | Low confidence | Thin data, multiple estimates, conclusion provisional; position size should reflect it |

Put the grade in `summary.json` as `"confidence": "A"`, `"B"` or `"C"`. The card
shows it in the header.

Do not grade every sentence. Grade the conclusion and the two or three assumptions
that do the most work.

## 11. Accuracy gate

Before delivering, complete this checklist and state the outcome in the note:

```text
Accuracy gate: PASS | FAIL | VACUOUS
```

- [ ] Price as of a stated date; market cap reconciles to price × shares.
- [ ] Filing period, currency and units stated; no mixed periods or currencies.
- [ ] Share base stated: basic vs diluted, weighted average vs period-end.
- [ ] EV reconciles; leases, minorities, pensions and associates treated
      consistently.
- [ ] P/E, margins, growth, FCF and per-share values recomputed.
- [ ] Segment sum reconciles to the total, or the gap is explained.
- [ ] Scenario probabilities sum to 1; expected value recomputed; bull > base >
      bear.
- [ ] Every load-bearing claim carries an evidence label and a source/date.
- [ ] Conflicts recorded; no silent averaging.
- [ ] Missing data marked `NEEDS SOURCE` or `not disclosed`; not filled with zero.
- [ ] Strongest bear case written; drawdown estimated.
- [ ] Variant perception stated, or "no edge" acknowledged.
- [ ] Ticker-swap test passed; the thesis is company-specific.
- [ ] `check_numbers.py` ran and returned `PASS`.
- [ ] Confidence grade assigned.

`PASS` means all checks ran and passed. `FAIL` means at least one check failed;
fix the numbers or do not publish the conclusion. `VACUOUS` means the gate did not
run or had no checks; say why. An un-run gate that reports success is the failure
mode this checklist exists to prevent.

## 12. Delivery language

Use the reader-facing labels from section 1. Keep the source note close to the
number. A short note per section is enough; a citation on every cell buries the
ones that matter.

Always timestamp: price, market cap, EV, every price-based multiple, FX, consensus
figures, ownership stakes, and any sentence containing "currently", "today" or
"now".

End with:

```text
Not investment advice. Figures are as of [date] unless stated.
```
