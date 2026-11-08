    static { RENDERERS.put("php", s -> "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"); }
