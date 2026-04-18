from pathlib import Path
from math import isqrt


def min_num_of_drops(n: int, h: int) -> int:
    # 1 drone:
    if n == 1:
        return h

    # 2 drones:
    if n == 2:
        return (isqrt(8 * h - 1) + 1) // 2

    # General case:
    if h.bit_length() <= n:
        return h.bit_length()

    running_sum = (1 << n) - 1
    cn = 1
    for t in range(n + 1, h + 1):
        running_sum = 1 + (running_sum << 1) - cn
        if running_sum >= h:
            return t
        cn = cn * t // (t - n)

    return h

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    for line in Path("input.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            n, _, h = line.partition(",")
            print(min_num_of_drops(int(n), int(h)))
        except (ValueError, TypeError):
            pass


if __name__ == "__main__":
    main()

#Az alábbi kód ugyanazt éri el, csak az os és sys modulokat használja a fájl olvasásához és írásához, valamint a standard output kezeléséhez.
#Ez egy (kb 2x) gyorsabb megközelítése a problémának, de a tesztszerver érthető okokból nem képes lefuttatni és errort dob, ezért a fenti kódot hagytam meg.
#Az if-ek pedig n=4 felett nem gyorsítenak de alatta jelentősen, ezért hagytam meg azokat is.

#import os
#import sys
#
#def min_num_of_drops(n: int, h: int) -> int:
#    # 1 drone:
#    if n == 1:
#        return h
#
#    # 2 drones:
#    if n == 2:
#        return (isqrt(8 * h - 1) + 1) // 2
#
#    # 3 drones:
#    if n == 3:
#        h6 = 6 * h
#        t = round(h6 ** (1 / 3))
#        while t * (t * t + 5) < h6:
#            t += 1
#        return t
#
#    # 4 drones:
#    if n == 4:
#        h24 = 24 * h
#        t = max(1, round((24 * h) ** 0.25))
#        while t * ((t - 1) * ((t - 2) * (t + 1) + 12) + 24) < h24:
#            t += 1
#        return t
#
#    # General case:
#    if h.bit_length() <= n:
#        return h.bit_length()
#
#    running_sum = (1 << n) - 1
#    cn = 1
#    for t in range(n + 1, h + 1):
#        running_sum = 1 + (running_sum << 1) - cn
#        if running_sum >= h:
#            return t
#        cn = cn * t // (t - n)
#
#    return h
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
#    _mnd = min_num_of_drops
#    results = []
#
#    for s in raw.decode("utf-8").splitlines():
#        s = s.strip()
#        if not s:
#            continue
#        try:
#            n, _, h = s.partition(",")
#            results.append(str(_mnd(int(n), int(h))))
#        except (ValueError, TypeError):
#            pass
#
#    sys.stdout.write("\n".join(results) + "\n")
#
#if __name__ == "__main__":
#    main()