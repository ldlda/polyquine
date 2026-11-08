function asJSON(value) {
    return JSON.stringify(value).replace(/\x7f/g, "\\u007f");
}
RENDERERS.json = asJSON;
