static Text single_quote(Text source) {
    Buffer result = {0};
    append(&result, "'", 1);
    for (size_t i = 0; i < source.len; ++i) {
        if (source.data[i] == '\\' || source.data[i] == '\'') append(&result, "\\", 1);
        append(&result, source.data + i, 1);
    }
    append(&result, "'", 1);
    return finish(&result);
}
#define LDA_ENTRY_php {"php", single_quote}
