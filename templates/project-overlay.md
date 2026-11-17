---
tone: neutral
type: dashboard
exclude_components: [Tabs]   # optional — drop contracts this project does not use,
                             # even if the project-type matrix would include them
# specimens: [pill, bookmark-card]  # optional — order/filter .ds4a/specimens/*.html;
                                    # omit to render every file in the folder
---

## Overview

<!--
Optional. Replaces the tone's Overview for this project. Delete this section to
keep the tone's own personality.

Token overrides go in the frontmatter, using the same keys as a tone pack and
listing only what differs, e.g.:

  colors:
    primary: "#7C3AED"        # imported --primary
  rounded:
    md: 10px

`exclude_components:` takes a plain list and removes those contracts from the
generated Components section (and any matrix filter). Use it instead of prose
like "we don't use tabs" that the reader has to reconcile by hand.

`specimens:` is metadata for the preview, not a token: list the slugs under
`.ds4a/specimens/` you want rendered and in what order. Omit it to render every
file in the folder. `add`/`remove` in `scripts/specimens.py` maintain it.

A `## <Section>` whose body starts with `<!-- replace -->` REPLACES that
section of the resolved doc (core + tone content dropped) instead of being
appended below it. Use it when the project contradicts the library outright
(e.g. no shadows anywhere). Without the marker, your section is appended
below the core/tone content as "Project notes".

All other `## <Section>` blocks (Colors, Typography, Components, Do's and
Don'ts, Pre-flight Checklist, ...) are appended to that section of DESIGN.md.
-->
