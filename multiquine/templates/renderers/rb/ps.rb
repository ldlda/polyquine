def as_powershell(s)
  "'" + s.gsub("'", "''") + "'"
end
RENDERERS["ps"] = method(:as_powershell)
