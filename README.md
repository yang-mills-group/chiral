# Chiral SU(5) — Results and verification

## [Read the draft one-page assessment (PDF)](docs/assessment-1.pdf)

**Private draft for discussion, 24 November 2026.** [LaTeX source](docs/assessment-1.tex).

This repository collects chiral gauge-theory submissions and the group's checks and assessments. The first submission is OpenAI's chiral SU(5) construction, labeled **15 November 2026**. It claims a four-dimensional continuum theory with three generations of left-handed fermions in the **10** and **5̄** representations, obtained from a common lattice history and selected vacuum.

The submitted theorem includes relativistic reconstruction, chirality conditions, a nonzero mixed matter–gauge correlation, and an ultraviolet running condition with coefficient **43/3**. The running statement concerns averages over increasingly long ultraviolet windows. The physical interpretation of the chiral fields, interaction test, and fitted coupling requires further review.

## Results and assessments

| Submission date | Original submission | Assessment |
|---|---|---|
| 15 November 2026 | [OpenAI-chiral-20261115](https://github.com/yang-mills-group/OpenAI-chiral-20261115) | [Draft one-page assessment](docs/assessment-1.pdf) |

The submission date is provisional and may be corrected before public release. The assessment concerns the package preserved at [archive commit `986dd35`](https://github.com/yang-mills-group/OpenAI-chiral-20261115/tree/986dd35e0c0c930b90b0cd5886fb066ff7126be0).

All 16,523 project Lean files compiled on macOS with the pinned dependencies. The main theorem's axiom audit found only the standard axioms and no `sorryAx`. An independent representation calculation checks the group factors, cubic anomaly cancellation, and the arithmetic giving the one-loop coefficient. This does not independently verify the submitted RG derivation.

We have not replayed Comparator, its second kernel, or the supplied Linux isolation and controls. Further checks are needed for the chiral measure and gauge invariance, exclusion of mirror degrees of freedom, the operator dictionary, and comparison with an appropriate free theory. Mass gap, confinement, particle spectrum, and uniqueness of the continuum limit are not established by the reviewed target.

## Documents and verification records

[docs/](docs/README.md) contains the assessment, its source, build and axiom records, and representation diagnostics. The [original proof repository](https://github.com/yang-mills-group/OpenAI-chiral-20261115) preserves OpenAI's source, claim, comparator configuration, and replay instructions.

## Making a submission

Send proposed submissions and feedback to [yangmills4d@gmail.com](mailto:yangmills4d@gmail.com). Include the authors, claimed results, a fixed revision of the materials, and reproduction instructions for formal checks. The group's [submission requirements](https://github.com/yang-mills-group/.github-private/blob/main/profile/README.md#making-a-submission) apply. Inclusion does not constitute endorsement, and the group does not promise to post or review submissions.
