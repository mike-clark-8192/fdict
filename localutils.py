import sys
import cchardet
from pathlib import Path

def read_file_guessing_encoding(file: Path) -> str:
    bytes_ = file.read_bytes()
    enc = cchardet.detect(bytes_)["encoding"]
    if enc:
        try:
            return bytes_.decode(enc)
        except UnicodeDecodeError:
            pass
    return ""


def try_print(file, match):
    try:
        print(f"{file}: {match.substring()}")
    except UnicodeEncodeError as e:
        print(f"{file}: {e}")

def print_err(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)