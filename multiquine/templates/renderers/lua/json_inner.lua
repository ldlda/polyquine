-- LDA_REQUIRES: json
RENDERERS.json_inner = function(s) return RENDERERS.json(s):sub(2, -2) end
