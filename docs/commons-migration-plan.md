# Technology Commons migration plan

This migration keeps the original presentation layer and removes Backgammon-specific systems in small, testable passes.

## Iterations

0. Original site plus the Windows glossary import compatibility fix.
1. Remove the social-card generator while preserving the rendered site appearance.
2. Remove the Backgammon publication pipeline while preserving the site shell and glossary generation.
3. Preserve the glossary system. Do not remove glossary generation. Later, replace the Backgammon term set with Technology Commons terms focused on engineering design, technical communication, fabrication, computing, measurement, safety, and course vocabulary.
4. Remove the Backgammon application layer: position analyzer, Match Predictor, Shiny position dashboard, and engine benchmark application/report machinery. Preserve the common CSS, layout, components, transitions, navigation behavior, Learn shell, Research shell, and glossary system.
5. Remove remaining Backgammon-specific content in small groups while keeping reusable presentation components.
6. Add Technology Commons identity, public navigation, course landing shells, Tools, Resources, and the NICE reference page.
7. Add TAS2O, TEJ3M/4M, and TTJ3C/4C course sidebars and current course content.
8. Retarget and expand the glossary for Technology Commons.
9. Add the interactive NICE design-process tool after the core curriculum site is stable.

## NICE tool later phase

The future NICE tool should reuse the useful interaction pattern from Free Therapy Tools while being redesigned for the engineering design process.

N: Needs & Necessities
- Students enter requirements one at a time.
- Each requirement is classified as a need or a necessity.
- Needs record the minimum acceptable condition the design must satisfy.
- Necessities can be ranked by importance or priority.

I: Investigate & Inquire
- Guided research and brainstorming space.
- Record questions, observations, possible approaches, constraints, references, and findings.

C: Create & Communicate
- Brainstorm candidate solutions.
- Develop and record chosen concepts, sketches, CAD ideas, prototypes, calculations, materials, processes, and communication evidence.

E: Evaluate
- Compare the result against the original needs and necessities.
- Record testing evidence, failures, trade-offs, revisions, and next actions.
- Feed evaluation back into Needs & Necessities so NICE remains cyclical.

The tool should support saving progress and exporting a clear project record to PDF or Word. Implementation is intentionally deferred until the stable Commons course shell is in place.
