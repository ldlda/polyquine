# LDA_REQUIRES: json
RENDERERS["kotlin"] = ->(s) { RENDERERS["json"].call(s).gsub('$') { '\\$' } }
