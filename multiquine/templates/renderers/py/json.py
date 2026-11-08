def as_json(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))

RENDERERS["json"] = as_json
