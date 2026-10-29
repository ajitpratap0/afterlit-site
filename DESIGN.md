---
name: afterlit
description: Life after the cloud. A calm, ruled, paper-and-ink workbench for a cautious local Bluetooth tool.
colors:
  ink: "#172a36"
  rust: "#b64727"
  rust-hover: "#a74022"
  rust-text: "#9d3b20"
  paper: "#f4f2eb"
  paper-raised: "#f9f8f2"
  paper-sunk: "#ebe8df"
  bench: "#dedfd3"
  readback: "#e9ede4"
  text-lede: "#4d5b60"
  text-muted: "#586763"
  text-soft: "#5d6c64"
  text-on-bench: "#53665c"
  rule: "#c9c7bb"
  rule-soft: "#d6d4ca"
  sage-text: "#4b654f"
  sage-text-soft: "#536e5b"
  sage-line: "#b9c3b2"
  status-ready: "#4b7a52"
  status-ready-text: "#3f6b47"
  status-pending: "#a8592b"
  status-pending-text: "#9a4a1c"
  status-future: "#6f7c75"
  terminal-text: "#e5ece4"
  terminal-head: "#b5c9be"
  terminal-note: "#c1ccc5"
  terminal-rule: "#435560"
  terminal-prompt: "#e4956b"
  tone-warm: "#efbd7b"
  tone-amber: "#d98246"
  tone-sage: "#91aa8d"
  tone-blue: "#86aeb5"
  tone-off: "#a7aca1"
  select: "#efbd7b"
  white: "#ffffff"
  art-detail: "#99b3aa"
  art-cloud: "#98a6a0"
  swatch-line: "#718179"
  art-grid: "#dedbd0"
  art-halo: "#e5ad71"
typography:
  display:
    fontFamily: "Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(48px,13cqi,96px)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.035em"
  thesis:
    fontFamily: "Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(40px, 3.6vw + 8px, 64px)"
    fontWeight: 400
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(34px,3.5vw,58px)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(25px,2vw,32px)"
    fontWeight: 400
    letterSpacing: "-0.02em"
  lede:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.65
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  body-small:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
  ui:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "14px"
    fontWeight: 700
  button:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "15px"
    fontWeight: 700
  wordmark:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "26px"
    fontWeight: 800
    letterSpacing: "-0.04em"
  workbench-title:
    fontFamily: "Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(28px,2.4vw,36px)"
    fontWeight: 400
    letterSpacing: "-0.02em"
  label-large:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 700
    letterSpacing: "0.09em"
  diagram-label:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "17px"
    letterSpacing: "0.03em"
  diagram-label-phone:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "24px"
    letterSpacing: "0.02em"
  label:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "11px"
    fontWeight: 700
    letterSpacing: "0.09em"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "13px"
    lineHeight: 1.75
rounded:
  none: "0px"
  base: "5px"
  round: "50%"
spacing:
  s-1: "4px"
  s-2: "8px"
  s-3: "12px"
  s-4: "16px"
  s-5: "24px"
  s-6: "32px"
  s-7: "48px"
  s-8: "64px"
  s-9: "96px"
  s-10: "128px"
  section: "clamp(44px, 4vw + 24px, 84px)"
  measure: "31em"
  tap: "44px"
components:
  button-primary:
    backgroundColor: "{colors.rust}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0 20px"
    height: "52px"
    typography: "{typography.button}"
  button-primary-hover:
    backgroundColor: "{colors.rust-hover}"
    textColor: "{colors.white}"
  button-text:
    textColor: "{colors.ink}"
    height: "52px"
    typography: "{typography.button}"
  badge-status:
    textColor: "{colors.sage-text}"
    padding: "8px 11px"
    rounded: "{rounded.none}"
    typography: "{typography.label}"
  terminal:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.terminal-text}"
    typography: "{typography.code}"
  workbench-visual:
    backgroundColor: "{colors.bench}"
    textColor: "{colors.text-on-bench}"
  workbench-controls:
    backgroundColor: "{colors.paper-raised}"
    textColor: "{colors.ink}"
  readback:
    backgroundColor: "{colors.readback}"
    textColor: "{colors.ink}"
    padding: "18px 21px"
  swatch:
    rounded: "{rounded.round}"
    size: "44px"
---

# Design System: afterlit

> This file records the system as it stands after the Impeccable design pass on branch feat/impeccable-design-pass. Token names match the custom properties in the :root block of website/styles.css. Font sizes are written as literal px or clamp() in each rule, because scripts/check_site.py rejects font-size:var(). The north star name is unconfirmed by the owner.

