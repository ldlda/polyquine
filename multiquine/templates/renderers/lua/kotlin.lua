-- LDA_REQUIRES: json
RENDERERS.kotlin = function(s)
    return (RENDERERS.json(s):gsub('%$', function() return '\\$' end))
end
