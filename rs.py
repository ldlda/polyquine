#[doc=r#"
rust=r"""#]fn main(){println!("{1}{1:?},{2:?}{2}{}\"#;",REAL,"#[doc=r#\"\nrust=r\"\"\"#]fn main(){println!(\"{1}{1:?},{2:?}{2}{}\\\"#;\",REAL,",")}\nconst REAL:&str=r#\"")}
const REAL:&str=r#""";p="""{0}
rust=r{2}{1}{2};p={2}{3}{2};print(p.format({0!r},rust,{2!r},p))#{2:.1}#;""";print(p.format('#[doc=r#"',rust,'"""',p))#"#;
