import argparse
from pathlib import Path
import re
import sys
from typing import Sequence
from urllib.parse import urlparse

from PIL import Image, ImageOps
import yaml


SITE_HOST = "rawlinson.us"
MAX_SOCIAL_DIMENSION = 1200
MIN_SOCIAL_DIMENSION = 640
JPEG_QUALITIES = (88, 82, 76, 70, 64)


def _frontmatter_bounds(text: str) -> tuple[int, int]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return 0, index
    raise ValueError("missing YAML frontmatter terminator")


def _load_frontmatter(post_path: Path) -> tuple[str, dict, int, int]:
    text = post_path.read_text(encoding="utf-8")
    start, end = _frontmatter_bounds(text)
    lines = text.splitlines(keepends=True)
    frontmatter_text = "".join(lines[start + 1 : end])
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter must be a mapping")
    return text, frontmatter, start, end


def _resolve_image_path(image_reference: str, repository_root: Path) -> Path:
    parsed = urlparse(image_reference)
    if parsed.scheme:
        if parsed.scheme != "https" or parsed.netloc != SITE_HOST:
            raise ValueError(f"unsupported image URL: {image_reference}")
        relative = parsed.path.lstrip("/")
    elif image_reference.startswith("/"):
        relative = image_reference.lstrip("/")
    else:
        raise ValueError(f"unsupported image URL: {image_reference}")

    image_path = (repository_root / relative).resolve()
    root = repository_root.resolve()
    try:
        image_path.relative_to(root)
    except ValueError as error:
        raise ValueError(f"image URL escapes repository: {image_reference}") from error
    if not image_path.is_file():
        raise ValueError(f"image file does not exist: {image_reference}")
    return image_path


def _social_dimensions(image: Image.Image) -> list[tuple[int, int]]:
    scale = min(1, MAX_SOCIAL_DIMENSION / max(image.size))
    width = max(1, round(image.width * scale))
    height = max(1, round(image.height * scale))
    dimensions = []
    while max(width, height) >= MIN_SOCIAL_DIMENSION:
        dimensions.append((width, height))
        width = round(width * 0.85)
        height = round(height * 0.85)
    return dimensions


def _write_social_image(image_path: Path, threshold: int) -> Path:
    output_base = image_path.with_name(f"{image_path.stem}-social")
    with Image.open(image_path) as source:
        source.load()
        dimensions = _social_dimensions(source)
        if not dimensions:
            raise ValueError(f"image is too small to create a social derivative: {image_path}")

        for width, height in dimensions:
            resized = source.resize((width, height), Image.Resampling.LANCZOS)
            png_path = output_base.with_suffix(".png")
            temporary_path = png_path.with_suffix(".png.tmp")
            resized.save(temporary_path, format="PNG", optimize=True)
            if temporary_path.stat().st_size <= threshold:
                temporary_path.replace(png_path)
                return png_path
            temporary_path.unlink()

        jpeg_path = output_base.with_suffix(".jpg")
        temporary_path = jpeg_path.with_suffix(".jpg.tmp")
        for width, height in reversed(dimensions):
            resized = source.resize((width, height), Image.Resampling.LANCZOS)
            rgb_image = ImageOps.exif_transpose(resized).convert("RGBA")
            background = Image.new("RGB", rgb_image.size, "white")
            background.paste(rgb_image, mask=rgb_image.getchannel("A"))
            for quality in JPEG_QUALITIES:
                background.save(
                    temporary_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                    progressive=True,
                )
                if temporary_path.stat().st_size <= threshold:
                    temporary_path.replace(jpeg_path)
                    return jpeg_path
        if temporary_path.exists():
            temporary_path.unlink()
    raise ValueError(f"could not create a social image under {threshold} bytes: {image_path}")


def _update_og_image(text: str, start: int, end: int, image_reference: str) -> str:
    lines = text.splitlines(keepends=True)
    header_index = None
    for index in range(start + 1, end):
        if re.match(r"^header:\s*$", lines[index]):
            header_index = index
            break
    if header_index is None:
        raise ValueError("frontmatter header mapping is required")

    for index in range(header_index + 1, end):
        if re.match(r"^[A-Za-z0-9_-]+:", lines[index]):
            break
        match = re.match(r"^(\s+og_image:\s*).*$", lines[index])
        if match:
            newline = "\n" if lines[index].endswith("\n") else ""
            lines[index] = f"{match.group(1)}{image_reference}{newline}"
            return "".join(lines)
    raise ValueError("frontmatter header.og_image is required")


def process_post(post_path: Path, repository_root: Path, threshold: int = 1_000_000) -> bool:
    repository_root = repository_root.resolve()
    text, frontmatter, start, end = _load_frontmatter(post_path)
    header = frontmatter.get("header")
    if not isinstance(header, dict) or not isinstance(header.get("og_image"), str):
        raise ValueError("frontmatter header.og_image is required")
    image_reference = header["og_image"]
    image_path = _resolve_image_path(image_reference, repository_root)
    if image_path.stat().st_size <= threshold:
        return False

    social_path = _write_social_image(image_path, threshold)
    relative_social_path = "/" + social_path.relative_to(repository_root).as_posix()
    updated_text = _update_og_image(text, start, end, relative_social_path)
    post_path.write_text(updated_text, encoding="utf-8")
    return True


def process_posts(
    post_paths: Sequence[Path], repository_root: Path, threshold: int = 1_000_000
) -> int:
    changed = 0
    for post_path in post_paths:
        if process_post(post_path, repository_root, threshold):
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare small Bluesky social images.")
    parser.add_argument("posts", nargs="+", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        changed = process_posts(args.posts, args.repository_root.resolve())
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Error preparing social images: {error}", file=sys.stderr)
        return 1
    print(f"Prepared social images for {changed} post(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
