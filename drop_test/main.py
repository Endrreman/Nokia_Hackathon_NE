from pathlib import Path
from math import isqrt


def min_num_of_drops(n: int, h: int) -> int:
    if n == 1: 
        return h
    if n == 2: 
        return (isqrt(8 * h - 1) + 1) // 2
    if n == 3:
        h6 = 6 * h; t = round(h6 ** (1/3))
        while t * (t * t + 5) < h6: t += 1
        return t
    if n == 4:
        t = max(1, round((24 * h) ** 0.25)); h24 = 24 * h
        while t * ((t - 1) * ((t - 2) * (t + 1) + 12) + 24) < h24: t += 1
        return t
    
    p1 = h.bit_length()
    
    if p1 <= n: 
        return p1
    
    s = (1 << n) - 1; cn = 1
    
    for t in range(n + 1, h + 1):
        s = 1 + (s << 1) - cn
        if s >= h: 
            return t
        cn = cn * t // (t - n)
    
    return h


def main():
    _int = int
    for line in Path("input.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            a, _, b = line.partition(",")
            print(min_num_of_drops(_int(a), _int(b)))
        except (ValueError, TypeError):
            pass


if __name__ == "__main__":
    main()