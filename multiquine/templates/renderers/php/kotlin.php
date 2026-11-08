// LDA_REQUIRES: json
$RENDERERS['kotlin'] = fn($s) => str_replace('$', '\\$', $RENDERERS['json']($s));
