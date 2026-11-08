"""Optional GCC/Clang AddressSanitizer + UBSan checks for every C strategy."""

import os
import subprocess
import tempfile
from pathlib import Path

from lda import STRATEGIES, link, load_languages


def main():
    root = Path(__file__).resolve().parent
    catalog = load_languages(root)
    languages = list(catalog.values())
    environment = os.environ.copy()
    # LeakSanitizer uses ptrace, which the development host blocks. Address and
    # undefined-behavior checks remain active; callers may override this setting.
    environment.setdefault('ASAN_OPTIONS', 'detect_leaks=0')
    count = 0
    with tempfile.TemporaryDirectory(prefix='lda-c-sanitizers-') as directory:
        work = Path(directory)
        for strategy in STRATEGIES:
            generated = link(t.build(languages, strategy=strategy) for t in languages)
            source = work / 'c.c'
            source.write_bytes(generated['c'])
            binary = work / 'c-bin'
            subprocess.run(
                [
                    'cc',
                    '-std=c11',
                    '-O1',
                    '-g',
                    '-fsanitize=address,undefined',
                    '-fno-omit-frame-pointer',
                    str(source),
                    '-o',
                    str(binary),
                ],
                check=True,
            )
            for target in ('c', 'kt', 'pl', 'ps'):
                result = subprocess.run(
                    [str(binary), target],
                    check=False, capture_output=True,
                    timeout=30,
                    env=environment,
                )
                if (
                    result.returncode
                    or result.stderr
                    or result.stdout != generated[target]
                ):
                    raise AssertionError(
                        (
                            strategy,
                            target,
                            result.returncode,
                            result.stderr.decode(errors='replace'),
                        )
                    )
                count += 1
            print('PASS C sanitizers:', strategy, flush=True)
    print(
        f'ALL C MEMORY CHECKS PASS: {count} executions; leak detection disabled by default'
    )


if __name__ == '__main__':
    main()
