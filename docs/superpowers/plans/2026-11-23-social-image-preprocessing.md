# Social Image Preprocessing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically prepare Bluesky-compatible social images for every changed Jekyll post before deployment.

**Architecture:** A focused Python script will inspect changed posts, resolve each `header.og_image` to a repository asset, and create a deterministic under-1 MB PNG derivative or JPEG fallback. The workflow will run it before Jekyll builds, commit generated assets/frontmatter, and make the Bluesky job check out the updated `main` branch so it posts using the new metadata.

**Tech Stack:** Python 3.12, Pillow, PyYAML, `unittest`, GitHub Actions, Jekyll.

**Spec:** `docs/superpowers/specs/2026-11-23-social-image-preprocessing-design.md`

## Global Constraints

- Process every changed `_posts/*.md` file in the existing `HEAD~1..HEAD` range.
- Leave `header.image` and Markdown image links unchanged.
- Prefer a sibling `-social.png`; use `-social.jpg` only as a fallback.
- Treat 1,000,000 bytes as the threshold and target a safety margin below it.
- Use white for transparent pixels only when the JPEG fallback is required.
- Fail explicitly for unsupported references, malformed frontmatter, missing files, or conversion errors.
- Do not use GIF for photographic social images.

## Review Focus

- Oversized RGBA PNG: PNG derivative preserves transparency and stays below the limit; JPEG fallback uses white only when necessary. Test in Task 1.
- Already-small image: no derivative or frontmatter rewrite occurs. Test in Task 1.
- Absolute site URL and site-relative image references: both resolve to repository assets; unrelated external hosts fail clearly. Test in Task 1.
- Malformed or unsupported frontmatter: preprocessing fails without partial output. Test in Task 1.
- Generated commit followed by Bluesky checkout: Bluesky sees the updated `og_image`, while the subsequent push does not look like a newly added post. Verify in Task 2.

---

### Task 1: Build and test the social-image processor

**Files:**
- Create: `.github/scripts/prepare_social_images.py`
- Create: `.github/tests/test_prepare_social_images.py`
- Modify: `.github/scripts/requirements.txt`

**Interfaces:**
- Produces `process_post(post_path: Path, repository_root: Path, threshold: int = 1_000_000) -> bool`, returning whether the post or an asset changed.
- Produces `process_posts(post_paths: Sequence[Path], repository_root: Path) -> int`, returning the number of changed posts and raising a clear exception for any failure.
- The CLI accepts post paths as positional arguments and exits nonzero on any processing error.

- [ ] **Step 1: Write failing unit tests**

Add `unittest` cases using temporary repositories and Pillow-generated fixtures:

```python
def test_small_og_image_is_unchanged():
    changed = process_post(post, root)
    self.assertFalse(changed)
    self.assertFalse((asset_dir / "photo-social.png").exists())

def test_oversized_png_creates_small_png_and_updates_og_image():
    process_post(post, root)
    self.assertLess((asset_dir / "photo-social.png").stat().st_size, 1_000_000)
    self.assertIn("og_image: /assets/images/photo-social.png", post.read_text())
    self.assertIn("image: /assets/images/photo.png", post.read_text())

def test_png_falls_back_to_jpeg_when_png_cannot_meet_size_target():
    process_post(post, root)
    self.assertLess((asset_dir / "photo-social.jpg").stat().st_size, 1_000_000)
    self.assertIn("og_image: /assets/images/photo-social.jpg", post.read_text())

def test_absolute_site_url_resolves_and_external_url_is_rejected():
    ...

def test_invalid_frontmatter_or_missing_image_leaves_no_partial_output():
    ...
```

- [ ] **Step 2: Run the focused tests and verify they fail**

Run:

```bash
python3 -m unittest .github/tests/test_prepare_social_images.py -v
```

Expected: import/behavior failures because the processor does not exist.

- [ ] **Step 3: Add Pillow and implement the processor**

Add a pinned Pillow version to `.github/scripts/requirements.txt`. Implement:

