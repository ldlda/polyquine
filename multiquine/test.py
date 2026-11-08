"""Execute emitted programs and compare their stdout bytes, including relay hops."""

import argparse
import json
import tempfile
from pathlib import Path

from cycles import choose_cycle, cycle_window
from lda import Language, link, load_languages, write
from runtime import available, command_for, execute


def equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(label)


def network(languages, work, strategy='packed_index'):
    generated = link(t.build(languages, strategy=strategy) for t in languages)
    write(generated, {t.id: t for t in languages}, work)
    count = 0
    for t in languages:
        command = command_for(t.id, work / t.filename, work)
        for target in languages:
            equal(
                execute(command, [target.id]),
                generated[target.id],
                f'{t.id} -> {target.id}',
            )
            count += 1
        equal(execute(command), generated[t.id], f'{t.id} default self-quine')
        count += 1
    equal(
        link(t.build(languages, strategy=strategy) for t in languages),
        generated,
        'deterministic network',
    )
    print(f'PASS network: {",".join(t.id for t in languages)} ({count} executions)')
    return generated, count


def relay(languages, work, laps=1, strategy='packed_index'):
    stages = [t.build([n], strategy=strategy) for t, n in cycle_window(languages)]
    generated = link(stages)
    equal(link(stages), generated, 'deterministic link')
    equal(
        link(t.build([n], strategy=strategy) for t, n in cycle_window(languages)),
        generated,
        'deterministic skeleton builds',
    )
    current = generated[languages[0].id]
    for i in range(len(languages) * laps):
        t, n = languages[i % len(languages)], languages[(i + 1) % len(languages)]
        source = work / t.filename
        source.write_bytes(current)
        current = execute(command_for(t.id, source, work), cwd=work)
        equal(current, generated[n.id], f'ring hop {i + 1}: {t.id} -> {n.id}')
        source.unlink()
        for binary in work.glob('*-bin*'):
            binary.unlink()
    equal(current, generated[languages[0].id], 'cycle closure')
    print(f'PASS ring: {" -> ".join(t.id for t in languages)} ({laps} laps)')
    return generated, len(languages) * laps


def contracts(catalog, work):
    ids = tuple(catalog)
    csv = ','.join(ids)
    equal(choose_cycle(csv, catalog), ids, 'explicit order')
    equal(
        choose_cycle(csv, catalog, order='sorted'), tuple(sorted(ids)), 'sorted order'
    )
    equal(
        choose_cycle(csv, catalog, order='random', seed=42),
        choose_cycle(csv, catalog, order='random', seed=42),
        'seeded order',
    )
    file = work / 'cycle.json'
    file.write_text(json.dumps(list(reversed(ids))), encoding='utf-8')
    from_file = choose_cycle(csv, catalog, file=file)
    equal(from_file, tuple(reversed(ids)), 'JSON file order')
    file.write_text('# comment\n' + ',\n'.join(ids), encoding='utf-8')
    equal(choose_cycle(csv, catalog, file=file), ids, 'text file order')
    for invalid in ('', 'py,py', 'unknown'):
        try:
            choose_cycle(invalid, catalog)
        except ValueError:
            pass
        else:
            raise AssertionError(f'invalid cycle accepted: {invalid}')
    directory = work / 'fixtures'
    snippets = directory / 'renderers' / 'py'
    snippets.mkdir(parents=True)
    (snippets / 'json.py').write_text('-- LDA_REQUIRES: ps,\n', encoding='utf-8')
    dependency = snippets / 'ps.py'
    dependency.write_text('# dependency\n', encoding='utf-8')
    fixture = Language('py', 'json', directory)
    equal(tuple(fixture.snippets(['json'])), ('ps', 'json'), 'dependency-first order')
    for text, error in [
        ('# LDA_REQUIRES: json\n', ValueError),
        (None, FileNotFoundError),
        ('# LDA_REQUIRES: unknown\n', ValueError),
    ]:
        if text is None:
            dependency.unlink()
        else:
            dependency.write_text(text, encoding='utf-8')
        try:
            fixture.snippets(['json'])
        except error:
            pass
        else:
            raise AssertionError('invalid dependency accepted')
    first, second = catalog['py'], catalog['rs']
    try:
        link([first.build([second])])
    except ValueError:
        pass
    else:
        raise AssertionError('missing graph destination accepted')
    # Linking may reorder stages; indices are resolved by identity, not build order.
    stages = [first.build([second]), second.build([first])]
    generated = link(reversed(stages))
    path = work / first.filename
    path.write_bytes(generated[first.id])
    equal(
        execute(command_for(first.id, path, work)),
        generated[second.id],
        'reordered link',
    )
    print(
        'PASS order parsing, dependency failures, missing destination, reordered linking'
    )
    return from_file


