// LDA_REQUIRES: json
    static { RENDERERS.put("json_inner", s -> {
        String quoted = RENDERERS.get("json").apply(s);
        return quoted.substring(1, quoted.length() - 1);
    }); }
