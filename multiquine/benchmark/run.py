"""Measure and execute composed strategies through the public build/link API."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cycles import cycle_window
from lda import STRATEGIES, link, load_languages, write
from runtime import command_for, execute


def run(all_renderers=False, strategies=STRATEGIES, order_filter=None):
    root = Path(__file__).resolve().parents[1]
    here = Path(__file__).resolve().parent
    catalog = load_languages(root)
    ids = list(catalog)
    shuffled = ids[:]
    random.Random(42).shuffle(shuffled)
    orders = dict(manifest=ids, sorted=sorted(ids), random42=shuffled)
    policy = 'equal' if all_renderers else 'needed'
    results = []
    for order, names in orders.items():
        if order_filter is not None and order != order_filter:
            continue
        languages = [catalog[name] for name in names]
        for strategy in strategies:
            stages = [t.build([n], strategy=strategy) for t, n in cycle_window(languages)]
            generated = link(stages, all_renderers=all_renderers)
            output = here / 'outputs' / policy / order / strategy
            write(generated, catalog, output)
            current = generated[names[0]]
            with tempfile.TemporaryDirectory(prefix='lda-benchmark-') as directory:
                work = Path(directory)
                for t, n in cycle_window(languages):
                    source = work / t.filename
                    source.write_bytes(current)
                    current = execute(command_for(t.id, source, work), cwd=work)
                    if current != generated[n.id]:
                        raise AssertionError(f'{policy}/{order}/{strategy}: {t.id} -> {n.id}')
                    source.unlink()
                    for binary in work.glob('*-bin*'):
                        binary.unlink()
            if current != generated[names[0]] or link(stages, all_renderers=all_renderers) != generated:
                raise AssertionError('closure or deterministic build failed')
            row = dict(renderer_policy=policy, order=order, cycle=names, variant=strategy,
                       total_bytes=sum(map(len, generated.values())),
                       per_language={k: len(v) for k, v in generated.items()},
                       executed_hops=len(languages),
                       sha256={k: hashlib.sha256(v).hexdigest() for k, v in generated.items()})
            results.append(row)
            (here / f'results_{policy}.json').write_text(json.dumps(results, indent=2) + '\n')
            print(policy, order, strategy, row['total_bytes'], 'bytes; cycle PASS', flush=True)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all-renderers', action='store_true')
    parser.add_argument('--strategy', choices=STRATEGIES)
    parser.add_argument('--order', choices=('manifest', 'sorted', 'random42'))
    args = parser.parse_args()
    run(args.all_renderers, (args.strategy,) if args.strategy else STRATEGIES, args.order)
