from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from prepare_social_images import process_post


class PrepareSocialImagesTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.asset_dir = self.root / "assets" / "images"
        self.asset_dir.mkdir(parents=True)
        self.post = self.root / "_posts" / "2026-11-23-example.md"
        self.post.parent.mkdir()

    def write_post(self, og_image, header_image=None):
        header_image = header_image or og_image
        self.post.write_text(
            "---\n"
            "title: Example\n"
            "header:\n"
            f"  image: {header_image}\n"
            f"  og_image: {og_image}\n"
            "---\n"
            "Post content.\n",
            encoding="utf-8",
        )

    def write_noise_image(self, name, size=(1482, 1112), mode="RGBA"):
        image_path = self.asset_dir / name
        image = Image.effect_noise(size, 128).convert(mode)
        image.save(image_path, format="PNG")
        return image_path

    def test_small_og_image_is_unchanged(self):
        image_path = self.write_noise_image("photo.png", size=(40, 40))
        self.write_post("/assets/images/photo.png")
        original = self.post.read_text(encoding="utf-8")

        changed = process_post(self.post, self.root)

        self.assertFalse(changed)
        self.assertEqual(self.post.read_text(encoding="utf-8"), original)
        self.assertFalse((image_path.parent / "photo-social.png").exists())

    def test_oversized_png_creates_small_png_and_updates_only_og_image(self):
        self.write_noise_image("photo.png", mode="RGB")
        self.write_post(
            "/assets/images/photo.png",
            header_image="/assets/images/photo.png",
        )

        changed = process_post(self.post, self.root)

        social_image = self.asset_dir / "photo-social.png"
        self.assertTrue(changed)
        self.assertLess(social_image.stat().st_size, 1_000_000)
        content = self.post.read_text(encoding="utf-8")
        self.assertIn("og_image: /assets/images/photo-social.png", content)
        self.assertIn("image: /assets/images/photo.png", content)

    def test_png_falls_back_to_jpeg_when_png_cannot_meet_size_target(self):
        self.write_noise_image("photo.png")
        self.write_post("/assets/images/photo.png")

        process_post(self.post, self.root, threshold=250_000)

        social_image = self.asset_dir / "photo-social.jpg"
        self.assertLess(social_image.stat().st_size, 250_000)
        self.assertIn("og_image: /assets/images/photo-social.jpg", self.post.read_text())
        self.assertFalse((self.asset_dir / "photo-social.png").exists())

    def test_jpeg_fallback_keeps_largest_candidate_under_threshold(self):
        self.write_noise_image("photo.png")
        self.write_post("/assets/images/photo.png")

        process_post(self.post, self.root, threshold=500_000)

        with Image.open(self.asset_dir / "photo-social.jpg") as social_image:
            self.assertEqual(social_image.size, (1200, 900))

    def test_absolute_site_url_resolves(self):
        self.write_noise_image("photo.png", size=(40, 40))
        self.write_post("https://rawlinson.us/assets/images/photo.png")

        self.assertFalse(process_post(self.post, self.root))

    def test_external_url_is_rejected(self):
        self.write_post("https://example.com/photo.png")

        with self.assertRaisesRegex(ValueError, "unsupported image URL"):
            process_post(self.post, self.root)

    def test_invalid_frontmatter_leaves_no_partial_output(self):
        self.write_noise_image("photo.png")
        self.post.write_text("not frontmatter\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "missing YAML frontmatter"):
            process_post(self.post, self.root)

        self.assertFalse((self.asset_dir / "photo-social.png").exists())
        self.assertFalse((self.asset_dir / "photo-social.jpg").exists())

    def test_uneditable_header_leaves_no_partial_output(self):
        self.write_noise_image("photo.png")
        self.post.write_text(
            "---\n"
            "title: Example\n"
            "header: {image: /assets/images/photo.png, og_image: /assets/images/photo.png}\n"
            "---\n"
            "Post content.\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "frontmatter header mapping is required"):
            process_post(self.post, self.root)

        self.assertFalse((self.asset_dir / "photo-social.png").exists())
        self.assertFalse((self.asset_dir / "photo-social.jpg").exists())


if __name__ == "__main__":
    unittest.main()
