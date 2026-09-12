# Commons branch consolidation

Reviewed every remote branch on 2026-09-10. Integration started from the original
`master` on `codex/commons-consolidation`, in an isolated worktree. The original
checkout's two untracked research HTML files were preserved.

## Branch comparison and decisions

| Original branch | Reviewed tip | Contribution and disposition |
| --- | --- | --- |
| `master` | `df9fabd` | Original Backgammon Simplified copy; retained as the history and attribution baseline. Replaced by the verified Commons integration. |
| `baseline-original` | `df9fabd` | Identical historical baseline; no unique work. |
| `development` | `4a9dd5f` | Already merged the cleaned Commons site, course outlines, navigation, resources, glossary, and initial Lore work. Used as the integration foundation. |
| `development-clean` | `e8d4ae7` | Intentional cleanup through `1202128` was already in development. Four later files contain only `placeholder`, `ignore`, `x`, or a temporary source note; discarded after inspection. |
| `feature/nice-design-process` | `8ec2ef5` | Retained the complete student guide, phone-evolution RevealJS lesson, Project Builder with exports, and index links. |
| `lore-layout-refresh` | `86adea4` | Retained navigation order, article metadata, right-rail themes, revised NICE story, current logo narrative, and final lighthouse system board. Two latest WebP replacements were truncated; restored complete earlier versions. |
| `lore-logo-redesign` | `17ac791` | Original logo story and four source images. The newer narrative supersedes its article; its valid images recover the two corrupted replacements. Temporary preview workflows had already been removed. |
| `branding/commons-logo-asset-kit` | `3368a31` | Retained AA vectors, wordmark, favicon/app icons, fabrication exports, export generator, and static social-image capability. Its emblem design and duplicate aliases were superseded. |
| `design/commons-logo-asset-kit` | `c7a992b` | Retained the corrected lighthouse vector, beam gradients, monochrome and fabrication variants. Regenerated matching PNG/DXF exports using the branding tooling. |

All reviewed tips are ancestors of the integration history. Separate merge
commits preserve provenance, including branches with superseded content; no
unrelated history was rewritten. Branch deletion is permitted only after the
verified integration is safely on master and the remote heads still match.

## Consolidated architecture

- One course navigation definition in `site/_quarto.yml`; removed the duplicate
  `_learn-navigation.yml` and the abandoned Learn/Updates shells.
- Current routes use Lore and Wellbeing; removed their duplicate Research and
  Mindfulness implementations. Fixed About and 404 destinations.
- One served brand kit in `site/assets/branding`, with current favicon links.
  Removed root copies, compatibility aliases, and obsolete inherited favicon
  variants. Lore's historical illustrations remain separate from current branding.
- NICE's existing form markup is a raw HTML block with separate CSS/JS. Fixed
  mobile containment for input and report tables while preserving exports.
  Corrected RevealJS boundaries so large text stays on its intended slide.
- Kept the Lore theme rail and positioned the glossary search box below it.
  Removed unused animation styles and moved the embedded system-board bitmap to
  an ordinary asset without changing its bytes.
- The glossary now regenerates and validates both presentation files, removing
  stale relationships to deleted lessons. All 37 existing definitions remain.
- Quarto cache output is ignored, with previously committed `_freeze` files
  removed from tracking. Builds need Quarto, Python/PyYAML, and Node for tests.
- Added a Commons verification entrypoint and read-only CI render/check workflow.
  Retired tests that depended on removed publication, engine, or service code;
  retained tests for shared glossary, browser, and quality helpers. The manual
  branding workflow exports an artifact instead of pushing to an obsolete branch.

## Verification

- Full integration render: 40 pages with Quarto 1.10.15, without warnings.
- Retained Python suite: 52 tests passed.
- JavaScript: all eight asset syntax checks and twelve behavior test files passed.
- Local HTML/CSS audit: 2,169 references, no missing destinations or fragments.
- WebP assets: checked container lengths; the restored story images decode fully.
- Chromium checks cover 15 desktop pages, three mobile layouts, course/menu
  navigation, Lore filtering and rail placement, glossary searching, the NICE
  live document and Markdown/Word downloads, print visibility, and RevealJS navigation.
- Master promotion, final render, remote branch cleanup, and final browser results
  are recorded in the completion report for this task. Browser verification passed
  with no local errors or failed external requests.

## Preserved material and next phase

The inherited Backgammon glossary is explicitly identified on its page. Its
technology vocabulary replacement is future curriculum work. Unresolved related
terms remain plain text, preserving content without creating broken links.
Historical Backgammon articles in `site/posts` and `site/research` remain excluded
from rendering. Older tooling and documentation are historical reference material;
the README and authoring guide identify the active Commons commands.

The existing NICE spiral illustration placeholder and course outlines remain for
the next content phase. No first-week curriculum, new framework, or classroom
openings system was added. NICE exports are session-based: Word is compatible
HTML in a `.doc` file, PDF uses printing, and authors should export before leaving.
