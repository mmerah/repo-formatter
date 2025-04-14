from pathlib import Path
from typing import List, Set

def generate_tree_string(start_path: Path, exclude_paths: List[str], include_extensions: List[str], anonymizer=None) -> str:
    """
    Generates a string representation of the directory tree, respecting exclusions.
    """
    tree_lines = []
    exclude_set = set(exclude_paths) # For faster lookups

    def is_excluded(path: Path, exclude_set: Set[str]) -> bool:
        """Check if a path or any of its parts match exclusion patterns."""
        # Check the name itself
        if path.name in exclude_set:
            return True
        # Check if any parent directory name is excluded (less common, but possible)
        # for part in path.parts:
        #     if part in exclude_set:
        #         return True
        return False

    def add_items(directory: Path, prefix: str = ""):
        # Sort items for consistent order, directories first
        items = sorted(list(directory.iterdir()), key=lambda p: (p.is_file(), p.name.lower()))
        pointers = ['├── '] * (len(items) - 1) + ['└── ']

        for pointer, path in zip(pointers, items):
            if is_excluded(path, exclude_set):
                continue

            anonymized_name = anonymizer.anonymize(path.name) if anonymizer else path.name

            if path.is_dir():
                tree_lines.append(f"{prefix}{pointer}{anonymized_name}/")
                extension = prefix + ('│   ' if pointer == '├── ' else '    ')
                add_items(path, prefix=extension)
            elif path.is_file():
                # Check extension if include_extensions is specified
                if not include_extensions or path.suffix.lower() in include_extensions:
                    tree_lines.append(f"{prefix}{pointer}{anonymized_name}")

    # Start the tree generation
    start_path = Path(start_path).resolve()
    anonymized_root = anonymizer.anonymize(start_path.name) if anonymizer else start_path.name
    tree_lines.append(f"{anonymized_root}/")
    add_items(start_path)
    return "\n".join(tree_lines)