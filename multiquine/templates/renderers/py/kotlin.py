# LDA_REQUIRES: json
RENDERERS["kotlin"] = lambda s: RENDERERS["json"](s).replace("$", "\\$")
