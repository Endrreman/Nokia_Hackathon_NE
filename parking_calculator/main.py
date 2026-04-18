from datetime import datetime
from pathlib import Path

# ── Pricing constants ─────────────────────────────────────────────────────────
_FREE_MINUTES  = 30        # first 30 minutes free — first day only
_CHEAP_HOURS   = 3         # cheap-rate hours
_CHEAP_RATE    = 300       # HUF per started hour (first 3 billable hours)
_EXP_RATE      = 500       # HUF per started hour (beyond first 3)
_DAILY_CAP     = 10_000    # daily cap
_DAY_MINUTES   = 1440      # minutes in 24 h


# ── Fee calculation ───────────────────────────────────────────────────────────

def _day_fees(minutes: int, free_minutes: int = 0) -> tuple:
    billable        = max(0, minutes - free_minutes)
    billable_hours  = -(-billable // 60)
    cheap_hours     = min(billable_hours, _CHEAP_HOURS)
    fee_h           = min(_DAILY_CAP, cheap_hours * _CHEAP_RATE + (billable_hours - cheap_hours) * _EXP_RATE)
    cheap_min       = min(billable, _CHEAP_HOURS * 60)
    exp_min         = billable - cheap_min
    fee_min         = min(_DAILY_CAP, (cheap_min * _CHEAP_RATE + exp_min * _EXP_RATE + 30) // 60)
    return fee_h, fee_min

def calculate_fees(total_minutes: int) -> tuple:
    full_days  = total_minutes // _DAY_MINUTES
    remainder  = total_minutes - full_days * _DAY_MINUTES
    h, m       = _day_fees(remainder, _FREE_MINUTES if full_days == 0 else 0)
    return full_days * _DAILY_CAP + h, full_days * _DAILY_CAP + m


# ── Input parsing ─────────────────────────────────────────────────────────────

def parse_line(line: str):
    parts = line.split()
    if len(parts) != 5:
        raise ValueError(f"expected 5 fields, got {len(parts)}")
    plate = parts[0]
    entry = datetime.fromisoformat(parts[1] + " " + parts[2])
    exit = datetime.fromisoformat(parts[3] + " " + parts[4])
    return plate, entry, exit


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()

    rows = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("=") or line.upper().startswith("RENDSZAM"):
            continue

        try:
            plate, entry, exit = parse_line(line)
        except ValueError as e:
            rows.append(f"{'INVALID':<10} | {e}")
            continue

        if exit < entry:
            rows.append(f"{plate:<10} | ERROR: exit before entry")
            continue

        total_minutes = int((exit - entry).total_seconds() // 60)
        fee_h, fee_min = calculate_fees(total_minutes)
        rows.append(f"{plate:<10} | {fee_h:>11} HUF | {fee_min:>11} HUF")

    header    = f"{'Plate':<10} | {'Fee (started h)':>12} | {'Fee (exact min)':>14}"
    separator = "-" * len(header)
    output    = "\n".join([header, separator] + rows)

    print(output)
    Path("output.txt").write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()