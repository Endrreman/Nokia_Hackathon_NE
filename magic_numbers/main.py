from pathlib import Path


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
    for s in Path("input.txt").read_text(encoding="utf-8").splitlines():
        try:
            if "^" in s:
                a, _, b = s.partition("^")
                n = int(a) ** int(b)
            else:
                n = int(s)
            print(next_palindrome(n))
        except (ValueError, ArithmeticError):
            pass


if __name__ == "__main__":
    main()