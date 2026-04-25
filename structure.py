import os

def print_tree(root_dir, prefix=""):
    entries = sorted(os.listdir(root_dir))
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        connector = "└── " if index == entries_count - 1 else "├── "

        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == entries_count - 1 else "│   "
            print_tree(path, prefix + extension)


def generate_structure(root_dir):
    print(os.path.basename(root_dir) + "/")
    print_tree(root_dir)


if __name__ == "__main__":
    folder_path = "Paktax AI/Paktax-AI"
    generate_structure(folder_path)