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
    fontSize: "clamp(36px,8cqi,72px)"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "-0.03em"
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
  section: "clamp(64px, 6vw + 40px, 128px)"
  thesis: "clamp(96px, 10vw, 160px)"
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

> This file records the system as it stands after the critique fixes on branch feat/critique-fixes. Token names match the custom properties in the :root block of website/styles.css. Font sizes are written as literal px or clamp() in each rule, because scripts/check_site.py rejects font-size:var(). The north star name is unconfirmed by the owner.

## Overview

**Creative North Star: "The Repair Bench Notebook"**

afterlit looks like a careful person's workbench notes: warm paper, navy ink, thin ruled lines between entries, and a single rust pencil used for what matters. The page states, qualifies and records; it does not sell with spectacle. It has two set pieces, and both are instruments:
- dark terminal panels showing real, fully visible command output;
- a small simulated lamp whose readback panel confirms every control change.

The page is calm and reading-first. Ambition shows as precision:
- exact output;
- honest status;
- one rust action per view;
- a single typographic peak after the hero (the thesis band);
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
  - the primary button (and its hover)
  - annotations: the wordmark full stop, the hero diagram wire, nodes, cloud strike and "BLUETOOTH / LOCAL" label, and the no-JS note ("Turn on JavaScript to use the lamp preview; everything else on this page works without it.")
  - the focus ring

  Links, chevrons, step ordinals, slider controls and hero-note separators are ink or --text-soft, never rust.

  It is 4.78:1 on paper.
