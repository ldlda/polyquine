// LDA_REQUIRES: json
    renderers.insert("kotlin", |s| json(s).replace('$', "\\$"));
