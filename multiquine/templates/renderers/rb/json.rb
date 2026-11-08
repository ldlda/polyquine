def as_json(s)
  JSON.generate(s, ascii_only: true).gsub("\x7f") { '\\u007f' }
end
RENDERERS["json"] = method(:as_json)
