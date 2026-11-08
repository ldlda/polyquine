render "json" s = "\"" ++ concatMap escape s ++ "\""
    where
        escape c = case c of
            '"' -> "\\\""
            '\\' -> "\\\\"
            '\b' -> "\\b"
            '\t' -> "\\t"
            '\n' -> "\\n"
            '\f' -> "\\f"
            '\r' -> "\\r"
            _ | ord c < 32 || ord c > 126 -> let h = showHex (ord c) "" in "\\u" ++ replicate (4 - length h) '0' ++ h
              | otherwise -> [c]
