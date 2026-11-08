RENDERERS['php'] = ->(s) { "'" + s.gsub("\\") { "\\\\" }.gsub("'") { "\\'" } + "'" }
