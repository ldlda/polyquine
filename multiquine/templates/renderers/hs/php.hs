render "php" s = "'" ++ concatMap escape s ++ "'"
    where
        escape '\\' = "\\\\"
        escape '\'' = "\\'"
        escape c = [c]
