AUTHOR = "lda@ldlda.com"

trix = {AUTHOR: (1) // int((int_escape:="""1
        .valueOf(),
    code: String.raw`
}; /*""")[0])}

def run(python_js):
    a = r"""AUTHOR = "{AUTHOR}"

trix = {{AUTHOR: (1) // int((int_escape:={t3q}{int_escape!s}{t3q})[0])}}

def run(python_js):
    a = r{t3q}{a}{t3q}
    print(a.format(AUTHOR=AUTHOR, int_escape=int_escape, t3q={t3q!r}, a=a, python_js=python_js))

python_js = r{t3q}{python_js}{t3q}
run(python_js)
# */ run();"""
    print(a.format(AUTHOR=AUTHOR, int_escape=int_escape, t3q='"""', a=a, python_js=python_js))

python_js = r"""`,
};

const t3q = '"'.repeat(3);
const cool = () => `AUTHOR = "${AUTHOR}"

trix = {AUTHOR: (1) // int((int_escape:=${t3q}1
        .valueOf(),
    code: String.raw\`${trix.code}\`,
};

const t3q = '"'.repeat(3);
const cool = ${cool}

const run = () => console.log(cool())
/* ${t3q}
run(python_js)
# */ run();`

const run = () => console.log(cool())
/* """
run(python_js)
# */ run();
