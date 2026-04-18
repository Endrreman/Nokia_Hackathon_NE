import json
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────────

FIELD_MAP = {"autoconfiguration_ipv4_address": "ipv4_address",}

LIST_FIELDS = {"default_gateway", "dns_servers"}

KNOWN_SUFFIXES = frozenset({'preferred', 'deferred', 'duplicate', 'tentative'})


# ── Output formatting ────────────────────────────────────────────────────

def _dumps(obj, indent=2, _level=0) -> str:
    pad   = ' ' * (indent * _level)
    inner = ' ' * (indent * (_level + 1))

    if isinstance(obj, dict):
        if not obj:
            return '{}'
        lines = [f'{inner}{json.dumps(k)}: {_dumps(v, indent, _level + 1)}'
                 for k, v in obj.items()]
        return '{\n' + ',\n'.join(lines) + '\n' + pad + '}'

    if isinstance(obj, list):
        if not obj:
            return '[]'
        # Keep lists on a single line for readability
        if all(isinstance(item, str) for item in obj):
            return '[' + ', '.join(json.dumps(item, ensure_ascii=False) for item in obj) + ']'

        lines = [f'{inner}{_dumps(item, indent, _level + 1)}' for item in obj]
        return '[\n' + ',\n'.join(lines) + '\n' + pad + ']'

    return json.dumps(obj, ensure_ascii=False)


# ── Helpers ─────────────────────────────────────────────────────────────────────

def _normalise_key(raw: str) -> str:
    return '_'.join(raw.replace('.', ' ').replace('-', ' ').lower().split())

def _clean_value(v: str) -> str:
    v = v.rstrip()
    if v and v[-1] == ')':
        before, sep, token = v.rpartition('(')
        if sep and token[:-1].lower() in KNOWN_SUFFIXES:
            return before.rstrip()
    return v

def _new_adapter(name: str) -> dict:
    return {
        "adapter_name":    name,
        "description":     "",
        "physical_address": "",
        "dhcp_enabled":    "",
        "ipv4_address":    "",
        "subnet_mask":     "",
        "default_gateway": [],
        "dns_servers":     [],
    }


# ── Parsing ──────────────────────────────────────────────────────────────────────

def parse_file(path: Path) -> dict:
    raw = path.read_bytes()
    encoding = 'utf-16' if raw[0] >= 0xfe else 'utf-8'
    text = raw.decode(encoding, errors='replace')

    adapters = []
    current = None
    last_field = None

    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue

        if line[0].isalpha() and line[-1] == ':' and len(line) > 1:
            current = _new_adapter(line[:-1])
            adapters.append(current)
            last_field = None
            continue

        if current is None:
            continue

        if ' : ' in line:
            left, _, right = line.partition(' : ')
            key_part = left.lstrip()
            if key_part and key_part[0].isalpha():
                field = FIELD_MAP.get(_normalise_key(key_part), _normalise_key(key_part))
                val = _clean_value(right)
                if field in LIST_FIELDS:
                    if val:
                        current[field] = [val]
                elif val:
                    current[field] = val
                last_field = field
                continue

        if line.startswith('      ') and last_field:
            val = _clean_value(line.strip())
            if val:
                existing = current.get(last_field)
                if isinstance(existing, list):
                    existing.append(val)
                elif existing:
                    current[last_field] = [existing, val]
                else:
                    current[last_field] = [val]

    return {"file_name": path.name, "adapters": adapters}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    result = [parse_file(p) for p in sorted(Path(".").glob("*.txt"))]
    print(_dumps(result))


if __name__ == "__main__":
    main()