// LDA_REQUIRES: json
func init() {
    renderers["json_inner"] = func(s string) string {
        quoted := renderers["json"](s)
        return quoted[1:len(quoted)-1]
    }
}
