private fun jsonQuote(s: String): String = buildString {
    append('"')
    for (c in s) {
        when (c) {
            '"' -> append("\\\"")
            '\\' -> append("\\\\")
            '\b' -> append("\\b")
            '\t' -> append("\\t")
            '\n' -> append("\\n")
            '\u000C' -> append("\\f")
            '\r' -> append("\\r")
            else -> if (c.code < 32 || c.code > 126) append("\\u%04x".format(c.code)) else append(c)
        }
    }
    append('"')
}
private val jsonRegistration = run { RENDERERS["json"] = ::jsonQuote }
