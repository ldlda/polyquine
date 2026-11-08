static Text json_quote(Text source) {
    Buffer result = {0};
    append(&result, "\"", 1);
    for (size_t i = 0; i < source.len; ++i) {
        unsigned char c = (unsigned char)source.data[i];
        const char *escape = NULL;
        switch (c) {
            case '"': escape = "\\\""; break;
            case '\\': escape = "\\\\"; break;
            case '\b': escape = "\\b"; break;
            case '\t': escape = "\\t"; break;
            case '\n': escape = "\\n"; break;
            case '\f': escape = "\\f"; break;
            case '\r': escape = "\\r"; break;
        }
        if (escape) append(&result, escape, strlen(escape));
        else if (c < 32 || c > 126) {
            char encoded[7];
            snprintf(encoded, sizeof encoded, "\\u%04x", (unsigned)c);
            append(&result, encoded, 6);
        } else append(&result, source.data + i, 1);
    }
    append(&result, "\"", 1);
    return finish(&result);
}
#define LDA_ENTRY_json {"json", json_quote}
