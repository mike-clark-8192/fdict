import hashlib
import sys
from multiprocessing import Pool, cpu_count

# Pipe a list of files to this script to get a list of unique files
# as determined by their SHA256 hash. When there is more than one file
# with the same hash, the shortest path is printed.

def compute_file_hash(filepath):
    """Compute SHA256 hash of the file content."""
    try:
        hash_sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4_000_000), b""):
                hash_sha256.update(chunk)
        return filepath, hash_sha256.hexdigest()
    except Exception as e:
        return filepath, e

def main():
    filepaths = [line.strip() for line in sys.stdin]
    n_workers = max(1, cpu_count() - 2)
    pool = Pool(processes=n_workers)

    # Parallel computation of file hashes
    results = pool.map(compute_file_hash, filepaths, chunksize=1000)

    filepath2hash = {}
    hash2filepaths = {}

    for filepath, hash_or_exc in results:
        if isinstance(hash_or_exc, Exception):
            print(f"Error processing file {filepath}\n{hash_or_exc}", file=sys.stderr)
            continue
        filehash = hash_or_exc
        filepath2hash[filepath] = filehash
        if filehash in hash2filepaths:
            hash2filepaths[filehash].append(filepath)
        else:
            hash2filepaths[filehash] = [filepath]

    # Selecting shortest path for duplicates, printing unique ones directly
    for paths in hash2filepaths.values():
        if len(paths) > 1:
            print(min(paths, key=len))
        else:
            print(paths[0])

if __name__ == "__main__":
    main()