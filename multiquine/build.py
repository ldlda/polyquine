"""CLI: choose topology, build skeletons, link, write."""

import argparse
import json
from pathlib import Path

from cycles import choose_cycle, cycle_window
from lda import STRATEGIES, link, load_languages, write


def main():
    root = Path(__file__).resolve().parent
    catalog = load_languages(root)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strategy', choices=STRATEGIES, default='packed_index')
    parser.add_argument('--mode', choices=('network', 'ring'), default='network')
    parser.add_argument('--languages', default=','.join(catalog))
    cycle_source = parser.add_mutually_exclusive_group()
    cycle_source.add_argument('--cycle')
    cycle_source.add_argument('--cycle-file', type=Path)
    parser.add_argument('--order', choices=('set', 'sorted', 'random'), default='set')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    cycle_options = (
        args.cycle is not None
        or args.cycle_file is not None
        or args.order != 'set'
        or args.seed is not None
    )
    if args.mode == 'network' and cycle_options:
        parser.error('cycle/order/seed options require --mode ring')
    try:
        ids = choose_cycle(
            args.languages,
            catalog,
            explicit=args.cycle,
            file=args.cycle_file,
            order=args.order,
            seed=args.seed,
        )
        languages = [catalog[name] for name in ids]
        if args.mode == 'ring':
            stages = [
                t.build([n], strategy=args.strategy) for t, n in cycle_window(languages)
            ]
        else:
            stages = [t.build(languages, strategy=args.strategy) for t in languages]
        generated = link(stages)
        output = args.output or root / ('out-ring' if args.mode == 'ring' else 'out')
        write(generated, catalog, output)
        if args.mode == 'ring':
            (output / 'cycle.json').write_text(
                json.dumps(ids, indent=2) + '\n', encoding='utf-8'
            )
        for name, data in generated.items():
            print(f'{output / catalog[name].filename}: {len(data)} bytes')
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
