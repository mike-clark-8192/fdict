import argparse
from pathlib import Path

import tqdm

import localutils as util
import pcre_patterns as preg

parser = argparse.ArgumentParser(description="Find dict literals that could be DRYed up")
parser.add_argument("filelist_file", default="dedupedpyfiles.txt",
                    type=str, help="File with list of files to process")
args = parser.parse_args()

def main():
    files = Path(args.filelist_file).read_text(encoding="utf-8")
    hash2file = {x: xp for x in files.splitlines() if (xp := Path(x)).is_file()}

    dry_match_count = 0
    match_count = 0
    bytes_count = 0

    with tqdm.tqdm(hash2file.items()) as pbar:
        for _hash, file in pbar:
            content = util.read_file_guessing_encoding(file)
            bytes_count += len(content)
            try:
                for match in preg.DRY_RE.scan(content):
                    dry_match_count += 1
                    util.try_print(file, match)
                for match in preg.NONDRY_RE.scan(content):
                    match_count += 1
                    util.try_print(file, match)
            except Exception as e:
                # The regex can't parse dicts literals with
                # embedded comments, so...
                continue

    match_count = match_count - dry_match_count
    megabytes = bytes_count / 1_000_000
    ratio = dry_match_count / match_count
    util.print_err(f"Total files: {len(hash2file)}")
    util.print_err(f"Total bytes: {megabytes:.2f} MB")
    util.print_err(f"Total DRY matches: {dry_match_count}")
    util.print_err(f"Total non-DRY matches: {match_count}")
    util.print_err(f"DRY / non-DRY %: {ratio * 100:.2f}")

if __name__ == "__main__":
    main()
