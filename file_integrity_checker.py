import hashlib
import os
import json

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def scan_directory(directory):
    """Scan all files in directory and return dict of file paths and hashes."""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = calculate_hash(path)
            if file_hash:
                hashes[path] = file_hash
    return hashes

def load_hashes(filename):
    """Load previously saved hashes."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes, filename):
    """Save current hashes to file."""
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=4)

def compare_hashes(old, new):
    """Compare old and new hashes, and print changes."""
    print("\n--- File changes detected ---")
    for path in new:
        if path not in old:
            print(f"[NEW] {path}")
        elif new[path] != old[path]:
            print(f"[MODIFIED] {path}")
    for path in old:
        if path not in new:
            print(f"[DELETED] {path}")

if __name__ == "__main__":
    folder = input("Enter directory to monitor: ")
    db = "file_hashes.json"
    old_hashes = load_hashes(db)
    new_hashes = scan_directory(folder)
    compare_hashes(old_hashes, new_hashes)
    save_hashes(new_hashes, db)
    print("Scan complete.")
