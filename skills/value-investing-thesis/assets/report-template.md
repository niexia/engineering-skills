# [Company] — Value Investing Thesis

**As of:** [YYYY-MM-DD]
**Price:** [value, currency, as-of date]
**Market cap:** [value, currency]
**Enterprise value:** [value, currency]
**Fiscal year:** [end date; 52/53-week?]
**Reporting unit:** [millions/billions; currency]
**Share base:** [basic/diluted; weighted average/period-end]
**Accounting:** [IFRS/US GAAP/other; lease convention]
**Verdict:** BUY / WATCH / PASS
**Confidence:** A / B / C
**Accuracy gate:** PASS / FAIL / VACUOUS

> Not investment advice. Figures are as of the date stated unless otherwise noted.

## 1. Bottom line

[One paragraph: what the business is, what the market is paying for, what you
believe differently, and why the verdict follows. Lead with the verdict and the
one reason that matters.]

## 2. Fact base and provenance

| Metric | Value | Period | Source | Label | Confidence |
|---|---:|---|---|---|---|
| Revenue | | | | FACT / COMPANY CLAIM / ESTIMATE / MODEL | A/B/C |
| Gross margin | | | | | |
| Operating margin | | | | | |
| Net profit | | | | | |
| Operating cash flow | | | | | |
| Capex | | | | | |
| Net cash / debt | | | | | |
| Inventory days | | | | | |
| Receivables days | | | | | |
| ROE / ROIC | | | | | |
| Segment mix | | | | | |
| Geographic mix | | | | | |
| Customer / IP concentration | | | | | |
| Management ownership | | | | | |
| Buybacks / dividends | | | | | |

**Data gaps:** [What is missing, what was searched, and what would supply it.]

**Conflict register:** [If two sources disagree, show both and why one was
selected. If none, write "none".]

## 3. Business model and three-layer truth

[How the company earns cash, in one paragraph. Revenue drivers: volume, price,
mix, geography, channel. Unit economics.]

| Layer | What belongs here | Current direction | Evidence |
|---|---|---|---|
| Stable core | Repeat demand, installed base, membership, essential use cases | Growing / flat / shrinking | |
| Cyclical layer | Restocking, macro, fashion, promotions, inventory cycle, FX | | |
| Bubble layer | Speculation, resale premia, one-off events, channel stuffing, pull-forward | | |

## 4. Three lenses

### Buffett

- Circle of competence:
- Moat (source, width, evidence):
- Owner earnings and returns on capital:
- Management and capital allocation:
- Margin of safety:

### Duan Yongping

- 买股票就是买公司:
- 生意模式 (差异化, 定价权, 用户需求, 现金流):
- 企业文化 (本分, 平常心, stop doing list):
- 毛估估:
- 机会成本:

### Munger

- Inversion: what would kill this investment?
- Psychology and incentives:
- Too hard? If yes, say so.
- 100% buy test:
- Opportunity cost:

### Scores

| Dimension | Score (1-5) | Evidence for | Evidence against |
|---|---:|---|---|
| Business quality | | | |
| Moat | | | |
| Management | | | |
| Valuation | | | |
| Risk | | | |

## 5. Normalized earnings bridge

| Line | Value | Label | Note |
|---|---:|---|---|
| Reported net profit | | FACT | |
| One-off gains/losses | | MODEL | |
| FX gains/losses | | MODEL | |
| Stock-based compensation | | MODEL | |
| Inventory write-downs / restructuring | | MODEL | |
| Excess margin from a temporary boom | | MODEL | |
| Maintenance capex | | MODEL | |
| Working-capital normalization | | MODEL | |
| **Normalized owner earnings** | | MODEL | Low / base / high range |

## 6. Valuation scenarios

| Case | Revenue | Margin | Net profit | Multiple | Equity value | Per share | Return | Probability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bear | | | | | | | | |
| Base | | | | | | | | |
| Bull | | | | | | | | |

**Expected return:** [Σ probability × return, recomputed]
**Reverse DCF:** [What growth and margin does the current price imply?]
**Peer comparison:** [At least one durable peer; why comparable, where the analogy
breaks.]
**What is priced in:** [Consensus view.]
**Variant perception:** [What you believe differently and why.]
**Why the market may be wrong:** [Evidence.]
**What would prove you wrong:** [Falsification conditions.]

## 7. Pre-mortem and risks

| Risk | Probability | Impact | Early warning | Response |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

**Worst realistic drawdown:** [Estimate, with the mechanism.]
**Permanent capital loss risk:** [What would make it permanent.]

## 8. Decision and rules

- Verdict:
- Buy zone:
- Watch zone:
- Avoid zone:
- Position suitability: Core / Satellite / Option / Avoid
- Position size:
- Expected return at the buy zone:
- Sell rules:
- What would change the verdict:
- Next evidence update: [date / event]

## 9. Tracking checklist

1. [Metric, threshold, date]
2. [Metric, threshold, date]
3. [Metric, threshold, date]
4. [Metric, threshold, date]

## 10. Accuracy gate

- [ ] Price and market cap reconcile.
- [ ] Period, currency, unit and share base are stated and consistent.
- [ ] EV reconciles; leases, minorities, pensions and associates are consistent.
- [ ] P/E, margins, growth, FCF and per-share values recomputed.
- [ ] Segment sum reconciles or the gap is explained.
- [ ] Scenario probabilities sum to 1; expected value recomputed; bull > base > bear.
- [ ] Every load-bearing claim has an evidence label and a source/date.
- [ ] Conflicts recorded; no silent averaging.
- [ ] Missing data marked; not filled with zero.
- [ ] Strongest bear case and drawdown estimated.
- [ ] Variant perception stated, or "no edge" acknowledged.
- [ ] Ticker-swap test passed.
- [ ] `check_numbers.py` result: PASS / FAIL / VACUOUS.
- [ ] Confidence grade assigned.

```text
Accuracy gate: PASS | FAIL | VACUOUS
```
