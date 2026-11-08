private val psRegistration = run {
    RENDERERS["ps"] = { s -> "'" + s.replace("'", "''") + "'" }
}
