#/* /* */
#if 0
p = r"""
*/![doc = ""]
const C: &str = r##"
#endif
#include <stdio.h>
int main(void) {
    char* s = "#/* /* */%c#if 0%cp = r%c%c%c%c*/![doc = %c%c]%cconst C: &str = r##%c%c#endif%c#include <stdio.h>%cint main(void) {%c    char* s = %c%s%c;%c    printf(s, 10, 10, 34, 34, 34, 10, 34, 34, 10, 34, 10, 10, 10, 10, 34, s, 34, 10, 10, 10, 10, 34, 10, 10, 10, 34, 92, 92, 92, 34, 34, 10, 34, 92, 92, 92, 34, 92, 34, 92, 34, 92, 92, 34, 92, 34, 92, 92, 34, 34, 10, 34, 92, 34, 92, 92, 92, 92, 34, 92, 92, 92, 92, 92, 92, 92, 34, 92, 34, 92, 34, 10, 34, 92, 92, 92, 92, 34, 34, 10, 10, 10, 34, 10, 34, 34, 34, 10, 92, 92, 92, 92, 92, 10, 34, 34, 34, 10, 34, 10);%c}%c#if 0%c%c##;%cfn main() {%c    println!(%c        %c{0}{C}{1}{0:?},%cn        {1:?},%cn        {2:?}{2}{PYTHON}%c%c##;%c,%c        %c#/* /* */%cn#if 0%cnp = r%c%c%c%c%c%c%cn*/![doc = %c%c%c%c]%cnconst C: &str = r##%c%c%c,%c        %c%c%c##;%cnfn main() {%cn    println!(%cn        %c%c{0}{C}{1}{0:?},%c%cn        {1:?},%c%cn        {2:?}{2}{PYTHON}%c%c%c%c##;%c%c,%cn        %c,%c        %c,%cn    )%cn}%cnconst PYTHON: &str = r##%c%c%c,%c    )%c}%cconst PYTHON: &str = r##%c%c%c%c%c%ci = '#/* /* */%cn#if 0%cnp = r{2}{0}{2}%cni = {1!r}%cnprint(i.format(p, i, {2!r}))%cn#endif // {2:.1}##;'%cprint(i.format(p, i, '%c%c%c'))%c#endif // %c##;%c";
    printf(s, 10, 10, 34, 34, 34, 10, 34, 34, 10, 34, 10, 10, 10, 10, 34, s, 34, 10, 10, 10, 10, 34, 10, 10, 10, 34, 92, 92, 92, 34, 34, 10, 34, 92, 92, 92, 34, 92, 34, 92, 34, 92, 92, 34, 92, 34, 92, 92, 34, 34, 10, 34, 92, 34, 92, 92, 92, 92, 34, 92, 92, 92, 92, 92, 92, 92, 34, 92, 34, 92, 34, 10, 34, 92, 92, 92, 92, 34, 34, 10, 10, 10, 34, 10, 34, 34, 34, 10, 92, 92, 92, 92, 92, 10, 34, 34, 34, 10, 34, 10);
}
#if 0
"##;
fn main() {
    println!(
        "{0}{C}{1}{0:?},\n        {1:?},\n        {2:?}{2}{PYTHON}\"##;",
        "#/* /* */\n#if 0\np = r\"\"\"\n*/![doc = \"\"]\nconst C: &str = r##\"",
        "\"##;\nfn main() {\n    println!(\n        \"{0}{C}{1}{0:?},\\n        {1:?},\\n        {2:?}{2}{PYTHON}\\\"##;\",\n        ",
        ",\n    )\n}\nconst PYTHON: &str = r##\"",
    )
}
const PYTHON: &str = r##"
"""
i = '#/* /* */\n#if 0\np = r{2}{0}{2}\ni = {1!r}\nprint(i.format(p, i, {2!r}))\n#endif // {2:.1}##;'
print(i.format(p, i, '"""'))
#endif // "##;
