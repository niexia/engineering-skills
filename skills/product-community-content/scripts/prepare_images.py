#!/usr/bin/env python3
"""Export product images for X, Xiaohongshu and Reddit.

Usage:
    prepare_images.py --out DIR [--platforms x,xiaohongshu,reddit]
                      [--fit contain|cover] [--cover-title TEXT]
                      [--title-position bottom|top] [--font PATH]
                      [--json] IMAGE [IMAGE ...]

Each readable image is exported once per platform size. With --cover-title, the
first readable image additionally becomes a titled cover per platform, named from
the title so several cover languages can coexist in one output directory. Outputs
are PNG files plus manifest.json, with paths reported on stdout. The run exits 2
without writing a manifest when no image could be exported.

Requires Pillow (python3 -m pip install Pillow) and a font covering the cover
title; CJK titles need a CJK font, and the script warns when the chosen font may
lack them. SVG input is not supported; export it to PNG first.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat
except ImportError:  # pragma: no cover - environment dependent
    sys.exit("Pillow is required: python3 -m pip install Pillow")

PLATFORMS = {
    "x": (1600, 900),
    "xiaohongshu": (1080, 1440),
    "reddit": (1200, 630),
}

CJK_FONTS = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
]

LATIN_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export product images at platform sizes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("images", nargs="+", type=Path, help="source images")
    parser.add_argument("--out", required=True, type=Path, help="output directory")
    parser.add_argument(
        "--platforms",
        default=",".join(PLATFORMS),
        help="comma-separated subset of: " + ", ".join(PLATFORMS),
    )
    parser.add_argument(
        "--fit",
        choices=("contain", "cover"),
        default="contain",
        help="contain letterboxes on a derived background; cover crops",
    )
    parser.add_argument("--cover-title", help="draw this text on a cover image")
    parser.add_argument("--title-position", choices=("bottom", "top"), default="bottom")
    parser.add_argument("--font", type=Path, help="explicit TTF/TTC font path")
    parser.add_argument("--json", action="store_true", help="print the manifest")
    return parser.parse_args(argv)


def selected_platforms(value: str) -> list[str]:
    wanted = [part.strip().lower() for part in value.split(",") if part.strip()]
    unknown = [name for name in wanted if name not in PLATFORMS]
    if unknown:
        raise SystemExit(f"unknown platform(s): {', '.join(unknown)}")
    if not wanted:
        raise SystemExit("no platforms selected")
    return wanted


def slugify(text: str) -> str:
    """Return a short filename-safe label, hashed when the text has no ASCII."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:32].strip("-")
    return slug or hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def open_image(path: Path) -> Image.Image:
    image = Image.open(path)
    if getattr(image, "n_frames", 1) > 1:
        image.seek(0)
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
        canvas.alpha_composite(image)
        image = canvas
    return image.convert("RGB")


