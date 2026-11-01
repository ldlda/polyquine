#[doc = r#"
rust = r"""
"#]
fn main() {
    let (head, body) = ("#[doc = r#\"\nrust = r\"\"\"\n\"#]\nfn main() {\n    let (head, body) = ", ";\n    println!(\"{head}{:?}{body}{REAL}\\\"#;\", (head, body))\n}\nconst REAL: &str = r#\"");
    println!("{head}{:?}{body}{REAL}\"#;", (head, body))
}
const REAL: &str = r#"""
p = """{0}
rust = r{2}{1}{2}
p = {2}{3}{2}
print(p.format({0!r}, rust, {2!r}, p))
#{2:.1}#;"""
print(p.format('#[doc = r#"', rust, '"""', p))
#"#;
