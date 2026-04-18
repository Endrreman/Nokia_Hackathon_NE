from pathlib import Path


def next_palindrome(n: int) -> int:
    digits = str(n + 1)
    length = len(digits)
    half = length >> 1
    mid = half + (length & 1)
    front = digits[:mid]
    mirrored = front + front[:half][::-1]

    if mirrored >= digits:
        return int(mirrored)

    incremented = str(int(front) + 1)

    if len(incremented) > mid:
        return 10**length + 1

    return int(incremented + incremented[:half][::-1])

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    for line in Path("input.txt").read_text(encoding="utf-8").splitlines():
        try:
            if "^" in line:
                base, _, exp = line.partition("^")
                n = int(base) ** int(exp)
            else:
                n = int(line)
            print(next_palindrome(n))
        except (ValueError, ArithmeticError):
            pass


if __name__ == "__main__":
    main()
    
#Az alábbi kód ugyanazt éri el, csak az os és sys modulokat használja a fájl olvasásához és írásához, valamint a standard output kezeléséhez.
#Ez egy (kb 2x) gyorsabb megközelítése a problémának, de a tesztszerver érthető okokból nem képes lefuttatni és errort dob, ezért a fenti kódot hagytam meg.

#import os
#import sys
#
#def next_palindrome(n: int) -> int:
#    s = str(n + 1)
#    length = len(s)
#    h = length >> 1
#    split = h + (length & 1)
#    front = s[:split]
#    tail = front[:h][::-1]
#    
#    if (m := front + tail) >= s: 
#        return int(m)
#    
#    fi = str(int(front) + 1)
#    
#    if len(fi) > split: 
#        return 10**length + 1
#    
#    return int(fi + fi[:h][::-1])
#
#def main():
#    _p = "input.txt"
#    fd = os.open(_p, os.O_RDONLY | os.O_BINARY)
#    
#    try:
#        raw = os.read(fd, os.path.getsize(_p))
#    finally:
#        os.close(fd)
#        
#    _np = next_palindrome
#    results = []
#    
#    for s in raw.decode("utf-8").splitlines():
#        try:
#            if "^" in s:
#                a, _, b = s.partition("^")
#                n = int(a) ** int(b)
#            else:
#                n = int(s)
#            results.append(str(_np(n)))
#        except (ValueError, ArithmeticError):
#            pass
#    sys.stdout.write("\n".join(results) + "\n")
#
#if __name__ == "__main__":
#    main()