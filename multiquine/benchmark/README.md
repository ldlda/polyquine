# Strategy benchmark

The benchmark now calls `Language.build(..., strategy=...)` and `link(...)`.
There are no frozen duplicate language templates or Python native-code emitters.

```sh
python benchmark/run.py
python benchmark/run.py --all-renderers
python benchmark/run.py --strategy marker_map --order manifest
```

Each run writes its selected configurations to `results_needed.json` or
`results_equal.json`, plus generated source files under `outputs/`. A filtered
run replaces that policy's results file with just its selected configurations.
Every measured cycle is executed through real runtimes and checked byte for
byte, then rebuilt for determinism. Binaries are excluded from source-byte totals.

Historical benchmark numbers came from older templates and are preserved in the
separate `lda_benchmarks.zip` deliverable. This refactor changes formatting and
some emitted code; rerun measurements before comparing this release's sizes.
The release smoke-tested the named-marker manifest cycle through this harness;
`test_strategies.py` provides the full all-strategy execution coverage.