## Overview

**Creative North Star: "The Repair Bench Notebook"**

afterlit looks like a careful person's workbench notes: warm paper, navy ink, thin ruled lines between entries, and a single rust pencil used for what matters. The page states, qualifies and records; it does not sell with spectacle. It has two set pieces, and both are instruments:
- one dark terminal panel showing real, shortened device-check output;
- a small simulated lamp whose readback panel confirms every control change.

The page is calm and reading-first. Ambition shows as precision:
- exact output;
- honest status;
- one rust action per view;
- a compact owner-help band immediately after the hero;
- a single authored motion moment (the lamp's light cross-fade plus the readback confirmation).

The illustration language is line drawing on a faint grid: a computer, a lamp, a crossed-out cloud. There is no photography, 3D, gradient or glow except the lamp's own light.

**Key Characteristics:**
- Paper ground, ink text, one rust accent. Sage and status colours are used only to report state.
- Georgia display headlines over an Arial body. Monospace is reserved for code, commands, readings and small uppercase labels.
- Flat surfaces, square corners and hairline rules. No drop shadows.
- No kicker or eyebrow label above any heading. Headings stand alone.
- Light scheme only, system fonts only, no network requests.

## Colors

The palette is warm paper neutrals and navy ink, with one burnt-rust accent and a small semantic status set.

### Primary
- **Workbench Rust** (--rust #b64727) is used for:
  - the primary button and the wordmark full stop
  - the italic hero phrase and the Today list markers
  - the focus ring, chevrons and diagram wires

  It is 4.78:1 on paper.
- **Rust Hover** (--rust-hover #a74022): the primary button's hover state only.
- **Rust Text** (--rust-text #9d3b20): rust text on tinted grounds, such as the "BLE / LOCAL" diagram label and the no-JS note.

### Status (state only, always paired with a text label)
- **Ready:** dot --status-ready #4b7a52; tag text --status-ready-text #3f6b47 (5.51:1). It is also used for the header badge dot and the readback confirmation dot.
- **Pending:** dot --status-pending #a8592b; tag text --status-pending-text #9a4a1c (5.56:1).
- **Not yet / Not implemented:** dot --status-future #6f7c75; tag text --text-soft.

### Secondary
- **Field Sage** (--sage-text #4b654f, --sage-text-soft #536e5b, --sage-line #b9c3b2): "local" and readback labels, the badge border and the footer link underline. Never a call to action.

### Neutral
- **Bench Ink** (--ink #172a36): body text, headings, the terminal ground, the lamp silhouette and the heavy footer rule.
- **Notebook Paper** (--paper #f4f2eb): the page background and the theme-color meta.
- **Raised Paper** (--paper-raised #f9f8f2): the workbench controls.
- **Sunk Paper** (--paper-sunk #ebe8df): the hero diagram panel.
- **Bench** (--bench #dedfd3): the simulated device stage.
- **Readback** (--readback #e9ede4): the readback panel.
- **Copy:**
  - --text-lede #4d5b60: the hero lede.
  - --text-muted #586763: all secondary copy (5.30:1).
  - --text-soft #5d6c64: 11 to 13px meta.
  - --text-on-bench #53665c: text on the bench ground (4.56:1).
- **Rules:** --rule #c9c7bb for lists, steps, status and FAQ; --rule-soft #d6d4ca for the header, section dividers, footer-bottom and panel outlines.
- **Terminal set:** text #e5ece4, header #b5c9be, notes #c1ccc5, rules and scrollbar #435560, prompt / in-terminal focus / in-terminal selection #e4956b.
- **Lamp tones** (illustration data shared by .tone-* and .swatch-*): warm #efbd7b, amber #d98246, sage #91aa8d, blue #86aeb5, off #a7aca1.
- **Illustration lines:** --art-detail #99b3aa (screen lines), --art-cloud #98a6a0 (the crossed-out cloud), --swatch-line #718179 (unpressed swatch outline). --art-grid #dedbd0 (the diagram grid) and --art-halo #e5ad71 (the lamp halos). The only literal hex outside :root is the @property --light initial-value, which must be a literal and is checked against --tone-warm.
- **Selection:** --select #efbd7b (the lamp's warm light) with ink text.

### Named Rules
**The One Pencil Rule.** Rust is the only decorative accent. It marks the primary action, focus and annotations. Status colours report state and nothing else.

**The Colour Is Never the Message Rule.** Every status dot sits next to a text state: "Available", "Pending", "Not yet" or "Not implemented".

## Typography

**Display Font:** Georgia (with "Times New Roman", serif), as --font-display.

**Body Font:** Arial (with Helvetica, sans-serif), as --font-body.

**Mono Font:** ui-monospace (with SFMono-Regular, Consolas, monospace), as --font-mono.

**Character:** a bookish serif for statements, a neutral sans for explanation, and a technical monospace for anything that is code or an instrument reading. All three are system faces: the page downloads no font files, by policy (the CSP has no font-src).

### Hierarchy
- **Display** (h1, 400, line-height 1, -.035em):
  - Sized to its column: clamp(48px,13cqi,96px) with a clamp(48px,5.8vw,96px) fallback, and clamp(48px,8cqi,58px) at 950px and below, so the size at 768px stays below the two-column size at 1024px.
  - The size grows steadily with width and never exceeds 96px (measured: 48px at 320 and 600, about 55 at 768, 59 at 1024, 84 at 1440, 88 at 1920).
  - The second line is an italic rust `em`.
  - The authored `<br>` holds at two-column widths; text-wrap:balance applies only at 620px and below, where the `<br>` is hidden.
- **Headline** (h2, 400, clamp(34px,3.5vw,58px), 1.08, -.03em, balanced).
- **Title** (h3, 400, clamp(25px,2vw,32px), -.02em, balanced). The workbench h3 is clamp(28px,2.4vw,36px), always below its h2.
- **Lede** (18px, 1.65, max-width 30em).
- **Body** (16px, 1.7, max-width 31em, about 70 characters): section copy and FAQ answers (FAQ answers use line-height 1.65).
- **Body small** (14px, 1.55): outcome and output captions, step text (max 34em), terminal captions, the hardware note.
- **FAQ summary** (18px, 1.35, bold, 44px target).
- **UI** (bold; nav 14px at 621px and above, 13px on phones; buttons 15px).
- **Wordmark** (26px Arial 800, -.04em; 32px in the footer).
- **Label** (11 to 12px mono, .09em, uppercase only; 12px is label-large): terminal headers, bench labels, state tags, range ends. Mixed-case mono sentences (bench foot, diagram footer, footer bottom line) use .02em.
- **Code** (13px, line-height 1.75; 12px at 620px and below; ligatures off; white-space pre-wrap).

### Named Rules
**The Eleven Pixel Floor.** No text below 11px. Every size is px, or a clamp() with a px minimum (enforced by scripts/check_site.py).

**The Tracking Floor.** No letter-spacing tighter than -.04em (enforced by scripts/check_site.py).

**The Measure Rule.** Prose never runs past about 75 characters per line (--measure 31em). Terminal captions get this through padding, so the panel's rules still span full width.

**The Instrument Voice Rule.** Monospace is for commands, output, readings and uppercase labels, never for decorative sentences.

**The No Kicker Rule.** No tracked label ever sits above a heading. When a label carried meaning, it was folded into the heading itself (for example "For contributors: how afterlit frees a new device"). The step ordinals sit inline in each step heading, in the heading's own face ("01 Capture: observe first."), so a step has one heading. scripts/check_site.py enforces this two ways: it rejects the eyebrow and kicker classes, and it rejects a short label element (span, small, strong, b, em, i, code or mark up to 40 characters, or an all-caps p or div) that is the immediate previous sibling of an h1 to h4. This is a heuristic, not a full guard: a label made uppercase only by CSS inside a p or div, or a label separated from its heading by a wrapper, still passes, so review new headings by eye.

## Layout

- **Shell:** max 1560px wide; side gutter clamp(24px,5.5vw,96px), 22px at 620px and below.
- **Section rhythm:** sections are separated by a 1px --rule-soft line with padding var(--section-pad), clamp(44px, 4vw + 24px, 84px), roughly a third less than before. The Today band uses 32px vertical padding.
- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 (--s-1 to --s-10).
- **Content sections:** device check keeps a two-column split (.9fr / 1.1fr), with its terminal sticky (top 24px) at 951px and above. Today, contributors, status and FAQ follow a single-column reading order; the FAQ list is capped at 840px.
- **Hero:** splits 1.05fr / .95fr, with the diagram on the right.
- **Contributor detail:** the workflow is a short paragraph followed by a native developer disclosure, including plain descriptions of doctor and the practice run instead of transcripts.
- **Status table:** spans the section; at 951px and above, rows are a dot, a name with its state tag directly under it, and the description at measure. On phones the rows stack.
- **Page order:**
  1. hero
  2. What you can do today
  3. device check
  4. browser preview
  5. contributors (with doctor and practice-run notes in a disclosure)
  6. status
  7. FAQ (four short answers)
- **Breakpoints:**
  - 951 to 1439px: hero SVG labels upsized to 17 viewBox units so they never render below 11px.
  - 950px: the device-check split and workbench stack; hero SVG labels use 13 units.
  - 760px: the nav takes its own row with a 16px gap, so no link wraps alone.
  - 620px: status rows stack; the nav becomes a two-column grid with Today spanning the first row.
- **Must hold:**
  - No horizontal overflow at 320px, including under translation expansion and the WCAG 1.4.12 text-spacing override. Grid children set min-width:0, text sets overflow-wrap:break-word, and headings use hyphens:auto.
  - Terminal lines wrap instead of scrolling.

## Elevation & Depth

Flat by design: there are no box-shadows. Depth comes from tonal grounds (paper, raised paper, sunk paper, bench, ink terminal) and from hairline rules. The only blur is the lamp's glow inside the simulation.

### Named Rules
**The Ruled Page Rule.** Separate things with a 1px rule or a change of ground, never with a shadow or a floating card.

## Shapes

- **Corners:** square for buttons, panels, terminals, the badge and the diagram frame.
- **Round:** reserved for status dots, colour swatches, diagram halos and the lamp base (5px).
- **Lines:**
  - 1px rules (--rule / --rule-soft);
  - a 2px ink rule over the footer;
  - a 1px ink underline on the text button.
- **Links:** text-underline-offset .2em, thickness 1px.
- **Illustration strokes:** 2 to 5px, with round caps and joins.

## Motion

There is one authored moment: the control-and-readback loop of the browser lamp.

- **Lamp:** --light (registered <color>) and --glow (registered <number>) cross-fade over .32s with cubic-bezier(.16,1,.3,1), so a colour change passes through real intermediate tints.
- **Readback:** the text updates in the same frame as the control. Delays are never faked. The readback status dot plays a single .6s scale-and-fade confirmation, triggered only by user input, never on page load.
- **Micro feedback:** the FAQ and developer-notes chevrons rotate in .18s; the primary button background and link underline colour ease over .15s.
- **Forbidden:** entrance animations, scroll-driven effects, parallax and staged loading.
- **Reduced motion:** prefers-reduced-motion makes every change instant and removes the pulse.
- **Fallback:** browsers without @property get an instant change.

## Components

### Buttons
- **Shape:** square (0 radius), 52px high, 15px bold, with an arrow glyph slot.
- **Primary:** rust background, white text, padding 0 20px, and a transparent 1px border that becomes visible in forced colours. Hover: --rust-hover.
- **Text button:** ink text with a 1px ink bottom border, the same height.
- **Focus:** a 3px solid rust outline with a 4px offset.
- **One primary per view.** The hero primary reads "See how the device check works".

### Hero note, status line and Today band
- **Hero note:** body sans, 13px bold ink, sentence case. From 621px the three trust facts run inline with small rust middots; each fact is nowrap and each middot is glued to the fact before it with a no-break space, so no wrapped line starts with "·". Below 621px the middots hide and the facts stack one per line.
- **Hardware note:** a 14px bold ink status line directly under the lede, before the actions, with a 1px rust left rule and 16px inset: pre-alpha, private source, no public download, real-device testing (Gate 1) pending.
- **Today band:** immediately follows the hero, with a 25–32px heading and three compact 14px ordered lines for exact-model research, keeping the vendor app and pairing, and returning to this page for status. Lines wrap naturally on phones.

### Status badge
- A 1px sage-line border, sage text, an 11px uppercase mono label, padding 8px 11px, and a 6px --status-ready dot. It is used once, in the header ("Pre-alpha").

### Ruled lists (status and FAQ)
- A 1px rule between rows and a 22 to 24px vertical rhythm. There are no index numbers; numbers belong only to the ordered steps.
- **Rows:** a bold title, then a 14px muted caption at measure.
- **Status rows:** a coloured dot, the name, its semantic state tag under the name (at 951px and above), and the description.
- **FAQ:** native details/summary with a rust CSS chevron, an 18px summary with a 44px target, and 16px answers. Answers expand in print (Chromium).

### Terminal panel
- An ink background and a mono header row above a 1px terminal rule.
- A focusable labelled `pre` (role region, unique aria-label without scroll instructions), 13px, line-height 1.75, wrapping (pre-wrap, overflow-wrap:break-word). Each logical output line is a span.ln (inline-block, full width) with a 2ch hanging indent, and "Fix:" lines hang at 4ch, so a wrapped continuation never reads as a new output line. The text and newlines are unchanged, so copying gives the same characters. Because the lines wrap, the pre never scrolls; it keeps tabindex="0" and role="region" because scripts/check_site.py requires them on every pre.
- The `$` prompt is in --terminal-prompt and aria-hidden.
- A thin themed scrollbar as a fallback.
- A caption paragraph saying what was shortened.
- Developer-only detail goes into a "Notes for developers" details element in the contributor section, using the paper ground and the same rust chevron as the FAQ.

### Workbench (signature component)
- **Bench visual** (--bench): a CSS-drawn lamp (shade clip-path, stem, base, and a blurred glow driven by --light and --glow through .level-* and .tone-*). Labels: "SIMULATED DEVICE / LAMP 01" and "● BROWSER ONLY".
- **Controls** (--paper-raised):
  - an h3 "Control the simulation." (no label above it);
  - a 44px range input in accent rust;
  - 44px round swatches using aria-pressed;
  - a readback panel (role status, aria-live polite, tabular numerals) whose text is only rewritten when it changes.
- **Without JS:** the fieldset stays disabled until site.js runs, and a note explains why.
- **Forced colours:** the bench visual keeps its authored colours; swatches keep their hue with a Highlight ring.
- The pane always states that it is a browser-only simulation that produces no evidence.

### Navigation
- **Header row:** the wordmark (26px bold, -.04em, rust glyph and full stop), five in-page links in page order (Today, Device check, Preview, For contributors, Status; 44px targets). The contributor link is a label, not an invitation: there is no public repository to contribute to, and scripts/check_site.py rejects nav labels such as Contribute, Download, Install or Get started, and the status badge.
- **Narrow screens:** at 760px and below the nav wraps onto its own row; at 620px and below it is a two-column grid with Today spanning the first row.
- A skip link appears on focus.

### Hero diagram
- A sunk-paper panel with a faint grid: a computer, a lamp with halos, a rust wire and a crossed-out cloud. Mono annotations are 11 viewBox units (.05em tracking), upsized to 17 between 951 and 1439px, 13 between 621 and 950px and 24 on phones, so they never render below 11px. These sizes are SVG user units, recorded as diagram-label and diagram-label-phone. "BLE / LOCAL" starts at x=254, 14 units clear of the wire's vertical run, and is hidden on phones. On phones the enlarged labels are nudged by CSS transforms (the cloud label 14,14 units clear of the strike line, the two base labels 10 units below the drawings).
- The footer captions read "Observe / Verify / Keep evidence".
- role="img" with a full aria-label. It keeps its colours in forced colours.

### 404 page
- One h1, "Page not found" (clamp(48px,5vw,64px)), and a lede linking to the home page, the device check and the current status, plus the "Back to afterlit" button. It uses the same stylesheet and cache token.

## Browser Surfaces
- **Selection:** warm lamp light with ink text; on terminals, the prompt colour with ink text.
- **Scrollbars:** themed on terminals.
- **Underlines:** link underline offset .2em.
- **Numerals:** tabular in the readback and the slider output.
- **Focus rings:** rust, or the prompt colour on ink.
- **Print:** navigation, CTAs and the workbench are hidden; terminals wrap; FAQ answers print; external link URLs are appended.

## Do's and Don'ts

### Do:
- **Do** keep rust to the primary action, annotations and focus (The One Pencil Rule).
- **Do** show proof as real, shortened CLI output in a terminal panel, fully visible, with a caption saying what was cut.
- **Do** pair every status colour with a text state.
- **Do** keep prose at about 70 characters per line, text at 11px or larger, tap targets at 44px, and scroll regions focusable and labelled.
- **Do** use the token custom properties for colour, font family and spacing, and literal px or clamp() for font-size.
- **Do** bump every `?v=` cache token together when CSS or JS changes.
- **Do** explain jargon (Gate 1, OTA/DFU, BLE) in plain words on first use.

### Don't:
- **Don't** put a kicker, eyebrow or tracked label above a heading.
- **Don't** track display type tighter than -.04em.
- **Don't** add drop shadows, rounded cards, gradients or glassmorphism; the system is flat and ruled.
- **Don't** add a second decorative accent colour, or use status colours for anything but state.
- **Don't** number lists whose order carries no meaning.
- **Don't** fake work with delays, or add entrance or scroll animations.
- **Don't** add logos, testimonials, device counts, "works with" lists, install commands, a download button, a lookup box or a waitlist (check_site.py NEVER_CLAIM and the honesty floor).
- **Don't** use inline styles or scripts, external or self-hosted webfonts, analytics or any network request (strict CSP).
- **Don't** put en dashes, em dashes or U+2212 in visible text.
