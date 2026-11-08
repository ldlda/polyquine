function asPowerShell(s) { return "'" + s.replace(/'/g, "''") + "'"; }
RENDERERS.ps = asPowerShell;
