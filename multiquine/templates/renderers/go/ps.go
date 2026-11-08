func quotePowerShell(s string) string {
    return "'" + regexp.MustCompile(`'`).ReplaceAllString(s, "''") + "'"
}
func init() { renderers["ps"] = quotePowerShell }
