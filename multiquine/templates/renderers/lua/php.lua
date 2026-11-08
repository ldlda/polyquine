RENDERERS.php = function(s)
    s = s:gsub('\\', function() return '\\\\' end)
    s = s:gsub("'", function() return "\\'" end)
    return "'" .. s .. "'"
end