- **Rust Hover** (--rust-hover #a74022): the primary button's hover state only.
- **Rust Text** (--rust-text #9d3b20): rust text on tinted grounds, such as the "BLUETOOTH / LOCAL" diagram label and the no-JS note.

### Status (state only, always paired with a text label)
- **Ready:** dot --status-ready #4b7a52; tag text --status-ready-text #3f6b47 (5.51:1). It is also used for the header badge dot and the readback pencil stroke. The readback confirmation dot is a text glyph, so it uses --status-ready-text (5.20:1 on --readback).
- **Pending:** dot --status-pending #a8592b; tag text --status-pending-text #9a4a1c (5.56:1).
- **Not yet:** dot --status-future #6f7c75; tag text --text-soft.

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

**The Colour Is Never the Message Rule.** Every status dot sits next to a text state: "Available", "Pending" or "Not yet". The status intro says "Not yet" covers both planned and unbuilt parts.

## Typography

**Display Font:** Georgia (with "Times New Roman", serif), as --font-display.

**Body Font:** Arial (with Helvetica, sans-serif), as --font-body.

**Mono Font:** ui-monospace (with SFMono-Regular, Consolas, monospace), as --font-mono.

**Character:** a bookish serif for statements, a neutral sans for explanation, and a technical monospace for anything that is code or an instrument reading. All three are system faces: the page downloads no font files, by policy (the CSP has no font-src).

### Hierarchy
- **Display** (h1, 400, line-height 1.05, -.03em):
  - A status sentence sized to its column: clamp(36px,8cqi,72px), with a clamp(36px,5vw,72px) fallback. It has a 15em maximum width, manual hyphenation and balanced wrapping, with no authored line break.
  - At 620px and below the h1 is clamp(28px,9cqi,34px), line-height 1.08, -.02em.
  - Computed sizes and line counts at target viewports remain pending browser verification; the base rule ranges from 36 to 72px and the phone rule from 28 to 34px.
- **Hero pitch** (.hero-pitch, Arial 700, ink, inline): "A second life for your smart devices." opens the lede as its first sentence, so the hero copy has five tiers (h1, status, lede, actions, note). Not italic, not display, not rust, never above the h1 or the status line. The hero note separates its two phrases with a dot that has one plain space on each side, so it sits centred.
- **Thesis** (the problem h2, 400, clamp(40px, 3.6vw + 8px, 64px), 1.04, -.035em): the one typographic peak after the hero.
- **Headline** (h2, 400, clamp(34px,3.5vw,58px), 1.08, -.03em, balanced).
- **Title** (h3, 400, clamp(25px,2vw,32px), -.02em, balanced). The workbench h3 is clamp(28px,2.4vw,36px), always below its h2.
- **Lede** (18px, 1.65, max-width 30em).
- **Body** (16px, 1.7, max-width 31em, about 70 characters): section copy and FAQ answers (FAQ answers use line-height 1.65).
- **Body small** (14px, 1.55): outcome and output captions, step text (max 34em), terminal captions.
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

**The No Kicker Rule.** No tracked label ever sits above a heading. When a label carried meaning, it was folded into the heading itself (for example "For contributors: investigating a new device"). The step ordinals sit inline in each step heading, in the heading's own face ("01 Capture: observe first."), so a step has one heading. scripts/check_site.py enforces this two ways: it rejects the eyebrow and kicker classes, and it rejects a short label element (span, small, strong, b, em, i, code or mark up to 40 characters, or an all-caps p or div) that is the immediate previous sibling of an h1 to h4. This is a heuristic, not a full guard: a label made uppercase only by CSS inside a p or div, or a label separated from its heading by a wrapper, still passes, so review new headings by eye.

## Layout

- **Shell:** max 1560px wide; side gutter clamp(24px,5.5vw,96px), 22px at 620px and below.
- **Section rhythm:** sections are separated by a 1px --rule-soft line with padding var(--section-pad), clamp(64px, 6vw + 40px, 128px). The thesis band breathes more (clamp(96px,10vw,160px)) and at 951px and above its heading (7fr) and paragraph (5fr) share one row, the paragraph aligned to the heading's last line.
- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 (--s-1 to --s-10).
- **Content sections:** check and doctor use a two-column split (.9fr / 1.1fr). The DOM order is intro (heading and explanation), terminal, then detail (outcomes or the state legend, and in doctor a disclosure). Each intro opens with a plain-language takeaway (18px ink, class takeaway) before any command-line detail; in check that takeaway is "This page has no lookup box" and glosses "command-line tool" on first use. Doctor shows only its takeaway, one sentence and the transcript; the state legend, the AFL-D codes and the system requirements sit in one disclosure ("What the states mean and system requirements"). At 951px and above the intro and detail sit on the left and the terminal spans both rows on the right; at 950px and below they stack in DOM order, so the output is read before the legend that explains it. The today, practice run, contributors and status sections use a heading row above their content (7/5 at 951px and above, align-items:start so each heading leads its section); the lamp preview has no split header: its h2 and one muted line stack at measure and the workbench leads; the FAQ is a single column at measure. At 951px and above the device check puts its intro beside the terminal and then runs the detail across the full width beneath both: the four answers in four columns, then the "Any match is a lead" line on the left and the confidence legend on the right, so neither column ends far before the other; its terminal is not sticky. In doctor, the terminal is position:sticky (top 121px, below the sticky header) at 951px and above. The thesis band puts its heading (7fr) and paragraph (5fr) in one row, the paragraph aligned to the heading's last line. Sections that say the visitor does not need them yet (doctor, practice run, contributors) end their takeaway with a one-line escape to the current status. The practice run and contributor heading rows wrap their takeaway and intro in .head-copy so the 7/5 row keeps two columns, so the proof stays beside the text it illustrates.
- **Hero:** splits 1.05fr / .95fr, with the diagram on the right.
- **Steps:** a 4-column ruled strip. Each h3 starts with its ordinal in --text-soft (01 to 04) and names the stage, then the plain action; step headings do not auto-hyphenate. Step 03 keeps one plain sentence ("Each write needs your approval and starts from read-only.") and folds the probe detail into a ruled disclosure inside its own card ("How the probe stays safe").
- **Ordinals:** every .number (today list and contributor steps) uses one treatment: the display face, weight 400, lining tabular numerals, --text-soft.
- **Status board:** a ruled grid of status rows, three columns at 951px and above, two from 761px, one below. Each row is a dot, a name with its state tag under it, and the description. There is no bottom border and no bottom padding on the status section: the FAQ's section rule closes the board.
- **Page order:**
  1. hero (status first: h1, the pre-alpha status line, the lede that explains what afterlit checks first, with the pitch as its first sentence, then two actions: the device check and "Three steps for now" (to #today), then the hero note)
  2. what you can do today
  3. thesis
  4. device check (the confidence wording is an always-visible dl; the terminal note names the outcomes in transcript order; Not freed yet and Out of scope both link back to step 01; Not freed yet also links to the contributor path)
  5. readiness check, afterlit doctor (state legend, codes, radio scan and system requirements behind one disclosure)
  6. practice run (the h2 is "The practice run"; the command afterlit demo appears once, in code style)
  7. lamp preview (browser only)
  8. contributors (with "What a run produces")
  9. status
  10. FAQ in two groups of four or fewer in visitor order ("Before you start", then "How it works", h3 each), ending with the page's only "Back to top" link
- **Breakpoints:**
  - 951 to 1439px: hero SVG labels upsized to 17 viewBox units so they never render below 11px.
  - 950px: splits stack, steps become 2 columns, the workbench stacks; hero SVG labels use 13 units.
  - 900px: the nav takes its own row with a 16px gap, so no link wraps inside the header row.
  - 620px: steps become 1 column; status rows stack; the nav wraps onto two rows so all five labels are visible at load (40px link rows, each label unbroken); the h1 drops to clamp(28px,9cqi,34px) at line-height 1.08; the readback uses 1fr 1fr 2fr columns so "Warm white" stays on one line.
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
- **Readback:** two steps, "01 Requested by this page" and "02 Reported back by the simulated lamp", under "SIMULATED IN THIS BROWSER". Both update in the same frame as the control. Delays and approvals are never faked. Only step 02 is a live region. Two marks confirm a change, both triggered only by user input, never on page load: the step 02 status dot plays a single .6s scale-and-fade, and a 2px --status-ready pencil stroke draws left to right under each value that changed (.5s, cubic-bezier(.16,1,.3,1)) and stays until the next change. Requested and reported strokes draw together, never staggered. A change that rewrites no value leaves the strokes in place.
- **Micro feedback:** the FAQ and developer-notes chevrons rotate in .18s; the primary button background eases over .15s; link hover thickens the underline to 2px without transition; the selected swatch's ink ring opens to its 4px offset in .18s and the previous one closes in .1s.
- **Forbidden:** entrance animations (including any load-time motion in the hero diagram), scroll-driven effects, parallax and staged loading.
- **Reduced motion:** prefers-reduced-motion makes every change instant and removes the pulse; the pencil stroke still appears, instantly, so the record of what changed is kept.
- **Fallback:** browsers without @property get an instant change.

## Components

### Buttons
- **Shape:** square (0 radius), 52px high, 15px bold, with an arrow glyph slot.
- **Primary:** rust background, white text, padding 0 20px, and a transparent 1px border that becomes visible in forced colours. Hover: --rust-hover.
- **Text button:** ink text with a 1px ink bottom border, the same height.
- **Focus:** a 3px solid rust outline with a 4px offset.
- **One primary per view.** The hero primary reads "See how the device check works".

### Hero status and hero note
- **Hero note:** body sans, 13px bold ink, sentence case. From 621px the two trust facts run inline, separated by a small --text-soft .note-sep dot with one plain space on each side; each fact is nowrap. Below 621px the .note-sep dot hides and the facts stack one per line.
- **Hero status:** 18px ink with a 3px pending-colour left rule and a bold "Pre-alpha." lead. It is the hero's honesty line and sits directly under the h1, above the lede and the actions: private source, no public download, real-device testing pending. scripts/check_site.py requires exactly one .hero-status.

### Status badge
- A 1px sage-line border, sage text, an 11px uppercase mono label, padding 8px 11px, and a 6px --status-ready dot. It is used once, in the header ("Pre-alpha").

### Ruled lists (outcomes, run outputs, confidence, today, status, FAQ)
- A 1px rule between rows and a 22 to 24px vertical rhythm. Ordinals belong to ordered steps and the today list.
- **Rows:** a bold title, then a 14px muted caption at measure.
- **Confidence list:** a dl with mono dt and body dd, used for match confidence and the doctor report states. Output words are quoted as literals ("OK", "Check" (a warning), "Problem", "Skipped", "Not applicable") so "Check" never reads as the device check or readiness check. It stacks on phones.
- **Tool names:** one display name per tool (device check, readiness check, practice run, lamp preview); the command (afterlit check, afterlit doctor, afterlit demo) appears once, in code style.
- **Today list:** three ordered steps with inline ordinals, 18px bold titles and 16px explanations; three columns at 951px and above. Step 01 ends with an ink link, "Not sure it is Bluetooth?", to the first FAQ answer (#faq-bluetooth), which starts open.
- **Status rows:** a coloured dot, the name, its semantic state tag under the name (at 951px and above), and the description. Ready tags read "Available (private source)"; scripts/check_site.py rejects an "Available" tag without "private source".
- **FAQ:** native details/summary with an ink CSS chevron, an 18px summary with a 44px target, and 16px answers. Answers expand in print (Chromium).

### Terminal panel
- An ink background and a mono header row above a 1px terminal rule. Every header reads "EXAMPLE OUTPUT · PRIVATE SOURCE ONLY" and "NO RADIO USED", so no prompt reads as an instruction and the constraint is seen before the command; the two halves of the first label are each nowrap, so a narrow panel breaks only at the dot. scripts/check_site.py requires "EXAMPLE OUTPUT" and "PRIVATE SOURCE ONLY" on every .terminal-head.
- A focusable labelled `pre` (role region, unique aria-label without scroll instructions), 13px, line-height 1.75, wrapping (pre-wrap, overflow-wrap:break-word). Each logical output line is a span.ln (inline-block, full width) with a 2ch hanging indent, and "Fix:" lines hang at 4ch, so a wrapped continuation never reads as a new output line. The text and newlines are unchanged, so copying gives the same characters. Because the lines wrap, the pre never scrolls; it keeps tabindex="0" and role="region" because scripts/check_site.py requires them on every pre.
- The `$` prompt is in --terminal-prompt and aria-hidden.
- A thin themed scrollbar as a fallback.
- A caption paragraph saying what was shortened.
- Developer-only detail and term glossaries go into a "Terms and notes for developers" details element, styled for the dark ground (terminal-note text, a prompt-coloured chevron and focus ring).

### Workbench (signature component)
- **Bench visual** (--bench): a CSS-drawn lamp (shade clip-path, stem, base, and a blurred glow driven by --light and --glow through .level-* and .tone-*). Labels: "LAMP PREVIEW" and "● BROWSER ONLY".
- **Controls** (--paper-raised):
  - an h3 "Set the lamp." (no label above it), in .bench-intro;
  - a 44px range input in accent ink;
  - 44px round swatches using aria-pressed;
  - a readback panel with a Requested step and a Reported back step (step 02 has role status, aria-live polite, tabular numerals), text only rewritten when it changes. At 0% brightness the swatches are disabled, a note explains why, and both steps report Color "None".
  - a "Reset preview" text button that returns the lamp to 75% and Warm white through the same update(), so the readback reports the reset like any other change.
- **Layout:** the h3 "Set the lamp." and its intro sit in .bench-intro, the first child of the workbench. At 951px and above the bench visual spans both rows on the left and the intro sits above the controls on the right. At 950px and below the stack reads intro, lamp, then controls, and the controls column (flex) orders the readback first, directly under the lamp, so a change and its reported state share one screen. The readback holds nothing focusable, so keyboard order is unaffected. At 620px and below the lamp is scaled to .62.
- **Without JS:** the fieldset stays disabled until site.js runs, and a note explains why.
- **Forced colours:** the bench visual keeps its authored colours; swatches keep their hue with a Highlight ring.
- The pane always states that it is a browser-only simulation that produces no evidence.

### Navigation
- **Header row:** the wordmark (26px bold, -.04em, ink glyph, rust full stop), five in-page links in page order (What you can do today, Device check, Lamp preview, Status, FAQ; 44px targets). Each destination has one label: the nav and the heading for #today both read "What you can do today"; the hero's secondary button is a call to action toward it, "Three steps for now", so the first screen does not repeat the label. The link for the section crossing the middle of the screen gets aria-current="location" (site.js, IntersectionObserver), drawn as a 2px ink underline at a 6px offset with no transition, and the status badge. There is no contributor link: the contributor section is reached in page order. scripts/check_site.py rejects nav labels such as Contribute, Download, Install or Get started.
- **Narrow screens:** at 900px and below the nav takes its own row; at 620px and below it wraps onto two rows (40px link rows, inset focus ring), so all five labels are visible at load without scrolling. A single "Back to top" link follows the FAQ; no section repeats it. The header is position:sticky (top 0, z-index 5, paper fill bled to the screen edges with a 100vmax box-shadow clipped by clip-path), so the wordmark link and the aria-current underline stay in view while reading. html carries scroll-padding-top (112px, 144px at 900px and below and at 620px and below, where the two-row phone header is about 137px) so anchors land below the header.
- A skip link appears on focus.

### Hero diagram
- A sunk-paper panel with a faint grid: a computer, a lamp with halos, a rust wire and a crossed-out cloud. Mono annotations are 11 viewBox units (.05em tracking), upsized to 17 between 951 and 1439px, 13 between 621 and 950px and 24 on phones, so they never render below 11px. These sizes are SVG user units, recorded as diagram-label and diagram-label-phone. "BLUETOOTH / LOCAL" starts at x=254, 14 units clear of the wire's vertical run, set on two lines ("BLUETOOTH /", then "LOCAL") so it stays clear of the lamp stem at every label size, and is hidden on phones. On phones the enlarged labels are nudged by CSS transforms (the cloud label 14,14 units clear of the strike line, the two base labels 10 units below the drawings).
- The diagram is a figure: the picture (role="img") keeps its own label, and the caption row is a figcaption below it with a top rule, without overlapping the drawing. The caption is one link to #workflow that reads as one sentence: "Contributor path: capture, infer, verify, save", underlined ink throughout, balanced when it wraps, never spaced out like a row of tabs. At 620px and below the SVG uses preserveAspectRatio slice with aspect-ratio 570/420, trimming empty grid top and bottom so the today section starts higher. Base labels use --sage-text with a 4px sunk-paper stroke halo and paint-order:stroke so grid lines do not reduce their contrast.
- The picture is role="img" with a full aria-label. It keeps its colours in forced colours.

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
