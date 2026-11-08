func quoteForJSON(s string) string {
    quoted := strconv.Quote(s)
    result := make([]byte, 0, len(quoted))
    for i := 0; i < len(quoted); i++ {
        if quoted[i] != '\\' || i+1 >= len(quoted) {
            result = append(result, quoted[i])
            continue
        }
        switch quoted[i+1] {
        case 'a':
            result = append(result, "\\u0007"...)
            i++
        case 'v':
            result = append(result, "\\u000b"...)
            i++
        case 'x':
            result = append(result, "\\u00"...)
            result = append(result, quoted[i+2], quoted[i+3])
            i += 3
        default:
            result = append(result, quoted[i], quoted[i+1])
            i++
        }
    }
    return string(result)
}
func init() { renderers["json"] = quoteForJSON }
