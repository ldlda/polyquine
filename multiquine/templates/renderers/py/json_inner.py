# LDA_REQUIRES: json
RENDERERS["json_inner"] = lambda s: RENDERERS["json"](s)[1:-1]
