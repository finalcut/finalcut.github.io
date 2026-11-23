# Social Image Preprocessing Design

## Intent

Ensure Bluesky link cards receive a usable thumbnail without changing the
image displayed in the article. When a changed post's `header.og_image` is
larger than 1 MB, CI will create a smaller JPEG beside the source image,
update only `og_image` to point to that derivative, and continue the existing
Jekyll deployment and Bluesky workflow.

## Goals

- Process every changed post in a push.
- Leave the article's `header.image` and Markdown image links unchanged.
- Keep generated social images under `assets/images/`, beside their source.
- Make the resulting frontmatter change visible in Git history.
- Fail explicitly when an image is configured but cannot be read or converted.
- Avoid regenerating an already-created derivative unnecessarily.

## Non-goals

- Recompressing images below the 1 MB threshold.
- Replacing article images with JPEGs.
- Changing Jekyll permalink or future-post behavior.
- Reposting existing Bluesky posts automatically unless the existing workflow
  already decides to do so.

## Approaches

1. **GitHub Actions preprocessing (selected):** inspect changed posts before
   Jekyll builds, using the repository's existing Python tooling and a pinned
   image library. This is automatic and applies consistently from every
   development machine.
2. **Local-only preprocessing:** provide a developer command to prepare images
   before pushing. This avoids CI work but depends on remembering to run it and
   cannot protect pushes made elsewhere.
3. **Runtime/theme transformation:** generate social images during Jekyll
   rendering. This does not naturally update source frontmatter and would make
   the Bluesky step race the generated metadata, so it does not fit the
   current workflow.

## Design

- Add a focused Python script under `.github/scripts/` that:
  - receives the changed post paths from the workflow;
  - parses frontmatter safely;
  - resolves absolute `https://rawlinson.us/...` and site-relative image
    references to repository files;
  - checks the configured `header.og_image` file size;
  - first creates a deterministic sibling `-social.png`, preserving
    transparency and reducing dimensions/metadata until the output is below
    1 MB;
  - falls back to a deterministic sibling `-social.jpg` only when PNG cannot
    meet the size target without excessive downscaling; JPEG uses a white
    background for transparent pixels;
  - updates the post's `header.og_image` while preserving the rest of the
    frontmatter and body.
- Add the image library to `.github/scripts/requirements.txt` with a pinned
  version.
- Add a workflow step before the Jekyll build that passes all changed
  `_posts/*.md` files to the script.
- Commit and push generated derivatives/frontmatter updates using the existing
  workflow token. Prevent the resulting push from creating a second Bluesky
  post by relying on the workflow's existing “new file” detection and keeping
  the original post identity unchanged.
- Add focused tests for: below-threshold no-op, oversized PNG conversion,
  absolute URL resolution, frontmatter update, and conversion failure.

## Open implementation calls

- Process every changed post in the commit.
- Prefer a sibling `-social.png` derivative; use `-social.jpg` only as a
  quality-preserving fallback when PNG compression is insufficient. Do not
  use GIF for photographic images because its 256-color palette causes
  visible quality loss.
- Treat 1,000,000 bytes as the threshold and target a small safety margin
  below it.
- Use the existing workflow's commit/push pattern rather than introducing a
  separate workflow.
