-- LDA_REQUIRES: json
render "json_inner" s = init (tail (render "json" s))
