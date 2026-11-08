"""Build language skeletons, then close their shared seed in one link step."""

import json
import re
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from quote import RENDERERS
from strategies import STRATEGIES, Strategy

SLOT = '@@LDA_DATA@@'
SEPARATOR = '\n@@LDA_STAGE@@\n'
TOKEN = re.compile(r'LDA:([a-z][a-z0-9_]*):([a-z][a-z0-9_]*)')
REQUIRES = re.compile(
    r"\bLDA_REQUIRES:[ \t]*([a-z][a-z0-9_]*(?:[ \t]*,[ \t]*[a-z][a-z0-9_]*)*)[ \t]*,?[ \t]*$"
)


def renderer_dependencies(source):
    match = REQUIRES.search(source.partition('\n')[0])
    return tuple(name.strip() for name in match[1].split(',')) if match else ()


@dataclass(frozen=True)
class Language:
    id: str
    renderer: str
    directory: Path
    extension: str = ""

    @property
    def filename(self):
        return f'{self.id}.{self.extension or self.id}'

    def snippets(self, requested):
        ordered, visiting = {}, set()

        def visit(name):
            if name in visiting:
                raise ValueError(f'{self.id}: circular renderer dependency: {name}')
            if name in ordered:
                return
            if name not in RENDERERS:
                raise ValueError(f'unknown renderer: {name}')
            visiting.add(name)
            path = self.directory / 'renderers' / self.id / f'{name}.{self.id}'
            source = path.read_text(encoding='utf-8').rstrip('\n')
            for dependency in renderer_dependencies(source):
                visit(dependency)
            visiting.remove(name)
            ordered[name] = source

        for name in sorted(set(requested)):
            visit(name)
        return ordered

    def build(self, targets, strategy='packed_index'):
        targets = tuple(targets)
        if not targets or len({t.id for t in targets}) != len(targets):
            raise ValueError('targets must be nonempty and unique')
        selected = STRATEGIES.get(strategy)
        if selected is None:
            raise ValueError(f'unknown strategy: {strategy}')
        return Stage(self, targets, selected)


@dataclass(frozen=True)
class Stage:
    language: Language
    targets: tuple[Language, ...]
    strategy: Strategy

    def render(self, languages, *, all_renderers=False):
        languages = tuple(languages)
        requested = (
            languages
            if all_renderers or self.strategy.renderer_scope == 'sources'
            else self.targets
        )
        snippets = self.language.snippets(t.renderer for t in requested)
        env = Environment(
            loader=FileSystemLoader(self.language.directory),
            undefined=StrictUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        env.filters.update(
            file_import=lambda names: '\n\n'.join(snippets[name] for name in names),
            content=lambda t: f'LDA:{t.id}:{self.language.renderer}',
            content_as=lambda t, how: f'LDA:{t.id}:{how}',
        )
        source = env.get_template(f'{self.language.id}.j2').render(
            targets=self.targets,
            languages=languages,
            strategy=self.strategy,
            positions={t.id: i for i, t in enumerate(languages)},
            default=self.language if self.language in self.targets else self.targets[0],
            renderers=tuple(snippets),
            data=SLOT,
        )
        if not source.isascii() or SEPARATOR in source:
            raise ValueError(f'{self.language.id}: invalid source skeleton')
        if self.strategy.storage == 'packed' and source.count(SLOT) != 1:
            raise ValueError(f'{self.language.id}: expected exactly one seed slot')
        return source


def load_languages(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    result = {}
    for name, spec in manifest.items():
        if (
            not name.isascii()
            or not name.isidentifier()
            or spec['renderer'] not in RENDERERS
        ):
            raise ValueError(f'invalid language specification: {name}')
        result[name] = Language(
            name, spec['renderer'], directory / 'templates', spec.get('extension', name)
        )
    return result


def _validate_graph(stages):
    by_id = {stage.language.id: stage for stage in stages}
    if not stages or len(by_id) != len(stages):
        raise ValueError('stages must be nonempty and unique')
    storages = {stage.strategy.storage for stage in stages}
    if len(storages) != 1:
        raise ValueError('marker and packed strategies cannot share a graph')
    for stage in stages:
        for target in stage.targets:
            if target.id not in by_id or by_id[target.id].language != target:
                raise ValueError(
                    f'{stage.language.id}: missing or conflicting destination: {target.id}'
                )
    return storages.pop()


def _embed_markers(skeletons):
    def substitute(match):
        name, how = match.groups()
        if name not in skeletons or how not in RENDERERS:
            raise ValueError(f'bad source reference: {match[0]}')
        return RENDERERS[how](skeletons[name])

    return {
        name: TOKEN.sub(substitute, source).encode('utf-8')
        for name, source in skeletons.items()
    }


def _embed_seed(stages, skeletons):
    seed = SEPARATOR.join(skeletons.values())
    return {
        stage.language.id: skeletons[stage.language.id]
        .replace(SLOT, RENDERERS[stage.language.renderer](seed))
        .encode('utf-8')
        for stage in stages
    }


def link(stages, *, all_renderers=False):
    stages = tuple(stages)
    storage = _validate_graph(stages)
    languages = tuple(stage.language for stage in stages)
    skeletons = {
        stage.language.id: stage.render(languages, all_renderers=all_renderers)
        for stage in stages
    }
    if storage == 'marker':
        return _embed_markers(skeletons)
    return _embed_seed(stages, skeletons)


def write(generated, languages, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, source in generated.items():
        (directory / languages[name].filename).write_bytes(source)
