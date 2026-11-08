"""Explicit configuration for template sections and renderer dependencies."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Strategy:
    name: str
    storage: str
    access: str
    renderer_scope: str = 'targets'
    renderer_binding: str = 'name'


STRATEGIES = {
    s.name: s
    for s in (
        Strategy('packed_index', 'packed', 'packed_index'),
        Strategy('packed_map', 'packed', 'packed_map'),
        Strategy('record_key', 'packed', 'record', renderer_scope='sources'),
        Strategy(
            'record_callable',
            'packed',
            'record',
            renderer_scope='sources',
            renderer_binding='callable',
        ),
        Strategy('marker_map', 'marker', 'marker'),
    )
}
