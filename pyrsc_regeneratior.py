"""for pyrs.c

Replace the char* s and the printf line with `$` and `@` respectively, then run this script to generate both lines. Then copy that and replace the `$...@` range (inclusive) with them.
"""


LIST = '\\\n"%'


def take(s):
    r = []
    n = []
    for c in s:
        if c in LIST:
            n.append("%c")
            r.append(ord(c))
        else:
            if c in "$":
                r.extend([ord('"'), "s", ord('"')])
            n.append(c)
    return r, "".join(n)



def proc(s):
    r, n = take(s)
    a = n.index("$")
    b = n.index("@")
    assert a < b
    chars = "char* s = %c%s%c;"
    printf = f"printf(s, {', '.join(map(str, r))});"
    a = n[:a] + chars + n[a + 1:b] + printf + n[b + 1 :]
    return a, printf

if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            s = f.read()
    else:
        s = sys.stdin.read()
    a, p = proc(s)
    print(f"char* s = {json.dumps(a)};")
    print(f"    {p}")
