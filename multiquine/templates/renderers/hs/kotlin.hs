-- LDA_REQUIRES: json
render "kotlin" s = concatMap (\c -> if c == '$' then "\\$" else [c]) (render "json" s)
