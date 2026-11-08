    fn json(s: &str) -> String {
        let mut out = String::from("\"");
        for c in s.encode_utf16() {
            match c {
                34 => out.push_str("\\\""),
                92 => out.push_str("\\\\"),
                8 => out.push_str("\\b"),
                9 => out.push_str("\\t"),
                10 => out.push_str("\\n"),
                12 => out.push_str("\\f"),
                13 => out.push_str("\\r"),
                32..=126 => out.push(char::from_u32(c as u32).unwrap()),
                _ => out.push_str(&format!("\\u{:04x}", c)),
            }
        }
        out.push('"');
        out
    }
    renderers.insert("json", json);