def branching(catalog, work, strategy='packed_index'):
    py, rs, php = (catalog[name] for name in ('py', 'rs', 'php'))
    generated = link(
        [
            py.build([rs, php], strategy=strategy),
            rs.build([py], strategy=strategy),
            php.build([rs], strategy=strategy),
        ]
    )
    write(generated, catalog, work)
    edges = [(py, rs), (py, php), (rs, py), (php, rs)]
    for source, target in edges:
        command = command_for(source.id, work / source.filename, work)
        equal(
            execute(command, [target.id]),
            generated[target.id],
            f'mixed graph: {source.id} -> {target.id}',
        )
    command = command_for(py.id, work / py.filename, work)
    try:
        execute(command, ['py'])
    except RuntimeError:
        pass
    else:
        raise AssertionError('unconfigured destination accepted')
    print(
        'PASS mixed graph: 4 executed edges and rejection of unconfigured destination'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-all', action='store_true')
    parser.add_argument('--mode', choices=('all', 'network', 'ring'), default='all')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    catalog = load_languages(root)
    missing = [name for name in catalog if not available(name)]
    if missing and (args.require_all or any(name != 'ps' for name in missing)):
        parser.error('missing runtimes: ' + ', '.join(missing))
    for name in missing:
        print('SKIP missing runtime:', name)
        del catalog[name]
    languages = list(catalog.values())
    with tempfile.TemporaryDirectory(prefix='lda-tests-') as directory:
        work = Path(directory)
        from_file = contracts(catalog, work)
        branching(catalog, work)
        if args.mode in ('all', 'network'):
            subsets = [
                tuple(catalog),
                ('py', 'js'),
                ('go', 'ps'),
                ('py',),
                ('rb', 'py'),
                ('ps',),
                ('rs',),
                ('php',),
                ('rs', 'php'),
                ('py', 'rs', 'php'),
            ]
            count = 0
            for subset in subsets:
                selected = [catalog[name] for name in subset if name in catalog]
                if selected:
                    _, n = network(selected, work)
                    count += n
            print(f'ALL NETWORK PASS: {count} executions')
        if args.mode in ('all', 'ring'):
            _, hops = relay(languages, work, laps=2)
            for ids in [
                sorted(catalog),
                choose_cycle(','.join(catalog), catalog, order='random', seed=1729),
                from_file,
            ]:
                _, n = relay([catalog[name] for name in ids], work)
                hops += n
            for t in languages:
                _, n = relay([t], work, laps=2)
                hops += n
            print(f'ALL RINGS PASS: {hops} executed hops')
    # Deliver default outputs using the exact same build/link API tested above.
    full = link(t.build(languages) for t in languages)
    slim = link(t.build([n]) for t, n in cycle_window(languages))
    write(full, catalog, root / 'out')
    write(slim, catalog, root / 'out-ring')
    (root / 'out-ring' / 'cycle.json').write_text(
        json.dumps(list(catalog), indent=2) + '\n', encoding='utf-8'
    )
    print(
        f'SIZE: network {sum(map(len, full.values()))}, ring {sum(map(len, slim.values()))} bytes'
    )


if __name__ == '__main__':
    main()
