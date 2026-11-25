# Chiral SU(5) assessment

The [summary assessment](assessment-1.pdf), dated **25 November 2026**, has a one-page review followed by a one-page appendix on reflection positivity. [LaTeX source](assessment-1.tex). The appendix distinguishes auxiliary positivity at finite cutoff from positivity of the limiting expectations and discusses the result of Lu and Shao. The [source trace](su5-reflection-positivity-trace.txt) records the relevant definitions and lemmas.

The original submission is preserved in [OpenAI-chiral-20261115](https://github.com/yang-mills-group/OpenAI-chiral-20261115/tree/986dd35e0c0c930b90b0cd5886fb066ff7126be0). The group [received the submission on **15 November 2026**](https://github.com/yang-mills-group/submissions/blob/main/docs/submission-dates.md), distinct from the assessment date.

## Completed checks

| Record | Contents |
|---|---|
| [Comparator replay](su5-comparator/README.md) · [acceptance](su5-comparator/acceptance.json) · [log](su5-comparator/comparator.log) | Reference definitions and theorem matched; con-ron and Lean accepted |
| [Seven controls](su5-comparator/controls.json) · [containment log](su5-comparator/containment.log) | Positive case, statement and definition mismatches, extra axiom, proof hole, forced checker failure, and containment |
| [Replay provenance](su5-comparator/run-provenance.json) · [import checks](su5-comparator/import-checks.json) | Source count, export and tool hashes, configuration, environment, and import integrity |
| [Native-build validation](su5-native-build/final-validation.json) | Earlier source and configuration hashes, main theorem, allowed axioms, and native-build scope |
| [Reference build log](su5-native-build/reference-build.log) | Native Lean build of the reference entry point |
| [Solution build log](su5-native-build/solution-build.log) | Native Lean build of the solution entry point |
| [Axiom audit](su5-native-build/axiom-audit.log) | The solution theorem's axiom report |
| [Representation diagnostics](su5-review-checks.json) · [calculation script](su5-review-checks.py) | Exact group-factor and anomaly checks and the conventional one-loop coefficient |
| [Build summary](su5-native-build/status.txt) · [HTML version](su5-native-build/status.html) | Recorded final status of the native build |

These records now include the completed independent Comparator replay and both kernel checks, in addition to native macOS compilation, the axiom audit, and representation calculations. The native-build logs and receipts retain their original timestamps; the final status summary also links to the completed replay. The replay checked fresh macOS exports on Linux with real bubblewrap, rather than rebuilding the source on Linux. The fresh export hashes differ from the supplied acceptance record, with matching byte counts; the cause remains unresolved. The [replay notes](su5-comparator/README.md) state the completed checks and limits.
