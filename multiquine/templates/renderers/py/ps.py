def as_powershell(s):
    return "'" + s.replace("'", "''") + "'"

RENDERERS["ps"] = as_powershell
