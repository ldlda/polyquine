# multiquine

A generator for programs that reproduce source code across **13 languages**.
Build an all-target network or a fixed cycle of programs.

Release history is in [CHANGELOG.md](CHANGELOG.md). The generator's internal name
is LDA; its Python API remains in `lda.py`.

## Quick start

Run these commands from this folder. Generating source needs only Python and
Jinja; executing it needs the selected language's runtime or compiler.

```sh
python -m pip install -r requirements.txt
python build.py --languages py,js
python out/py.py js
```

The last command prints the generated JavaScript source. With no target argument,
a network program prints its own source.

```sh
# Full network: every program can emit every selected language.
python build.py

# Ring: Python emits C, C emits Kotlin, Kotlin emits Python.
python build.py --mode ring --cycle py,c,kt

# Other ordering and output options.
python build.py --mode ring --order random --seed 42
python build.py --mode ring --cycle-file cycles/thirteen.json
python build.py --languages py,rs --output generated
```

Network output goes to `out/`; ring output goes to `out-ring/`. Ring programs emit
one fixed successor. The saved `cycle.json` records the exact order and can be
reused with `--cycle-file`. `--order set` preserves supplied order; `sorted` sorts
IDs; `random` shuffles them. Cycle files accept JSON arrays or text lists separated
by commas/whitespace, with `#` comments in text files.

Generated outputs and compiler artifacts are ignored by `.gitignore`.

## Languages

| ID | Language | Execution toolchain |
| --- | --- | --- |
| `py` | Python | `python` |
| `js` | JavaScript | `node` |
| `go` | Go | `go` |
| `rb` | Ruby | `ruby` |
| `ps` | PowerShell | `pwsh` |
| `rs` | Rust | `rustc` and a system linker |
| `php` | PHP | `php` |
| `lua` | Lua | `lua` |
| `pl` | Perl | `perl`, including core `JSON::PP` |
| `java` | Java | Java 21+ JDK, including its compiler module |
| `hs` | Haskell | GHC and native linking dependencies |
| `c` | C | C11 compiler (`cc`) |
| `kt` | Kotlin | `kotlinc` and Java |

Source filenames use the ID and its extension: `py.py`, `c.c`, `kt.kt`, etc.
PowerShell uses `ps.ps1`. C, Go, Rust, and Haskell are compiled before execution;
Kotlin is compiled to a runnable JVM JAR. The tests handle these steps.

## Strategies

Choose one with `--strategy NAME`; `packed_index` is the default.

| Strategy | Representation |
| --- | --- |
| `packed_index` | Shared seed, numeric source selection |
| `packed_map` | Shared seed, named source map |
| `record_key` | Entries containing source and renderer name |
| `record_callable` | Entries containing source and callable |
| `marker_map` | Named `LDA:language:renderer` references |

The four packed strategies share data and emission sections. Named markers use
a separate embedding method. Packed strategies may coexist in an API-built graph;
packed and marker representations cannot share one graph.

## Build API and source layout

```python
from pathlib import Path
from cycles import cycle_window
from lda import load_languages, link, write

catalog = load_languages(Path("."))
languages = list(catalog.values())
stages = [t.build([n]) for t, n in cycle_window(languages)]
write(link(stages), catalog, Path("generated"))
```

For a full network, use `stages = [t.build(languages) for t in languages]`.
`build(targets, strategy=...)` records a stage. `link(stages)` validates the graph,
then renders the templates and embeds their source data.

| File or directory | Responsibility |
| --- | --- |
| `build.py` | CLI and topology selection |
| `lda.py` | Language/stage objects, rendering and linking |
| `strategies.py` | Explicit strategy configuration |
| `cycles.py` | Cycle parsing and ordering |
| `manifest.json` | Language IDs, default quoting and extensions |
| `quote.py` | Bootstrap string encoders |
| `templates/<id>.j2` | Native outer template |
| `templates/data/`, `emit/`, `access/` | Shared and strategy-specific sections |
| `templates/renderers/` | Native encoder implementations |
| `runtime.py` | Test-only compiler/process execution helper |

Native renderer snippets can declare dependencies on their first line, for
example `-- LDA_REQUIRES: json,`. The comment prefix is not prescribed.

## Verification

```sh
python test.py --require-all
python test_strategies.py --require-all
python test_c_memory.py   # Optional C AddressSanitizer/UBSan checks.
```

Install all toolchains for the full suites. `test.py` alone may skip a missing
PowerShell runtime without `--require-all`; the all-strategy suite requires all
runtimes. Tests execute real programs, compare stdout bytes, and fail on runtime
errors, timeouts, or differences. Checks remain active under `python -O`.

Recorded v0.14 results: **1,258 strategy executions**, **325 encoder probes**, and
**20 C sanitizer executions** passed. Leak detection is disabled by default in
the optional sanitizer suite. Details are in [test_results.txt](test_results.txt).

Size benchmarks are available through `python benchmark/run.py`; add
`--all-renderers` to compare strategies with equal renderer sets.

## Docker

```sh
docker build --platform linux/amd64 -t multiquine .
docker run --rm --network none multiquine
```

The Dockerfile installs all toolchains and runs both main suites during the
image build. Its default command runs the all-strategy suite. Building requires
network access; tests run offline. The image targets Linux amd64.

**The Dockerfile passed error-level lint checks, but the image itself was not
built on the development host.** Direct toolchain executions were verified.

## Constraints and attribution

Source templates currently require valid **ASCII program text in UTF-8/LF**.
Encoder probes containing every ASCII byte do not imply every such byte is valid
source syntax. Arbitrary Unicode source and Windows execution are unverified.
Each generated program carries the information needed to reconstruct its peers;
ring mode reduces active dispatch code rather than eliminating that information.

The original v0.14 implementation and these documentation updates were developed
with **OpenAI's ChatGPT/Codex**, under the user's direction. The user supplied
requirements, architectural ideas, corrections, and feedback. The assistant
wrote the original builder, native templates, renderer snippets, tests,
Dockerfile, and documentation; subsequent repository edits may differ.
