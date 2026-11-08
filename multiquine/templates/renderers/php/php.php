$RENDERERS['php'] = fn($s) => "'" . str_replace(["\\", "'"], ["\\\\", "\\'"], $s) . "'";
