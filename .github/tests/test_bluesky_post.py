from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from bluesky_post import prepare_message


class PrepareMessageTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.post = Path(self.directory.name) / "2026-10-24-example.md"

    def write_post(self, frontmatter, body="Post content."):
        self.post.write_text(f"---\n{frontmatter}\n---\n{body}\n", encoding="utf-8")

    def test_quoted_description_is_parsed_as_yaml(self):
        self.write_post('description: "A friend\'s visit: disc golf."\ncategory: fun')
        self.assertEqual(
            prepare_message(str(self.post)),
            "A friend's visit: disc golf. https://rawlinson.us/fun/example/#page-title",
        )

    def test_multiline_description_produces_single_line_output(self):
        self.write_post("description: |\n  First line.\n  Second line.\ncategory: fun")
        self.assertEqual(
            prepare_message(str(self.post)),
            "First line. Second line. https://rawlinson.us/fun/example/#page-title",
        )

    def test_missing_category_defaults_to_blogging(self):
        self.write_post("description: A visit.")
        self.assertEqual(
            prepare_message(str(self.post)),
            "A visit. https://rawlinson.us/blogging/example/#page-title",
        )

    def test_missing_empty_or_non_text_description_is_rejected(self):
        for frontmatter in ("title: Example", "description:", 'description: " "', "description: 123"):
            with self.subTest(frontmatter=frontmatter):
                self.write_post(frontmatter)
                with self.assertRaisesRegex(ValueError, "non-empty description is required"):
                    prepare_message(str(self.post))

    def test_description_in_body_is_not_used(self):
        self.write_post("title: Example", body="description: Not frontmatter.")
        with self.assertRaisesRegex(ValueError, "non-empty description is required"):
            prepare_message(str(self.post))

    def test_custom_message_does_not_require_description(self):
        self.write_post("category: fun")
        self.assertEqual(
            prepare_message(str(self.post), 'A "custom" message with $shell syntax.'),
            'A "custom" message with $shell syntax. https://rawlinson.us/fun/example/#page-title',
        )

    def test_missing_frontmatter_is_rejected(self):
        self.post.write_text("Post content.", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing YAML frontmatter"):
            prepare_message(str(self.post))


if __name__ == "__main__":
    unittest.main()