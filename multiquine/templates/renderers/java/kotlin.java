// LDA_REQUIRES: json
    static { RENDERERS.put("kotlin", s -> RENDERERS.get("json").apply(s).replace("$", "\\$")); }
