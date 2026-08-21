"""Compile les catalogues .po vers .mo (format GNU gettext) sans gettext.

Usage : python compile_po.py
Lit locale/<lang>/LC_MESSAGES/django.po et écrit django.mo.
Le .mo est trié par ordre d'octets UTF-8 des msgids (recherche binaire Django).
"""

import struct
import sys
from pathlib import Path

LOCALE = Path(sys.argv[1] if len(sys.argv) > 1 else "locale").resolve()


def parse_po(text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    current_id: list[str] = []
    current_str: list[str] | None = None
    in_header = True

    def flush():
        nonlocal current_id, current_str
        if current_str is not None:
            mid = "".join(current_id)
            mstr = "".join(current_str)
            entries.append((mid, mstr))
        current_id, current_str = [], None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith('msgid "') or line == 'msgid ""':
            flush()
            current_id = [line[len('msgid "') : -1]]
        elif line.startswith('msgstr "') or line == 'msgstr ""':
            current_str = [line[len('msgstr "') : -1]]
        elif line.startswith('"') and current_str is not None:
            current_str.append(line[1:-1])
        elif line.startswith('"') and current_id:
            current_id.append(line[1:-1])
        elif line.startswith("msgid_plural"):
            flush()
            current_id, current_str = [], None
        elif line.startswith("msgstr["):
            continue
    flush()
    return entries


def unescape(s: str) -> str:
    return (
        s.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


def write_mo(path: Path, entries: list[tuple[str, str]]) -> None:
    pairs = [(unescape(k).encode("utf-8"), unescape(v).encode("utf-8")) for k, v in entries]
    pairs.sort(key=lambda kv: kv[0])
    n = len(pairs)
    offsets = []
    payload = bytearray()
    for _, val in pairs:
        offsets.append((len(val), len(payload)))
        payload += val
        payload += b"\0"
        while len(payload) % 4:
            payload += b"\0"
    key_offsets = []
    for key, _ in pairs:
        key_offsets.append((len(key), len(payload)))
        payload += key
        payload += b"\0"
        while len(payload) % 4:
            payload += b"\0"
    header_len = 20
    o_table = header_len
    t_table = header_len + n * 8
    data_start = t_table + n * 8
    header = struct.pack("<IiiII", 0x950412DE, 0, n, o_table, t_table)
    out = bytearray(header)
    for length, off in key_offsets:
        out += struct.pack("<II", length, data_start + off)
    for length, off in offsets:
        out += struct.pack("<II", length, data_start + off)
    out += payload
    path.write_bytes(out)


def main():
    for lang_dir in sorted(LOCALE.iterdir()):
        po = lang_dir / "LC_MESSAGES" / "django.po"
        if not po.exists():
            continue
        entries = parse_po(po.read_text(encoding="utf-8"))
        mo = po.with_suffix(".mo")
        write_mo(mo, entries)
        print(f"{po.relative_to(LOCALE)} -> {mo.name} ({len(entries)} chaînes)")


if __name__ == "__main__":
    main()