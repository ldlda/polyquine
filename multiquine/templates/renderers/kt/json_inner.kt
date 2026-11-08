// LDA_REQUIRES: json
private val jsonInnerRegistration = run {
    RENDERERS["json_inner"] = { s -> RENDERERS.getValue("json")(s).drop(1).dropLast(1) }
}
