$RENDERERS['json'] = fn($s) => str_replace("\x7f", '\\u007f', json_encode($s, JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR));