def edge_background(image: Image.Image) -> tuple[int, int, int]:
    strips = [
        image.crop((0, 0, image.width, max(1, image.height // 10))),
        image.crop((0, image.height - max(1, image.height // 10), image.width, image.height)),
        image.crop((0, 0, max(1, image.width // 10), image.height)),
        image.crop((image.width - max(1, image.width // 10), 0, image.width, image.height)),
    ]
    means = [ImageStat.Stat(strip).mean for strip in strips]
    channels = [sum(mean[index] for mean in means) / len(means) for index in range(3)]
    return tuple(int(channel * 0.35 + 255 * 0.65) for channel in channels)


def compose(
    image: Image.Image, size: tuple[int, int], fit: str
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Fit an image into a canvas and return the canvas plus the image's box."""
    width, height = size
    if fit == "cover":
        scale = max(width / image.width, height / image.height)
        resized = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        return resized.crop((left, top, left + width, top + height)), (0, 0, width, height)

    canvas = Image.new("RGB", size, edge_background(image))
    scale = min(width / image.width, height / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = (width - resized.width) // 2
    top = (height - resized.height) // 2
    canvas.paste(resized, (left, top))
    return canvas, (left, top, left + resized.width, top + resized.height)


def resize_to(image: Image.Image, size: tuple[int, int], fit: str) -> Image.Image:
    return compose(image, size, fit)[0]


def has_cjk(text: str) -> bool:
    return any(
        "\u3040" <= character <= "\u30ff"
        or "\u3400" <= character <= "\u4dbf"
        or "\u4e00" <= character <= "\u9fff"
        or "\uac00" <= character <= "\ud7af"
        for character in text
    )


def load_font(
    explicit: Path | None, size: int, text: str
) -> tuple[ImageFont.FreeTypeFont | None, str]:
    paths = [str(explicit)] if explicit else []
    paths += CJK_FONTS if has_cjk(text) else LATIN_FONTS
    if not explicit:
        paths += LATIN_FONTS if has_cjk(text) else CJK_FONTS
    for path in paths:
        try:
            return ImageFont.truetype(path, size=size), path
        except (OSError, ValueError):
            continue
    return None, ""


def wrap_lines(
    text: str, font: ImageFont.FreeTypeFont, max_width: int, limit: int
) -> list[str]:
    words = text.split()
    units = words if len(words) > 1 else list(text)
    separator = " " if len(words) > 1 else ""
    lines: list[str] = []
    current = ""
    for unit in units:
        trial = f"{current}{separator}{unit}" if current else unit
        if font.getlength(trial) <= max_width or not current:
            current = trial
            continue
        lines.append(current)
        current = unit
    if current:
        lines.append(current)
    if len(lines) > limit:
        lines = lines[:limit]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def draw_cover_title(
    canvas: Image.Image,
    text: str,
    position: str,
    font_path: Path | None,
    content_box: tuple[int, int, int, int],
) -> bool:
    width, height = canvas.size
    font_size = max(24, min(int(width * 0.055), height // 9))
    font, used_font = load_font(font_path, font_size, text)
    if font is None:
        print("warning: no usable font found; cover written without a title", file=sys.stderr)
        return False
    if has_cjk(text) and used_font not in CJK_FONTS:
        print(
            "warning: the selected font may not cover CJK characters; "
            "pass a CJK font with --font or install one",
            file=sys.stderr,
        )

    lines = wrap_lines(text.strip(), font, int(width * 0.86), 3)
    line_height = int(font_size * 1.3)
    inner_pad = max(12, int(width * 0.025))
    band_height = line_height * len(lines) + 2 * inner_pad
    room_above = content_box[1]
    room_below = height - content_box[3]
    if position == "top":
        band_top = (room_above - band_height) // 2 if room_above >= band_height else 0
    else:
        band_top = (
            content_box[3] + (room_below - band_height) // 2
            if room_below >= band_height
            else height - band_height
        )

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, band_top, width, band_top + band_height), fill=(0, 0, 0, 165))
    for index, line in enumerate(lines):
        draw.text(
            ((width - int(font.getlength(line))) // 2, band_top + inner_pad + index * line_height),
            line,
            font=font,
            fill=(255, 255, 255, 255),
        )
    canvas.paste(overlay, (0, 0), overlay)
    return True


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    platforms = selected_platforms(args.platforms)
    out_dir: Path = args.out

    manifest: list[dict] = []
    written = 0
    cover_source: Image.Image | None = None
    cover_source_path: Path | None = None

    for source in args.images:
        try:
            image = open_image(source)
        except FileNotFoundError:
            print(f"warning: missing {source}", file=sys.stderr)
            continue
        except Exception as error:  # Pillow raises several types here
            print(f"warning: cannot read {source}: {error}", file=sys.stderr)
            continue
        if cover_source is None:
            cover_source, cover_source_path = image, source

        for platform in platforms:
            size = PLATFORMS[platform]
            try:
                export = resize_to(image, size, args.fit)
            except Exception as error:
                print(f"warning: {source} -> {platform}: {error}", file=sys.stderr)
                continue
            target_dir = out_dir / platform
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / f"{source.stem}-{platform}.png"
            counter = 2
            while target.exists():
                target = target_dir / f"{source.stem}-{counter}-{platform}.png"
                counter += 1
            export.save(target, "PNG", optimize=True)
            manifest.append(
                {
                    "source": str(source),
                    "platform": platform,
                    "output": str(target),
                    "size": list(size),
                    "fit": args.fit,
                    "cover": False,
                }
            )
            written += 1

    if args.cover_title and cover_source is not None and written > 0:
        slug = slugify(args.cover_title)
        for platform in platforms:
            size = PLATFORMS[platform]
            cover, content_box = compose(cover_source, size, args.fit)
            titled = draw_cover_title(
                cover, args.cover_title, args.title_position, args.font, content_box
            )
            target_dir = out_dir / platform
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / f"cover-{slug}-{platform}.png"
            counter = 2
            while target.exists():
                target = target_dir / f"cover-{slug}-{counter}-{platform}.png"
                counter += 1
            cover.save(target, "PNG", optimize=True)
            manifest.append(
                {
                    "source": str(cover_source_path),
                    "platform": platform,
                    "output": str(target),
                    "size": list(size),
                    "fit": args.fit,
                    "cover": True,
                    "title": args.cover_title if titled else None,
                }
            )
            written += 1

    if written == 0:
        print("error: no images were exported", file=sys.stderr)
        return 2

    manifest_path = out_dir / "manifest.json"
    out_dir.mkdir(parents=True, exist_ok=True)
    merged: dict[str, dict] = {}
    if manifest_path.exists():
        try:
            for entry in json.loads(manifest_path.read_text(encoding="utf-8")):
                if isinstance(entry, dict) and "output" in entry:
                    merged[entry["output"]] = entry
        except ValueError:
            pass
    for entry in manifest:
        merged[entry["output"]] = entry
    manifest_path.write_text(
        json.dumps(list(merged.values()), indent=2) + "\n", encoding="utf-8"
    )

    if args.json:
        print(json.dumps(list(merged.values()), indent=2))
    else:
        for entry in manifest:
            width, height = entry["size"]
            print(f"{entry['platform']:<12} {width}x{height}  {entry['output']}")
        print(f"manifest: {manifest_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
