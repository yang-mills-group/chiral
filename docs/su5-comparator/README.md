# Chiral SU(5): completed Comparator replay

The independent replay passed on **24 November 2026**, at 20:27 Eastern time (25 November 01:27 UTC). The checked theorem is `ChiralSU5.exists_interacting_three_generation_theory_with_exact_running`.

Linux Lean 4.35.0 Comparator matched the reference definitions and theorem and checked the permitted axioms. **con-ron in verified mode accepted 222,008 declarations; Lean's default kernel also accepted.** The allowed axioms are `propext`, `Classical.choice`, and `Quot.sound`.

| Record | What it records |
|---|---|
| [Acceptance](acceptance.json) · [Comparator log](comparator.log) | Successful reference comparison and both kernel verdicts |
| [Controls](controls.json) | All seven controls passed with the expected exit codes and log markers |
| [Containment log](containment.log) | Writes denied to protected paths and inputs; no external network route |
| [Export record](export-status.json) | Fresh reference and solution export sizes, hashes, compiler and exporter pins |
| [Run provenance](run-provenance.json) | Actual container command, source count, export hashes, tool hashes and configuration hash |
| [Final container state](container-final-state.json) | Exit code 0, with no out-of-memory kill |
| [Import checks](import-checks.json) | Read-only validation before import and hashes of the copied records and scripts |
| [Replay files](replay/) | Actual configuration, sandbox profile, scripts, and small control sources |

The controls include a valid proof and rejection of a wrong statement, changed definition, forbidden axiom, `sorryAx`, and a deliberately failing external checker. The seventh control checks containment. These test the verification process; they are not additional tests identifying the constructed theory with physical chiral gauge theory.

The source build and exports used macOS Lean 4.32.0 with the pinned dependencies. Comparator and the two kernels ran in Linux with real bubblewrap, read-only proof inputs, and no external network. This replay did not rebuild the source on Linux. Before import, all 16,523 source files were checked against the original archive's manifest; the current export, tool, configuration, and main-log hashes also matched the replay records.

Both fresh export hashes differ from [OpenAI's acceptance record](https://github.com/yang-mills-group/OpenAI-chiral-20261115/blob/986dd35e0c0c930b90b0cd5886fb066ff7126be0/verification/acceptance.json), although both byte counts agree. The cause remains unresolved. The independent acceptance applies to the fresh exports identified in this folder, not to an assertion that the exports were reproduced byte for byte.

The multi-gigabyte proof exports and tool binaries are not stored in this repository. Their hashes and locations are recorded. The replay scripts preserve the original workspace layout and paths; they are records of the completed run, not a portable setup package. Original logs and acceptance records are unchanged. The status page's assessment link was adjusted to the group copy.

The earlier [native-build records](../su5-native-build/final-validation.json) describe the stage before replay. See the [current assessment](../assessment-1.pdf) for the remaining questions about chirality, operator identification, interaction, and running coupling.
