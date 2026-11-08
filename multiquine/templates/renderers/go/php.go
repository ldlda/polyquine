func quotePHP(s string) string {
    s = regexp.MustCompile(`\\`).ReplaceAllStringFunc(s, func(string) string { return `\\` })
    s = regexp.MustCompile(`'`).ReplaceAllStringFunc(s, func(string) string { return `\'` })
    return "'" + s + "'"
}
func init() { renderers["php"] = quotePHP }
