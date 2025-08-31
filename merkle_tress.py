import os
import hashlib

# step 1 - hashing each file
def file_hash(filepath):
    
    hasher = hashlib.md5()
    with open(filepath, "rb") as f: # reads it binary
        while chunk := f.read(4096):  # reads it in in small chunks
            hasher.update(chunk)
    return hasher.hexdigest()


# step 2 - Merkle Trees 
class MerkleTree:
    def __init__(self, hashes):
        self.levels = []        # store all levels (leaves up to root)
        self.build_tree(hashes)

    def build_tree(self, hashes):
        current_level = hashes
        self.levels.append(current_level)

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left  # duplicate last if odd number
                # parent = hash(left + right)
                parent = hashlib.md5((left + right).encode()).hexdigest()
                next_level.append(parent)
            current_level = next_level
            self.levels.append(current_level)

    def get_root(self):
        return self.levels[-1][0] if self.levels else None


# step 3: Scan folder and build tree
def scan_and_build_merkle(directory):
    file_hashes = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                h = file_hash(filepath)
                file_hashes.append(h)
                print(f"{filepath} -> {h}")
            except Exception as e:
                print(f"Could not read {filepath}: {e}")

    if not file_hashes:
        print("No files found.")
        return None

    # building the Merkle Tree
    tree = MerkleTree(file_hashes)
    root_hash = tree.get_root()

    print("\nMerkle Root:", root_hash)

    # saving the root for later verification
    with open("root_hash.txt", "w") as f:
        f.write(root_hash)

    return root_hash


# actually running it 
if __name__ == "__main__":
    folder = input("Enter folder to scan: ")
    scan_and_build_merkle(folder)
