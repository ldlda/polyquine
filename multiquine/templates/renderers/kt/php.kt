private val phpRegistration = run {
    RENDERERS["php"] = { s -> "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'" }
}
