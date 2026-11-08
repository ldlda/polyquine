"""Select an ordered cycle; independent of rendering and file generation."""

import json
import random
import re
from pathlib import Path


def validate_cycle(cycle, known):
    if not cycle or any(
        not isinstance(lang, str) or lang not in known for lang in cycle
    ):
        raise ValueError(f"cycle must contain language IDs from: {', '.join(known)}")
    if len(set(cycle)) != len(cycle):
        raise ValueError("each language must occur once in a cycle")
    return tuple(cycle)


def read_cycle(path):
    text = Path(path).read_text(encoding="utf-8")
    if text.lstrip().startswith("["):
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON cycle: {error}") from error
    text = "\n".join(line.split("#", 1)[0] for line in text.splitlines())
    return re.split(r"[,\s]+", text.strip()) if text.strip() else []


def choose_cycle(languages, known, explicit=None, file=None, order="set", seed=None):
    if explicit is not None and file is not None:
        raise ValueError("choose --cycle or --cycle-file, not both")
    if seed is not None and order != "random":
        raise ValueError("--seed requires --order random")
    if file is not None:
        cycle = read_cycle(file)
    else:
        text = explicit if explicit is not None else languages
        cycle = [part.strip() for part in text.split(",")]
    cycle = list(validate_cycle(cycle, known))
    if order == "sorted":
        cycle.sort()
    elif order == "random":
        random.Random(seed).shuffle(cycle)
    elif order != "set":
        raise ValueError(f"unknown order: {order}")
    return tuple(cycle)


def cycle_window(items):
    items = tuple(items)
    return zip(items, items[1:] + items[:1])
