RENDERERS['php'] = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
