# Changelog

Development history of the LDA generator, distributed here as `multiquine`.
Version labels refer to the development packages; they do not imply Git tags.

## 0.15 — Documentation and polish

- Shortened the README around usage, structure, and verification.
- Moved development history into this changelog.
- Reformatted Python build/test files with ruff

## 0.14 — C and Kotlin

- Added C and Kotlin, bringing the total to 13 languages across five strategies.
- Added Kotlin quoting: JSON-style escaping plus escaped dollar signs.
- Implemented the new format in every emitter through renderer composition.
- Used length-aware text and typed function pointers in C.
- Expanded encoder probes to all emitters and all five formats; corrected
  control-character escaping differences in older JSON implementations.
- Added optional C AddressSanitizer/UBSan checks and Kotlin toolchain setup.
- Kept the core builder, linker, strategy configuration, and cycle code unchanged.
- Passed 1,258 strategy executions, 325 encoder probes, and 20 C sanitizer
  executions. Leak detection was disabled for the sanitizer checks.

## 0.13 — Java and Haskell

- Added Java and Haskell with support for all five strategies.
- Used the JDK source-file launcher for Java and GHC compilation for Haskell.
- Added native encoder probes and toolchain setup.
- Passed 958 strategy executions and 80 encoder probes.

## 0.12 — Lua and Perl

- Added Lua and Perl with support for all five strategies.
- Reused the PHP single-quoted literal format for Perl's source strings.
- Added encoder probes for quotes, backslashes, and all ASCII byte values.
- Passed 698 strategy executions and 40 encoder probes.

## 0.11 — Explicit strategy configuration

- Centralized storage, access, renderer scope, and binding in a strategy table.
- Replaced scattered strategy-name checks and conditional template paths.
- Separated graph validation, embedding methods, and cycle-file parsing.
- Simplified CLI control flow and cycle-source argument validation.
- Added `.gitignore` and an AI-assistance disclosure.
- Preserved all 420 generated files across 60 before/after configurations.

## 0.10 — Composed strategy templates

- Exposed all five strategies through the build API and CLI.
- Kept one outer template per language, with included data/emission/access sections.
- Shared packed-data and emission sections across four strategies.
- Shared record sections between renderer-name and callable variants.
- Removed the benchmark's Python native-source string assembly.
- Supported mixed packed-strategy graphs; rejected incompatible seed protocols.

## 0.9 — Unified construction

- Introduced `Language.build(targets)` and a shared linking step.
- Used the same language templates for networks and rings.
- Removed the separate ring generator, duplicate templates, circular imports,
  and dependency discovery through rendering side effects.
- Standardized generated source extensions.

## 0.8 — Relay mode and Docker

- Added a slim fixed-successor relay mode and shared skeleton seed.
- Supported explicit, sorted, seeded-random, and file-loaded cycle orders.
- Added real emitted-source relay execution tests and Docker build instructions.
- Fixed dependency ordering to load prerequisites before consumers.

## 0.7 — Rust and PHP

- Added Rust and PHP and the PHP single-quoted literal format.
- Verified seven-language cross-generation and reduced selections.

## 0.6 — Composable renderers

- Added transitive renderer dependencies through `LDA_REQUIRES` declarations.
- Reused JSON quoting to implement `json_inner`.
- Detected dependency cycles, missing snippets, and unknown formats.

## 0.5 — PowerShell

- Added PowerShell and its single-quoted literal format.
- Separated bootstrap encoders into `quote.py` and simplified builder functions.
- Used binary output paths to avoid text-mode newline transformations.
- PowerShell execution was verified later when its runtime became available.

## 0.4 — Renderer discovery

- Discovered requested formats from template operations.
- Used two Jinja passes to resolve dependencies before importing native snippets.
  This mechanism was subsequently replaced in 0.9.

## 0.3 and earlier — Initial prototypes

- Started with a Python quine and expanded to cross-language source reproduction.
- Introduced single-pass `LDA:language:renderer` references.
- Added Jinja language loops, a manifest, renderer includes, and generated registries.
- Developed the Python, JavaScript, Go, and Ruby emitters.
