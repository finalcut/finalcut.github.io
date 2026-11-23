from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[2] / ".github" / "workflows" / "jekyll.yml"
).read_text(encoding="utf-8")


class SocialImageWorkflowTest(unittest.TestCase):
    def test_changed_posts_are_filtered_before_processing(self):
        self.assertIn(
            'git diff --name-only HEAD~1 HEAD | grep "^_posts/.*\\.md\\?$"',
            WORKFLOW,
        )
        self.assertIn("prepare_social_images.py", WORKFLOW)
        self.assertIn('IFS=\',\' read -ra POSTS <<< "$CHANGED_POSTS"', WORKFLOW)

    def test_bluesky_job_checks_out_generated_main_commit(self):
        self.assertIn("ref: main", WORKFLOW)
        self.assertIn("token: ${{ secrets.GITHUB_TOKEN }}", WORKFLOW)

    def test_generated_assets_are_committed_before_build(self):
        processor_index = WORKFLOW.index("prepare_social_images.py")
        ruby_index = WORKFLOW.index("- name: Setup Ruby")
        self.assertLess(processor_index, ruby_index)
        self.assertIn("git add _posts/ assets/images/", WORKFLOW)


if __name__ == "__main__":
    unittest.main()
