import os

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