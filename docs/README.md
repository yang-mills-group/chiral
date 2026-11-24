# Chiral SU(5) assessment

The [one-page assessment](assessment-1.pdf), dated **24 November 2026**, summarizes the claims, completed checks, and remaining questions. [LaTeX source](assessment-1.tex). It is a draft for group discussion.

The original submission is preserved in [OpenAI-chiral-20261115](https://github.com/yang-mills-group/OpenAI-chiral-20261115/tree/986dd35e0c0c930b90b0cd5886fb066ff7126be0). The **15 November** submission date is a provisional label, distinct from the assessment date.

## Completed checks

| Record | Contents |
|---|---|
| [Final validation](su5-native-build/final-validation.json) | Source and configuration hashes, main theorem, allowed axioms, and verification scope |
| [Reference build log](su5-native-build/reference-build.log) | Native Lean build of the reference entry point |
| [Solution build log](su5-native-build/solution-build.log) | Native Lean build of the solution entry point |
| [Axiom audit](su5-native-build/axiom-audit.log) | The solution theorem's axiom report |
| [Representation diagnostics](su5-review-checks.json) · [calculation script](su5-review-checks.py) | Exact group-factor and anomaly checks and the conventional one-loop coefficient |
| [Build summary](su5-native-build/status.txt) · [HTML version](su5-native-build/status.html) | Recorded final status of the native build |

These records cover native macOS compilation, source integrity, the axiom audit, and representation calculations. They do not record an independent Comparator or second-kernel replay. The original archive contains OpenAI's own verification record and replay instructions.
