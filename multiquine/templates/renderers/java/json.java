    static String json(String s) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"': out.append("\\\""); break;
                case '\\': out.append("\\\\"); break;
                case '\b': out.append("\\b"); break;
                case '\t': out.append("\\t"); break;
                case '\n': out.append("\\n"); break;
                case '\f': out.append("\\f"); break;
                case '\r': out.append("\\r"); break;
                default:
                    if (c < 32 || c > 126) out.append(String.format("\\u%04x", (int)c));
                    else out.append(c);
            }
        }
        return out.append('"').toString();
    }
    static { RENDERERS.put("json", Main::json); }
