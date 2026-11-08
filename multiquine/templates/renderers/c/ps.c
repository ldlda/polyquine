static Text powershell_quote(Text source) {
    Buffer result = {0};
    append(&result, "'", 1);
    for (size_t i = 0; i < source.len; ++i) {
        append(&result, source.data + i, 1);
        if (source.data[i] == '\'') append(&result, "'", 1);
    }
    append(&result, "'", 1);
    return finish(&result);
}
#define LDA_ENTRY_ps {"ps", powershell_quote}
