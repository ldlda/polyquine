RENDERERS.json = function(s)
    local escapes = { ['"'] = '\\"', ['\\'] = '\\\\', ['\b'] = '\\b',
        ['\t'] = '\\t', ['\n'] = '\\n', ['\f'] = '\\f', ['\r'] = '\\r' }
    return '"' .. s:gsub('[%z\1-\31\127\\"]', function(c)
        return escapes[c] or string.format('\\u%04x', string.byte(c))
    end) .. '"'
end
