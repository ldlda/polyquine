// LDA_REQUIRES: json
static Text json_contents(Text source) {
    Text quoted = get_renderer("json")(source);
    memmove(quoted.data, quoted.data + 1, quoted.len - 2);
    quoted.len -= 2; quoted.data[quoted.len] = '\0';
    return quoted;
}
#define LDA_ENTRY_json_inner {"json_inner", json_contents}
