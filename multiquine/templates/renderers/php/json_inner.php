// LDA_REQUIRES: json
$RENDERERS['json_inner'] = fn($s) => substr($RENDERERS['json']($s), 1, -1);
