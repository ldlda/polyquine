// LDA_REQUIRES: json
static Text kotlin_quote(Text source) {
    Text quoted = get_renderer("json")(source);
    Text result = replace_text(quoted, "$", text("\\$"));
    free(quoted.data);
    return result;
}
#define LDA_ENTRY_kotlin {"kotlin", kotlin_quote}
