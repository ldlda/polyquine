// LDA_REQUIRES: json
private val kotlinRegistration = run {
    RENDERERS["kotlin"] = { s -> RENDERERS.getValue("json")(s).replace('$'.toString(), "\\" + '$') }
}
