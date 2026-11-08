"""Verify the new native encoders against bootstrap output on ASCII edge cases."""

import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from lda import load_languages
from quote import RENDERERS
from runtime import command_for, execute


def main():
    root = Path(__file__).resolve().parent
    catalog = load_languages(root)
    env = Environment(
        loader=FileSystemLoader(root),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    samples = [
        '',
        "don't \\",
        '"$x @ARGV `tick` % \\ end',
        ''.join(map(chr, range(128))),
        '@@LDA_DATA@@\n@@LDA_STAGE@@\nLDA:py:json',
    ]
    count = 0
    with tempfile.TemporaryDirectory(prefix='lda-native-quotes-') as directory:
        work = Path(directory)
        for name in catalog:
            language = catalog[name]
            for how in RENDERERS:
                definitions = language.snippets([how])
                source = work / language.filename
                source.write_text(
                    env.get_template(f'tests/renderers.{name}.j2').render(
                        snippets='\n\n'.join(definitions.values()),
                        renderers=tuple(definitions),
                        how=how,
                    ),
                    encoding='utf-8',
                )
                command = command_for(name, source, work)
                for value in samples:
                    got = execute(command, input_bytes=value.encode('ascii'))
                    if got != RENDERERS[how](value).encode('utf-8'):
                        raise AssertionError((name, how, repr(value), got))
                    count += 1
    print(f'ALL QUOTING PASS: {count} actual native executions across all emitters')


if __name__ == '__main__':
    main()
