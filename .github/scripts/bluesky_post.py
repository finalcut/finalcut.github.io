import os
from pathlib import Path
import re
import sys

import yaml


def prepare_message(post_file: str, custom_message: str = "") -> str:
    post_path = Path(post_file)
    lines = post_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError(f"{post_file}: missing YAML frontmatter")

    frontmatter = yaml.safe_load("\n".join(lines[1:lines.index("---", 1)]))
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{post_file}: frontmatter must be a mapping")

    description = custom_message or frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{post_file}: a non-empty description is required")

    category = frontmatter.get("category") or "blogging"
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post_path.stem)
    post_url = f"https://rawlinson.us/{category}/{slug}/#page-title"
    blurb = " ".join(description.split())
    return f"{blurb} {post_url}"


def main() -> int:
    try:
        post_file = os.environ["POST_FILE"]
        message = prepare_message(post_file, os.environ.get("CUSTOM_MESSAGE", ""))
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
            output.write(f"MESSAGE={message}\n")
            output.write(f"BLUESKY_TEXT={message}\n")
            output.write(f"POST_FILE={post_file}\n")
        print(f"Generated message: {message}")
    except (KeyError, OSError, ValueError, yaml.YAMLError) as error:
        print(f"Error preparing Bluesky message: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())