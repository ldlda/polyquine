// LDA_REQUIRES: json
func init() {
    renderers["kotlin"] = func(s string) string {
        quoted := renderers["json"](s)
        result := make([]byte, 0, len(quoted))
        for i := 0; i < len(quoted); i++ {
            if quoted[i] == '$' { result = append(result, '\\') }
            result = append(result, quoted[i])
        }
        return string(result)
    }
}
