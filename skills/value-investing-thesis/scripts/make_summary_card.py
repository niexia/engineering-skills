#!/usr/bin/env python3
"""Render a one-page value-investing summary card from JSON.

Usage:
    python make_summary_card.py summary.json --out summary.png
    python make_summary_card.py summary.json --out summary.svg --format svg

PNG output requires Pillow. When Pillow is unavailable, the script writes an SVG
fallback and prints a warning instead of failing.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont

    HAVE_PIL = True
except Exception:  # pragma: no cover - exercised only without Pillow
    HAVE_PIL = False

W, H = 1600, 2280
M = 80

BG = "#F5F1E8"
CARD = "#FFFCF5"
INK = "#1B2A2A"
MUTED = "#6E7C79"
LINE = "#D8D0BF"
GREEN = "#1E6B57"
RED = "#A23B3B"
GOLD = "#A97B22"
WHITE = "#FFFFFF"
BAR_BG = "#E6DFD1"

VERDICT_COLORS = {"BUY": GREEN, "WATCH": GOLD, "PASS": RED}
LAYER_COLORS = [GREEN, GOLD, RED]

FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

LABELS = {
    "en": {
        "kicker": "VALUE INVESTING THESIS",
        "scorecard": "Five-dimension scorecard",
        "score_hint": "5 = best",
        "metrics": "Key metrics",
        "layers": "Three layers of truth",
        "bull": "Bull case",
        "bear": "Bear case",
        "lenses": "Three lenses",
        "decision": "Decision",
        "buy": "Buy zone",
        "watch": "Watch zone",
        "avoid": "Avoid",
        "position": "Position",
        "expected": "Expected return",
        "not_advice": "Not investment advice.",
        "verdict": {"BUY": "BUY", "WATCH": "WATCH", "PASS": "PASS"},
        "scores": {
            "business": "Business quality",
            "moat": "Moat",
            "management": "Management",
            "valuation": "Valuation",
            "risk": "Risk",
        },
    },
    "zh": {
        "kicker": "价值投资论点",
        "scorecard": "五维评分",
        "score_hint": "5 = 最好",
        "metrics": "关键数据",
        "layers": "三层真相",
        "bull": "多头逻辑",
        "bear": "空头逻辑",
        "lenses": "三面镜子",
        "decision": "决策",
        "buy": "买入区",
        "watch": "观察区",
        "avoid": "回避",
        "position": "仓位",
        "expected": "预期回报",
        "not_advice": "不构成投资建议。",
        "verdict": {"BUY": "买入", "WATCH": "观察", "PASS": "回避"},
        "scores": {
            "business": "生意质量",
            "moat": "护城河",
            "management": "管理层",
            "valuation": "估值",
            "risk": "风险",
        },
    },
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def require(data: dict[str, Any], key: str) -> Any:
    if key not in data or data[key] in (None, "", [], {}):
        fail(f"missing required field: {key}")
    return data[key]


def validate(data: dict[str, Any]) -> None:
    for key in ("company", "ticker", "as_of", "verdict", "verdict_line", "scores", "metrics", "layers", "bull", "bear", "lenses", "decision"):
        require(data, key)
    if data["verdict"] not in VERDICT_COLORS:
        fail("verdict must be one of BUY, WATCH or PASS")
    scores = data["scores"]
    for key in ("business", "moat", "management", "valuation", "risk"):
        if key not in scores:
            fail(f"missing score: {key}")
        try:
            value = int(scores[key])
        except (TypeError, ValueError):
            fail(f"score {key} must be an integer from 1 to 5")
        if not 1 <= value <= 5:
            fail(f"score {key} must be between 1 and 5")
    if len(data["layers"]) != 3:
        fail("layers must contain exactly three items")
    if not 1 <= len(data["metrics"]) <= 6:
        fail("metrics must contain between one and six items")
    if not 1 <= len(data["bull"]) <= 3:
        fail("bull must contain between one and three items")
    if not 1 <= len(data["bear"]) <= 3:
        fail("bear must contain between one and three items")
    for key in ("buffett", "duan", "munger"):
        if key not in data["lenses"]:
            fail(f"missing lens: {key}")


def find_font(explicit: str | None = None) -> str | None:
    candidates = [explicit, os.environ.get("SUMMARY_CARD_FONT"), *FONT_CANDIDATES]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if not path.is_file():
            continue
        try:
            ImageFont.truetype(str(path), 24, index=0)
            return str(path)
        except Exception:
            continue
    return None


class FontBook:
    def __init__(self, path: str | None) -> None:
        self.path = path
        self.cache: dict[int, Any] = {}

    def get(self, size: int) -> Any:
        if size not in self.cache:
            if self.path:
                self.cache[size] = ImageFont.truetype(self.path, size, index=0)
            else:
                self.cache[size] = ImageFont.load_default()
        return self.cache[size]


def is_cjk(ch: str) -> bool:
    code = ord(ch)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0xF900 <= code <= 0xFAFF
    )


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    buf = ""
    for ch in text:
        if ch == "\n":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append("\n")
        elif ch == " ":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(" ")
        elif is_cjk(ch) or ch in "，。；：！？、（）【】《》“”‘’—…·":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(ch)
        else:
            buf += ch
    if buf:
        tokens.append(buf)
    return tokens


def wrap_text(draw: Any, text: str, font: Any, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for token in tokenize(text):
        if token == "\n":
            lines.append(current.rstrip())
            current = ""
            continue
        if token == " ":
            if current and not current.endswith(" "):
                current += " "
            continue
        candidate = current + token
        if not current.strip() or draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current.rstrip())
            current = token
    if current.strip():
        lines.append(current.rstrip())
    return lines or [""]


def fit_text(
    draw: Any,
    text: str,
    fonts: FontBook,
    max_width: int,
    max_height: int,
    base: int,
    minimum: int,
    ratio: float = 1.35,
) -> tuple[Any, list[str], int]:
    for size in range(base, minimum - 1, -1):
        font = fonts.get(size)
        lines = wrap_text(draw, text, font, max_width)
        line_height = int(size * ratio)
        if len(lines) * line_height <= max_height:
            return font, lines, line_height
    font = fonts.get(minimum)
    lines = wrap_text(draw, text, font, max_width)
    return font, lines, int(minimum * ratio)


def draw_lines(draw: Any, x: int, y: int, lines: list[str], font: Any, fill: str, line_height: int) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)


def panel(draw: Any, box: tuple[int, int, int, int], fill: str = CARD, outline: str = LINE, radius: int = 24) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def draw_header(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    draw.text((M, 62), labels["kicker"], font=fonts.get(22), fill=GOLD)
    font, lines, line_height = fit_text(draw, str(data["company"]), fonts, 1000, 78, 66, 42)
    draw_lines(draw, M, 100, lines, font, INK, line_height)

    meta = [str(data["ticker"])]
    if data.get("market"):
        meta.append(str(data["market"]))
    meta.append(str(data["as_of"]))
    if data.get("price"):
        price = f'{data["price"]} {data.get("currency", "")}'.strip()
        meta.append(price)
    if data.get("market_cap"):
        meta.append(str(data["market_cap"]))
    draw.text((M, 194), "  ·  ".join(meta), font=fonts.get(24), fill=MUTED)

    verdict = str(data["verdict"]).upper()
    verdict_label = labels["verdict"][verdict]
    verdict_font = fonts.get(30)
    text_width = int(draw.textlength(verdict_label, font=verdict_font))
    pill_width = max(180, text_width + 80)
    pill_x = W - M - pill_width
    draw.rounded_rectangle(
        (pill_x, 92, pill_x + pill_width, 160),
        radius=34,
        fill=VERDICT_COLORS[verdict],
    )
    draw.text(
        (pill_x + pill_width / 2, 126),
        verdict_label,
        font=verdict_font,
        fill=WHITE,
        anchor="mm",
    )

    font, lines, line_height = fit_text(draw, str(data["verdict_line"]), fonts, W - 2 * M, 72, 30, 22)
    draw_lines(draw, M, 242, lines, font, INK, line_height)


def draw_scorecard(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    panel(draw, (M, 370, W - M, 700))
    draw.text((M + 30, 394), labels["scorecard"], font=fonts.get(28), fill=INK)
    draw.text((W - M - 30, 400), labels["score_hint"], font=fonts.get(20), fill=MUTED, anchor="ra")

    order = ["business", "moat", "management", "valuation", "risk"]
    y = 446
    for key in order:
        score = int(data["scores"][key])
        draw.text((M + 30, y), labels["scores"][key], font=fonts.get(25), fill=INK)
        bar_x, bar_y, bar_w, bar_h = M + 330, y + 7, 820, 16
        draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=8, fill=BAR_BG)
        fill_width = int(bar_w * score / 5)
        if fill_width > 0:
            color = GREEN if score >= 4 else GOLD if score == 3 else RED
            draw.rounded_rectangle(
                (bar_x, bar_y, bar_x + fill_width, bar_y + bar_h),
                radius=8,
                fill=color,
            )
        draw.text((bar_x + bar_w + 20, y - 2), f"{score}/5", font=fonts.get(22), fill=MUTED)
        y += 48

    average = sum(int(data["scores"][key]) for key in order) / 5
    draw.text((W - M - 30, 658), f"{average:.1f} / 5", font=fonts.get(24), fill=GOLD, anchor="ra")


def draw_metrics(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    panel(draw, (M, 730, W - M, 960))
    draw.text((M + 30, 754), labels["metrics"], font=fonts.get(28), fill=INK)
    metrics = list(data["metrics"])[:6]
    columns = 3
    cell_width = (W - 2 * M - 60) // columns
    for index, metric in enumerate(metrics):
        column = index % columns
        row = index // columns
        x = M + 30 + column * cell_width
        y = 804 + row * 70
        draw.text((x, y), str(metric.get("label", "")), font=fonts.get(20), fill=MUTED)
        font, lines, line_height = fit_text(draw, str(metric.get("value", "")), fonts, cell_width - 20, 38, 30, 20)
        draw_lines(draw, x, y + 24, lines, font, INK, line_height)


def draw_layers(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    panel(draw, (M, 990, W - M, 1320))
    draw.text((M + 30, 1014), labels["layers"], font=fonts.get(28), fill=INK)
    y = 1064
    for index, layer in enumerate(data["layers"][:3]):
        tag = str(layer.get("label", ""))
        tag_font = fonts.get(20)
        tag_width = max(180, int(draw.textlength(tag, font=tag_font)) + 40)
        draw.rounded_rectangle(
            (M + 30, y, M + 30 + tag_width, y + 38),
            radius=19,
            fill=LAYER_COLORS[index],
        )
        draw.text(
            (M + 30 + tag_width / 2, y + 19),
            tag,
            font=tag_font,
            fill=WHITE,
            anchor="mm",
        )
        text_x = M + 30 + tag_width + 25
        font, lines, line_height = fit_text(
            draw,
            str(layer.get("text", "")),
            fonts,
            W - 2 * M - 60 - tag_width - 25,
            62,
            23,
            18,
        )
        draw_lines(draw, text_x, y + 7, lines, font, INK, line_height)
        y += 82


def draw_case(
    draw: Any,
    box: tuple[int, int, int, int],
    title: str,
    items: list[Any],
    color: str,
    fonts: FontBook,
) -> None:
    panel(draw, box)
    draw.text((box[0] + 28, box[1] + 22), title, font=fonts.get(26), fill=color)
    y = box[1] + 70
    for item in list(items)[:3]:
        draw.ellipse((box[0] + 30, y + 10, box[0] + 40, y + 20), fill=color)
        font, lines, line_height = fit_text(
            draw,
            str(item),
            fonts,
            box[2] - box[0] - 80,
            80,
            22,
            17,
        )
        draw_lines(draw, box[0] + 52, y, lines, font, INK, line_height)
        y += max(78, len(lines) * line_height + 12)


def draw_lenses(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    panel(draw, (M, 1720, W - M, 1960))
    draw.text((M + 30, 1744), labels["lenses"], font=fonts.get(28), fill=INK)
    rows = [("Buffett", "buffett", GREEN), ("Duan", "duan", GOLD), ("Munger", "munger", RED)]
    y = 1790
    for label, key, color in rows:
        draw.text((M + 30, y), label, font=fonts.get(21), fill=color)
        font, lines, line_height = fit_text(
            draw,
            str(data["lenses"].get(key, "")),
            fonts,
            W - 2 * M - 220,
            52,
            21,
            16,
        )
        draw_lines(draw, M + 190, y - 2, lines, font, INK, line_height)
        y += 56


def draw_decision(draw: Any, data: dict[str, Any], labels: dict[str, Any], fonts: FontBook) -> None:
    panel(draw, (M, 1990, W - M, 2160), fill="#1E2B2A", outline="#1E2B2A")
    draw.text((M + 30, 2008), labels["decision"], font=fonts.get(24), fill=GOLD)
    expected = data["decision"].get("expected_return", "")
    if expected:
        draw.text(
            (W - M - 30, 2010),
            f"{labels['expected']}: {expected}",
            font=fonts.get(20),
            fill=GOLD,
            anchor="ra",
        )
    cells = [
        (labels["buy"], data["decision"].get("buy_zone", "n/a")),
        (labels["watch"], data["decision"].get("watch_zone", "n/a")),
        (labels["avoid"], data["decision"].get("avoid_zone", "n/a")),
        (labels["position"], data["decision"].get("position", "n/a")),
    ]
    x = M + 30
    cell_width = (W - 2 * M - 60) // 4
    for label, value in cells:
        draw.text((x, 2048), label, font=fonts.get(18), fill="#A8B5AF")
        font, lines, line_height = fit_text(draw, str(value), fonts, cell_width - 20, 50, 26, 18)
        draw_lines(draw, x, 2074, lines, font, WHITE, line_height)
        x += cell_width


def compose_footer(labels: dict[str, Any], data: dict[str, Any]) -> str:
    extra = str(data.get("footer", "")).strip()
    disclaimer = labels["not_advice"].rstrip("。.")
    if extra and (disclaimer.lower() in extra.lower() or "not investment advice" in extra.lower()):
        return extra
    if extra:
        return f"{labels['not_advice']}  {extra}"
    return labels["not_advice"]


def render_png(data: dict[str, Any], labels: dict[str, Any], out_path: Path, font_path: str | None) -> None:
    fonts = FontBook(font_path)
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, W, 6), fill=GOLD)
    draw_header(draw, data, labels, fonts)
    draw.line((M, 338, W - M, 338), fill=LINE, width=2)
    draw_scorecard(draw, data, labels, fonts)
    draw_metrics(draw, data, labels, fonts)
    draw_layers(draw, data, labels, fonts)
    draw_case(draw, (M, 1350, 780, 1688), labels["bull"], list(data["bull"]), GREEN, fonts)
    draw_case(draw, (820, 1350, W - M, 1688), labels["bear"], list(data["bear"]), RED, fonts)
    draw_lenses(draw, data, labels, fonts)
    draw_decision(draw, data, labels, fonts)

    footer = compose_footer(labels, data)
    font, lines, line_height = fit_text(draw, footer, fonts, W - 2 * M, 50, 18, 14)
    draw_lines(draw, M, 2200, lines, font, MUTED, line_height)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path} ({W}x{H} PNG)")


def svg_visual_width(text: str, size: int) -> float:
    width = 0.0
    for ch in text:
        if is_cjk(ch):
            width += size
        elif ch == " ":
            width += size * 0.3
        else:
            width += size * 0.55
    return width


def svg_wrap(text: str, max_width: int, size: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        if not current or svg_visual_width(current + ch, size) <= max_width:
            current += ch
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines or [""]


def render_svg(data: dict[str, Any], labels: dict[str, Any], out_path: Path) -> None:
    font_family = "'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif"
    parts: list[str] = []
    y = 90

    def text(value: str, size: int, fill: str, weight: str = "normal", width: int = W - 2 * M) -> None:
        nonlocal y
        for line in svg_wrap(str(value), width, size):
            parts.append(
                f'<text x="{M}" y="{y}" font-family="{font_family}" '
                f'font-size="{size}" font-weight="{weight}" fill="{fill}">{html.escape(line)}</text>'
            )
            y += int(size * 1.4)

    text(labels["kicker"], 22, GOLD, "bold")
    y += 10
    text(data["company"], 60, INK, "bold")
    meta = [str(data["ticker"])]
    if data.get("market"):
        meta.append(str(data["market"]))
    meta.append(str(data["as_of"]))
    if data.get("price"):
        meta.append(f'{data["price"]} {data.get("currency", "")}'.strip())
    if data.get("market_cap"):
        meta.append(str(data["market_cap"]))
    text(" · ".join(meta), 24, MUTED)
    y += 8
    text(f'{labels["verdict"][data["verdict"]]} — {data["verdict_line"]}', 30, VERDICT_COLORS[data["verdict"]], "bold")
    y += 30

    def section(title: str) -> None:
        nonlocal y
        parts.append(f'<text x="{M}" y="{y}" font-family="{font_family}" font-size="28" font-weight="bold" fill="{INK}">{html.escape(title)}</text>')
        y += 44

    def rule() -> None:
        nonlocal y
        parts.append(f'<line x1="{M}" y1="{y}" x2="{W - M}" y2="{y}" stroke="{LINE}" stroke-width="2"/>')
        y += 36

    section(labels["scorecard"])
    for key in ("business", "moat", "management", "valuation", "risk"):
        score = int(data["scores"][key])
        text(f'{labels["scores"][key]}: {score}/5', 24, INK)
    y += 8
    rule()

    section(labels["metrics"])
    for metric in list(data["metrics"])[:6]:
        text(f'{metric.get("label", "")}: {metric.get("value", "")}', 24, INK)
    y += 8
    rule()

    section(labels["layers"])
    for layer in data["layers"]:
        text(f'{layer.get("label", "")}: {layer.get("text", "")}', 24, INK)
    y += 8
    rule()

    section(labels["bull"])
    for item in data["bull"]:
        text(f'• {item}', 24, GREEN)
    y += 8
    section(labels["bear"])
    for item in data["bear"]:
        text(f'• {item}', 24, RED)
    y += 8
    rule()

    section(labels["lenses"])
    for label, key in (("Buffett", "buffett"), ("Duan", "duan"), ("Munger", "munger")):
        text(f'{label}: {data["lenses"].get(key, "")}', 24, INK)
    y += 8
    rule()

    section(labels["decision"])
    text(f'{labels["buy"]}: {data["decision"].get("buy_zone", "n/a")}', 24, INK)
    text(f'{labels["watch"]}: {data["decision"].get("watch_zone", "n/a")}', 24, INK)
    text(f'{labels["avoid"]}: {data["decision"].get("avoid_zone", "n/a")}', 24, INK)
    text(f'{labels["position"]}: {data["decision"].get("position", "n/a")}', 24, INK)
    if data["decision"].get("expected_return"):
        text(f'{labels["expected"]}: {data["decision"]["expected_return"]}', 24, GOLD)
    y += 20

    footer = compose_footer(labels, data)
    text(footer, 18, MUTED)

    height = y + 50
    parts.insert(
        0,
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}">',
    )
    parts.insert(1, f'<rect x="0" y="0" width="{W}" height="{height}" fill="{BG}"/>')
    parts.insert(2, f'<rect x="0" y="0" width="{W}" height="6" fill="{GOLD}"/>')
    parts.append("</svg>")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out_path} ({W}x{height} SVG fallback)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a value-investing summary card from JSON.")
    parser.add_argument("input", type=Path, help="Path to summary.json")
    parser.add_argument("--out", type=Path, default=Path("summary.png"), help="Output image path")
    parser.add_argument("--format", choices=("png", "svg"), default=None, help="Force an output format")
    parser.add_argument("--font", default=None, help="Path to a TTF/TTC font, preferably with CJK glyphs")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"input not found: {args.input}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail("input must be a JSON object")

    validate(data)
    locale = str(data.get("locale", "en")).lower()
    labels = LABELS.get(locale, LABELS["en"])

    output_format = args.format
    if output_format is None:
        output_format = "svg" if args.out.suffix.lower() == ".svg" else "png"

    if output_format == "svg" or not HAVE_PIL:
        if output_format == "png":
            print("warning: Pillow is unavailable; writing an SVG fallback instead", file=sys.stderr)
        render_svg(data, labels, args.out)
        return

    font_path = find_font(args.font)
    if not font_path:
        print("warning: no TrueType font found; Chinese text may render as boxes", file=sys.stderr)
    render_png(data, labels, args.out, font_path)


if __name__ == "__main__":
    main()
