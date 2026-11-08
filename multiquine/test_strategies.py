"""Exercise every composed strategy through real native processes."""

import argparse
import tempfile
from pathlib import Path

from lda import STRATEGIES, link, load_languages
from runtime import available, command_for, execute
from test import branching, network, relay


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-all', action='store_true')
    parser.parse_args()
    catalog = load_languages(Path(__file__).resolve().parent)
    missing = [name for name in catalog if not available(name)]
    if missing:
        parser.error('missing runtimes: ' + ', '.join(missing))
    from test_quotes import main as check_quotes

    check_quotes()
    languages = list(catalog.values())
    count = 0
    for strategy in STRATEGIES:
        print('STRATEGY', strategy, flush=True)
        with tempfile.TemporaryDirectory(prefix='lda-strategy-') as directory:
            work = Path(directory)
            _, n = network(languages, work, strategy)
            count += n
            for order in (
                languages,
                sorted(languages, key=lambda t: t.id),
                list(reversed(languages)),
            ):
                _, n = relay(order, work, strategy=strategy)
                count += n
            for t in languages:
                _, n = relay([t], work, laps=2, strategy=strategy)
                count += n
            branching(catalog, work, strategy)
            count += 4
    # Packed strategies share the same seed protocol and may coexist.
    py, rs, php = (catalog[name] for name in ('py', 'rs', 'php'))
    stages = [
        py.build([rs], strategy='packed_index'),
        rs.build([php], strategy='record_callable'),
        php.build([py], strategy='packed_map'),
    ]
    generated = link(stages)
    current = generated['py']
    with tempfile.TemporaryDirectory(prefix='lda-mixed-strategies-') as directory:
        work = Path(directory)
        for t, n in ((py, rs), (rs, php), (php, py)):
            source = work / t.filename
            source.write_bytes(current)
            current = execute(command_for(t.id, source, work), cwd=work)
            if current != generated[n.id]:
                raise AssertionError('mixed packed strategies')
            count += 1
    try:
        link([py.build([rs], strategy='marker_map'), rs.build([py])])
    except ValueError:
        pass
    else:
        raise AssertionError('incompatible seed protocols accepted')
    print('PASS mixed packed strategies and incompatible-protocol rejection')
    print(
        f'ALL STRATEGIES PASS: {count} successful emitted-program executions',
        flush=True,
    )


if __name__ == '__main__':
    main()
