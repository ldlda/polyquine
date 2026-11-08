"""Bootstrap string renderers. Keep these byte-equivalent to runtime snippets."""

import json


def json_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def json_inner(value: str) -> str:
    return RENDERERS["json"](value)[1:-1]


def ps_string(value: str) -> str:
    """PowerShell single-quoted literal: only apostrophes need doubling."""
    return "'" + value.replace("'", "''") + "'"


RENDERERS = {
    "json": json_string,
    "json_inner": json_inner,
    "ps": ps_string,
}


def php_string(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


RENDERERS["php"] = php_string


def kotlin_string(value: str) -> str:
    return RENDERERS["json"](value).replace("$", "\\$")


RENDERERS["kotlin"] = kotlin_string
