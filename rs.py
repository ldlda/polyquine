#![doc = r#"
rust = r"""
"#]
fn main() {
    let (head, body) = ("#![doc = r#\"\nrust = r\"\"\"\n\"#]\nfn main() {\n    let (head, body) = ", "    println!(\"{head}({head:?}, {body:?});\\n{body}{REAL}\\\"#;\");\n}\nconst REAL: &'static str = r#\"");
    println!("{head}({head:?}, {body:?});\n{body}{REAL}\"#;");
}
const REAL: &'static str = r#"""
p = """{d}
rust = r{triple}{rust}{triple}
p = {triple}{p}{triple}
print(p.format(p=p, d={d!r}, rust=rust, triple={triple!r}))
{triple}
{triple}#;"""
print(p.format(p=p, d='#![doc = r#"', rust=rust, triple='"""'))
"""
"""#;
