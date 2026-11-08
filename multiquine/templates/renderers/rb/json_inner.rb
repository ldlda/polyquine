# LDA_REQUIRES: json
RENDERERS["json_inner"] = ->(s) { RENDERERS["json"].call(s)[1...-1] }
