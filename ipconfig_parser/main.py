import json
from pathlib import Path


FIELD_MAP = {
    "description": "description",
    "physical address": "physical_address",
    "dhcp enabled": "dhcp_enabled",
    "ipv4 address": "ipv4_address",
    "autoconfiguration ipv4 address": "ipv4_address",
    "subnet mask": "subnet_mask",
    "default gateway": "default_gateway",
    "dns servers": "dns_servers",
}

LIST_FIELDS = {"default_gateway", "dns_servers"}

_KNOWN_SUFFIXES = frozenset({'preferred', 'deferred', 'duplicate', 'tentative'})

def _normalise_key(raw: str) -> str:
    return ' '.join(raw.replace('.', ' ').lower().split())

def _clean_value(v: str) -> str:
    v = v.rstrip()
    if v and v[-1] == ')':
        before, sep, token = v.rpartition('(')
        if sep and token[:-1].lower() in _KNOWN_SUFFIXES:
            return before.rstrip()
    return v

def _new_adapter(name: str) -> dict:
    return {
        "adapter_name": name,
        "description": "",
        "physical_address": "",
        "dhcp_enabled": "",
        "ipv4_address": "",
        "subnet_mask": "",
        "default_gateway": [],
        "dns_servers": [],
    }


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
                field = FIELD_MAP.get(_normalise_key(key_part))
                val = _clean_value(right)
                if field:
                    if field in LIST_FIELDS:
                        current[field] = [val] if val else []
                    else:
                        current[field] = val
                    last_field = field
                else:
                    last_field = None
                continue

        if line.startswith('      ') and last_field in LIST_FIELDS:
            val = _clean_value(line.strip())
            if val:
                current[last_field].append(val)

    return {"file_name": path.name, "adapters": adapters}


def main():
    result = [parse_file(p) for p in sorted(Path(".").glob("*.txt"))]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()