- strict frontmatter extraction with `yaml.safe_load`;
- `og_image` lookup under `header` and site-relative/`https://rawlinson.us/` resolution;
- no-op for existing images at or below 1,000,000 bytes;
- deterministic `-social.png` generation with dimension reduction and PNG
  optimization;
- JPEG fallback with white alpha compositing if PNG cannot reach the target
  without excessive downscaling;
- targeted replacement of only the `og_image` frontmatter value;
- cleanup of partial output on failure and nonzero CLI exit.

- [ ] **Step 4: Run the focused tests and verify they pass**

Run:

```bash
python3 -m unittest .github/tests/test_prepare_social_images.py -v
```

Expected: all processor tests pass.

- [ ] **Step 5: Run the existing Bluesky tests**

Run:

```bash
python3 -m unittest .github/tests/test_bluesky_post.py -v
```

Expected: all existing tests pass, confirming the frontmatter changes remain
compatible with the Bluesky message generator.

- [ ] **Step 6: Commit the processor**

```bash
git add .github/scripts/prepare_social_images.py .github/tests/test_prepare_social_images.py .github/scripts/requirements.txt
git commit -m "feat: prepare small social images for Bluesky"
```

### Task 2: Integrate preprocessing into the Pages workflow

**Files:**
- Modify: `.github/workflows/jekyll.yml:38-100`
- Modify: `.github/workflows/jekyll.yml:130-145`

**Interfaces:**
- Consumes the changed-post list from `HEAD~1..HEAD`.
- Invokes `python3 .github/scripts/prepare_social_images.py` with every changed
  post path.
- Produces a committed working tree whose `og_image` metadata is available to
  the Jekyll build and to the later Bluesky job.

- [ ] **Step 1: Add a workflow-level integration check**

Extend the existing Python test or add a small shell assertion in the workflow
logic so a changed oversized post is included in the processor input and a
non-post change is ignored. The check must assert that the generated
`-social.*` asset and updated `og_image` are present before Jekyll runs.

- [ ] **Step 2: Run the integration check and verify it fails before workflow changes**

Run the relevant focused test command from Task 1 and inspect the workflow
logic locally; expected failure is the absence of the preprocessing step and
updated checkout behavior.

- [ ] **Step 3: Add the preprocessing workflow step**

After detection and before Ruby/Jekyll setup:

- derive changed post paths from the existing `HEAD~1..HEAD` range;
- install `.github/scripts/requirements.txt` before invoking the processor;
- run the processor for every changed post;
- `git add` generated assets and modified posts;
- commit/push only when staged changes exist;
- allow a processing error to fail the job before deployment.

- [ ] **Step 4: Make the Bluesky job use the generated commit**

Change its checkout to `ref: main`, so it sees the preprocessing commit and
posts the updated `og_image`. Preserve existing Bluesky URL update behavior.

- [ ] **Step 5: Run workflow syntax and local regression checks**

Run:

```bash
python3 -m unittest discover -s .github/tests -p 'test_*.py' -v
git diff --check
```

Expected: all Python tests pass and Git reports no whitespace errors.

- [ ] **Step 6: Commit the workflow integration**

```bash
git add .github/workflows/jekyll.yml
git commit -m "ci: prepare social images before Pages deployment"
```

### Task 3: Verify the end-to-end changed-post behavior

**Files:**
- Modify only temporary test fixtures or use a temporary branch/worktree; do
  not alter production content for this verification.

- [ ] **Step 1: Run the complete focused validation**

Run:

```bash
python3 -m unittest discover -s .github/tests -p 'test_*.py' -v
git diff --check
```

- [ ] **Step 2: Inspect the final diff**

Confirm only the processor, its tests, dependency manifest, workflow, and
design/plan documentation changed; confirm no article `header.image` values
were rewritten.

- [ ] **Step 3: Verify the generated output contract**

Using a temporary oversized PNG fixture, confirm the processor produces an
under-1 MB social image, updates only `header.og_image`, and exits nonzero
without partial files for invalid input.
