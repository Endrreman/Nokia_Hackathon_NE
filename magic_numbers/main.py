import os
import sys

def next_palindrome(n: int) -> int:
    s = str(n + 1)
    length = len(s)
    h = length >> 1
    split = h + (length & 1)
    front = s[:split]
    tail = front[:h][::-1]
    
    if (m := front + tail) >= s: 
        return int(m)
    
    fi = str(int(front) + 1)
    
    if len(fi) > split: 
        return 10**length + 1
    
    return int(fi + fi[:h][::-1])


def main():
    _p = "input.txt"
    fd = os.open(_p, os.O_RDONLY | os.O_BINARY)
    
    try:
        raw = os.read(fd, os.path.getsize(_p))
    finally:
        os.close(fd)
        
    _np = next_palindrome
    results = []
    
    for s in raw.decode("utf-8").splitlines():
        try:
            if "^" in s:
                a, _, b = s.partition("^")
                n = int(a) ** int(b)
            else:
                n = int(s)
            results.append(str(_np(n)))
        except (ValueError, ArithmeticError):
            pass
    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()