    renderers.insert("php", |s| format!("'{}'", s.replace("\\", "\\\\").replace("'", "\\'")));
