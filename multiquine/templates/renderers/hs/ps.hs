render "ps" s = "'" ++ concatMap (\c -> if c == '\'' then "''" else [c]) s ++ "'"
