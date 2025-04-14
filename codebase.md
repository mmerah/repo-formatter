# Tree View:
```
.
├─.pytest_cache
└─pyproject.toml
```

# Content:

## .devcontainer/devcontainer.json
```json
{
    "name": "Repo Formatter Dev",
    "image": "python:3.11-slim",
	"features": {
		"ghcr.io/devcontainers/features/git:1": {}
	},
	"postCreateCommand": "pip install --editable .[dev]", // Install the package itself in editable mode + dev deps
	"customizations": {
		"vscode": {
			"extensions": [
				"ms-python.python",
				"ms-python.vscode-pylance",
				"charliermarsh.ruff",
				"esbenp.prettier-vscode"
			],
			"settings": {
				"python.defaultInterpreterPath": "/usr/local/bin/python",
				"python.testing.unittestEnabled": false,
				"python.testing.pytestEnabled": true
			}
		}
	}
}
```

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "repo-formatter"
version = "0.1.0"
authors = [
  { name="Your Name", email="your.email@example.com" },
]
description = "A tool to format repository content into a single Markdown file."
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing",
]
dependencies = [
    "PyYAML>=6.0",
    # Add tiktoken later if needed for more accurate token counting
    # "tiktoken>=0.4.0"
]

[project.urls]
"Homepage" = "https://github.com/mmerah/repo-formatte"
"Bug Tracker" = "https://github.com/mmerah/repo-formatte/issues"

# This creates the command-line script entry point
[project.scripts]
repo-formatter = "repo_formatter.main:cli"

[project.optional-dependencies]
dev = [
    "pytest",
    "ruff",
]
```

## sample_project/CMakeLists.txt
```txt
cmake_minimum_required(VERSION 3.10)
project(Project VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(include)

# Add executable
add_executable(sample_app src/main.cpp src/utils/project/calculator.cpp)

# Print message
message(STATUS "Configuring Project for MyOrg")
```

## sample_project/data/input.txt
```txt
This is some sample data.

```

## sample_project/include/utils/project/calculator.h
```h
#ifndef CALCULATOR_H
#define CALCULATOR_H

namespace MyOrg { // Example potential anonymization target

/**
 * @brief A simple calculator class.
 * Provided by MyOrg Tech Solutions.
 */
class Calculator {
public:
    /**
     * @brief Adds two integers.
     * @param a The first integer.
     * @param b The second integer.
     * @return The sum of a and b.
     */
    int add(int a, int b);

    /**
     * @brief Subtracts two integers.
     * @param a The first integer.
     * @param b The second integer.
     * @return The result of a - b.
     */
    int subtract(int a, int b);
};

} // namespace MyOrg

#endif // CALCULATOR_H
```

## sample_project/scripts/build.sh
```sh
#!/bin/bash
echo "Building the project..."
# Add actual build commands here if needed (e.g., using cmake)
mkdir -p build
cd build
# cmake ..
# make
echo "Build script finished."
```

## sample_project/src/main.cpp
```cpp
#include <iostream>
#include "utils/project/calculator.h" // Relative include path

int main() {
    MyOrg::Calculator calc; // Using the class
    int x = 10;
    int y = 5;

    std::cout << "Welcome to the Sample Calculator!" << std::endl;
    std::cout << x << " + " << y << " = " << calc.add(x, y) << std::endl;
    std::cout << x << " - " << y << " = " << calc.subtract(x, y) << std::endl;

    // Secret message from MyOrg: This should be anonymized if configured.
    std::cout << "Powered by MyOrg." << std::endl;

    return 0;
}
```

## sample_project/src/utils/project/calculator.cpp
```cpp
#include "utils/project/calculator.h"

namespace MyOrg {

int Calculator::add(int a, int b) {
    // Simple addition implementation
    // TODO(ABc): Add overflow check for MyOrg, Project
    return a + b;
}

int Calculator::subtract(int a, int b) {
    // Simple subtraction
    return a - b;
}

} // namespace MyOrg
```

## src/repo_formatter/__init__.py
```py

```

## src/repo_formatter/anonymizer.py
```py
import re
from typing import Dict, Optional

class Anonymizer:
    def __init__(self, rules: Optional[Dict[str, str]] = None):
        self.rules = rules or {}
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Optional[re.Pattern]:
        if not self.rules:
            return None
        # Create a single regex pattern with case-insensitivity
        # Sort by length descending to match longer strings first (e.g., "OrgName" before "Org")
        sorted_keys = sorted(self.rules.keys(), key=len, reverse=True)
        pattern = '|'.join(re.escape(key) for key in sorted_keys)
        return re.compile(pattern, re.IGNORECASE)

    def _replacement_function(self, match: re.Match) -> str:
        """
        Performs replacement while preserving original case pattern.
        """
        matched_text = match.group(0)
        # Find which rule key matched (case-insensitively)
        replacement = ""
        for key, value in self.rules.items():
            if matched_text.lower() == key.lower():
                replacement = value
                break

        # Try to mimic the original case
        if matched_text.islower():
            return replacement.lower()
        elif matched_text.isupper():
            return replacement.upper()
        elif matched_text.istitle():
            # Handle multi-word replacements correctly for title case
            return ' '.join(word.capitalize() for word in replacement.split())
        else:
            # Default to the replacement value as is for mixed case or complex cases
            # More sophisticated case mapping could be added if needed
            return replacement

    def anonymize(self, text: str) -> str:
        """
        Anonymizes the given text based on the loaded rules.
        """
        if not self._compiled_patterns or not text:
            return text
        return self._compiled_patterns.sub(self._replacement_function, text)

    def anonymize_path(self, path_str: str) -> str:
        """
        Anonymizes components of a path string.
        """
        if not self.rules or not path_str:
            return path_str

        parts = path_str.split(re.escape(os.path.sep))
        anonymized_parts = [self.anonymize(part) for part in parts]
        return os.path.sep.join(anonymized_parts)

import os # Need this for anonymize_path
```

## src/repo_formatter/config.py
```py
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

DEFAULT_CONFIG_NAME = ".repo_formatter.yaml"

DEFAULT_CONFIG = {
    "exclude_paths": [
        ".git",
        ".vscode",
        ".devcontainer",
        "__pycache__",
        "node_modules",
        "build",
        "dist",
        ".venv",
        "venv",
        "env",
        ".env",
    ],
    "include_extensions": [], # Empty list means include all
    "anonymize": {}, # e.g., {"YourName": "Contributor A"}
}

def load_config(config_path: Optional[str] = None, start_dir: str = '.') -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    Searches for the default config file name if no path is provided.
    Merges found config with defaults.
    """
    loaded_config = {}
    found_path = None

    if config_path:
        path = Path(config_path)
        if path.is_file():
            found_path = path
    else:
        # Search upwards from start_dir for the default config file
        current_dir = Path(start_dir).resolve()
        while True:
            potential_path = current_dir / DEFAULT_CONFIG_NAME
            if potential_path.is_file():
                found_path = potential_path
                break
            if current_dir.parent == current_dir: # Reached root
                break
            current_dir = current_dir.parent

    if found_path:
        print(f"Loading configuration from: {found_path}")
        try:
            with open(found_path, 'r') as f:
                loaded_config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not read or parse config file {found_path}: {e}")
            loaded_config = {}
    else:
        if config_path: # User specified a path but it wasn't found
             print(f"Warning: Specified config file not found: {config_path}")
        else: # No config specified and default not found
             print(f"No configuration file '{DEFAULT_CONFIG_NAME}' found. Using defaults.")


    # Merge loaded config with defaults (loaded values override defaults)
    # Deep merge isn't strictly necessary here as the structure is simple
    final_config = DEFAULT_CONFIG.copy()

    # Ensure lists and dicts from loaded_config are valid
    exclude_paths = loaded_config.get('exclude_paths')
    if isinstance(exclude_paths, list):
        # Combine default and loaded exclusions, remove duplicates
        final_config['exclude_paths'] = list(set(final_config['exclude_paths'] + exclude_paths))
    elif exclude_paths is not None:
         print(f"Warning: 'exclude_paths' in config is not a list. Ignoring.")

    include_extensions = loaded_config.get('include_extensions')
    if isinstance(include_extensions, list):
        # Overwrite default (empty list means include all)
        final_config['include_extensions'] = [ext.lower() for ext in include_extensions if isinstance(ext, str)]
    elif include_extensions is not None:
         print(f"Warning: 'include_extensions' in config is not a list. Ignoring.")

    anonymize = loaded_config.get('anonymize')
    if isinstance(anonymize, dict):
         final_config['anonymize'] = anonymize
    elif anonymize is not None:
         print(f"Warning: 'anonymize' in config is not a dict. Ignoring.")


    # Ensure all keys exist
    for key in DEFAULT_CONFIG:
        if key not in final_config:
            final_config[key] = DEFAULT_CONFIG[key]

    return final_config
```

## src/repo_formatter/core.py
```py
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .anonymizer import Anonymizer
from .tree import generate_tree_string

# Max file size to read (e.g., 5MB) to avoid memory issues with huge files
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

def is_likely_binary(file_path: Path) -> bool:
    """Check if a file is likely binary by reading the first few bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024) # Read the first 1KB
            return b'\x00' in chunk # Null byte is a strong indicator of binary files
    except Exception:
        return True # Treat read errors as potentially binary/problematic

def _should_skip(
    path: Path,
    root_dir: Path,
    exclude_paths: List[str],
    include_extensions: List[str],
    class_name: Optional[str] = None,
    check_content: bool = False
) -> bool:
    """Determines if a file or directory should be skipped."""
    # Check against exclude_paths (applies to files and dirs)
    for exclude in exclude_paths:
        try:
            # Check if the path relative to root starts with or exactly matches exclude
            relative_path_str = str(path.relative_to(root_dir))
            # Check name directly (e.g., "node_modules")
            if path.name == exclude:
                 # print(f"Skipping {relative_path_str} (name match: {exclude})")
                 return True
            # Check if path starts with excluded dir (e.g., "src/vendor")
            # Need to handle path separators carefully
            # if relative_path_str.startswith(exclude + os.path.sep):
            #      print(f"Skipping {relative_path_str} (prefix match: {exclude})")
            #      return True
        except ValueError: # path is not relative to root_dir (shouldn't happen with os.walk)
             pass
        # Check if any part of the path matches an excluded name
        if exclude in path.parts:
            # print(f"Skipping {path} (part match: {exclude})")
            return True


    if path.is_file():
        # Check file size
        try:
            if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                print(f"Skipping large file: {path.relative_to(root_dir)}")
                return True
        except OSError:
             print(f"Warning: Could not get size for {path.relative_to(root_dir)}. Skipping.")
             return True # Skip if we can't get size

        # Check extensions if specified
        if include_extensions and path.suffix.lower() not in include_extensions:
            # print(f"Skipping {path.relative_to(root_dir)} (extension mismatch)")
            return True

        # Check if likely binary
        if is_likely_binary(path):
            print(f"Skipping likely binary file: {path.relative_to(root_dir)}")
            return True

        # Check content for class name if in class mode
        if check_content and class_name:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if class_name not in content:
                        # print(f"Skipping {path.relative_to(root_dir)} (class name '{class_name}' not found)")
                        return True
            except Exception as e:
                print(f"Warning: Could not read {path.relative_to(root_dir)} for class check: {e}. Skipping.")
                return True # Skip if reading fails

    return False


def format_repo_to_markdown(
    root_dir: str,
    config: Dict,
    anonymize_flag: bool,
    class_name: Optional[str] = None
) -> Tuple[str, List[Path]]:
    """
    Generates the markdown content for the repository.
    Returns the markdown string and a list of included file paths.
    """
    root_path = Path(root_dir).resolve()
    exclude_paths = config.get('exclude_paths', [])
    include_extensions = config.get('include_extensions', [])
    anonymize_rules = config.get('anonymize', {}) if anonymize_flag else {}

    anonymizer = Anonymizer(anonymize_rules)

    markdown_content = []
    included_files = []

    # 1. Generate Tree Structure
    print("Generating directory tree...")
    tree_string = generate_tree_string(root_path, exclude_paths, include_extensions, anonymizer if anonymize_flag else None)
    markdown_content.append("# Repository Structure")
    markdown_content.append("```")
    markdown_content.append(tree_string)
    markdown_content.append("```")
    markdown_content.append("\n---\n") # Separator

    # 2. Walk through the directory and collect file contents
    print("Collecting and formatting file contents...")
    markdown_content.append("# File Contents")

    # Use os.walk for better control over skipping directories
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        current_path = Path(dirpath)

        # Filter dirnames in-place to prevent descending into excluded directories
        # Important: Modify dirnames[:] to change the list os.walk uses
        original_dirnames = list(dirnames) # Copy for iteration
        dirnames[:] = [d for d in original_dirnames if not _should_skip(current_path / d, root_path, exclude_paths, [])]


        for filename in filenames:
            file_path = current_path / filename

            # Determine if we need to check content based on mode
            check_content_for_class = (class_name is not None)

            if _should_skip(file_path, root_path, exclude_paths, include_extensions, class_name, check_content_for_class):
                continue

            relative_path = file_path.relative_to(root_path)
            anonymized_rel_path_str = anonymizer.anonymize_path(str(relative_path)) if anonymize_flag else str(relative_path)

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if anonymize_flag:
                    content = anonymizer.anonymize(content)

                # Determine language for syntax highlighting (optional but nice)
                lang = file_path.suffix.lstrip('.').lower()
                if lang == 'md': lang = 'markdown'
                if lang == 'py': lang = 'python'
                if lang == 'js': lang = 'javascript'
                if lang == 'ts': lang = 'typescript'
                if lang == 'h': lang = 'cpp' # Treat .h as C++
                if lang == 'hpp': lang = 'cpp'
                if lang == 'c': lang = 'c'
                if lang == 'cpp': lang = 'cpp'
                if lang == 'java': lang = 'java'
                if lang == 'sh': lang = 'bash'
                if lang == 'yml': lang = 'yaml'
                # Add more mappings as needed

                markdown_content.append(f"\n## `{anonymized_rel_path_str}`\n")
                markdown_content.append(f"```{lang}")
                markdown_content.append(content.strip()) # Strip leading/trailing whitespace from content
                markdown_content.append("```")
                included_files.append(relative_path) # Store original relative path

            except Exception as e:
                print(f"Warning: Could not process file {relative_path}: {e}")

    if not included_files:
         markdown_content.append("\n*No files were included based on the current filters.*")

    return "\n".join(markdown_content), included_files
```

## src/repo_formatter/git_utils.py
```py
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple, List

def _run_git_command(args: List[str], cwd: str) -> Tuple[bool, str]:
    """Runs a git command and returns (success, output_or_error)."""
    try:
        process = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False, # Don't raise exception on non-zero exit
            encoding='utf-8',
            errors='ignore' # Ignore decoding errors for potentially binary diffs
        )
        if process.returncode == 0:
            return True, process.stdout
        else:
            error_message = f"Git command failed: {' '.join(['git'] + args)}\n"
            error_message += f"Stderr: {process.stderr}\n"
            error_message += f"Stdout: {process.stdout}"
            return False, error_message
    except FileNotFoundError:
        return False, "Error: 'git' command not found. Is Git installed and in your PATH?"
    except Exception as e:
        return False, f"Error running git command: {e}"

def get_current_changes_diff(repo_path: str) -> Tuple[bool, str]:
    """Gets the diff for uncommitted changes."""
    print(f"Getting diff for current changes in: {repo_path}")
    return _run_git_command(["diff", "HEAD"], cwd=repo_path)

def get_commit_diff(repo_path: str, diff_target: str) -> Tuple[bool, str]:
    """Gets the diff between two commits/branches or a commit and HEAD."""
    target1 = diff_target
    target2 = "HEAD" # Default comparison target

    # Check if diff_target contains '...' for range diff
    if '...' in diff_target:
        parts = diff_target.split('...', 1)
        target1 = parts[0]
        target2 = parts[1]
        print(f"Getting diff between {target1} and {target2} in: {repo_path}")
        return _run_git_command(["diff", f"{target1}...{target2}"], cwd=repo_path)
    elif '..' in diff_target:
         parts = diff_target.split('..', 1)
         target1 = parts[0]
         target2 = parts[1]
         print(f"Getting diff between {target1} and {target2} in: {repo_path}")
         return _run_git_command(["diff", f"{target1}..{target2}"], cwd=repo_path)
    else:
        # Assume diff against target and working tree or HEAD if single ref
        # Let's default to diffing against HEAD for simplicity if only one ref given
        print(f"Getting diff between {diff_target} and HEAD in: {repo_path}")
        return _run_git_command(["diff", diff_target], cwd=repo_path) # Diff between target and working tree
        # Or: return _run_git_command(["diff", f"{diff_target}..HEAD"], cwd=repo_path) # Diff between target and HEAD commit

def check_repo(repo_path: str) -> bool:
    """Checks if the path is a git repository."""
    git_dir = Path(repo_path) / ".git"
    return git_dir.is_dir()
```

## src/repo_formatter/main.py
```py
import argparse
import os
import sys
from pathlib import Path

from . import config as cfg
from . import core
from . import git_utils
from . import token_estimator
from .anonymizer import Anonymizer

OUTPUT_FILENAME = "repository.md"

def cli():
    parser = argparse.ArgumentParser(
        description="Format repository content into a single Markdown file."
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The target directory to process (default: current directory).",
    )

    # Mode arguments
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-m", "--mode",
        choices=["normal", "class", "patch"],
        default="normal",
        help="Processing mode: 'normal' (default), 'class', or 'patch'.",
    )
    parser.add_argument(
        "--class-name",
        metavar="NAME",
        help="The class name to search for in 'class' mode.",
    )
    parser.add_argument(
        "--diff-target",
        metavar="TARGET",
        help="Specify the target for 'patch' mode. "
             "Use 'current' for uncommitted changes, or a commit/branch name (e.g., 'main', 'HEAD~1', 'feature-branch..main').",
    )

    # Configuration and Options
    parser.add_argument(
        "-c", "--config",
        metavar="PATH",
        help=f"Path to the configuration YAML file (default: searches for {cfg.DEFAULT_CONFIG_NAME}).",
    )
    parser.add_argument(
        "-a", "--anonymize",
        action="store_true",
        help="Enable anonymization based on config file rules.",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILENAME",
        default=OUTPUT_FILENAME,
        help=f"Name of the output Markdown file (default: {OUTPUT_FILENAME}).",
    )

    args = parser.parse_args()

    # --- Input Validation ---
    target_dir = Path(args.directory).resolve()
    if not target_dir.is_dir():
        print(f"Error: Directory not found: {args.directory}")
        sys.exit(1)

    if args.mode == "class" and not args.class_name:
        print("Error: --class-name is required for 'class' mode.")
        sys.exit(1)

    if args.mode == "patch" and not args.diff_target:
        print("Error: --diff-target is required for 'patch' mode (e.g., 'current', 'main', 'HEAD~1').")
        sys.exit(1)

    output_file_path = target_dir / args.output

    # --- Load Configuration ---
    try:
        config = cfg.load_config(args.config, str(target_dir))
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # --- Execute Mode ---
    markdown_content = ""
    final_output_path = output_file_path # Default output path

    if args.mode == "patch":
        print(f"Running in Patch mode (target: {args.diff_target})...")
        if not git_utils.check_repo(str(target_dir)):
             print(f"Error: Target directory '{target_dir}' is not a Git repository.")
             sys.exit(1)

        success = False
        diff_output = ""
        if args.diff_target.lower() == "current":
            success, diff_output = git_utils.get_current_changes_diff(str(target_dir))
        else:
            success, diff_output = git_utils.get_commit_diff(str(target_dir), args.diff_target)

        if not success:
            print(f"Error getting diff:\n{diff_output}") # diff_output contains error message on failure
            sys.exit(1)

        if not diff_output.strip():
             print("No differences found for the specified target.")
             # Decide whether to create an empty file or exit
             # Let's create a file indicating no diff
             markdown_content = f"# Git Diff: {args.diff_target}\n\n```diff\nNo differences found.\n```"
        else:
            # Anonymize the diff output if requested
            if args.anonymize:
                anonymizer = Anonymizer(config.get('anonymize', {}))
                diff_output = anonymizer.anonymize(diff_output)

            markdown_content = f"# Git Diff: {args.diff_target}\n\n"
            markdown_content += "```diff\n"
            markdown_content += diff_output.strip() + "\n" # Ensure trailing newline
            markdown_content += "```"
        # In patch mode, output file might be better placed outside the repo?
        # For now, place it inside like other modes.
        final_output_path = target_dir / f"diff_{args.diff_target.replace('/', '_').replace('.', '_')}.md"


    elif args.mode == "class":
        print(f"Running in Class mode (searching for '{args.class_name}')...")
        markdown_content, _ = core.format_repo_to_markdown(
            str(target_dir), config, args.anonymize, class_name=args.class_name
        )
        final_output_path = target_dir / f"class_{args.class_name}.md"

    else: # Normal mode
        print("Running in Normal mode...")
        markdown_content, _ = core.format_repo_to_markdown(
            str(target_dir), config, args.anonymize
        )
        final_output_path = target_dir / args.output # Use default or specified output name


    # --- Write Output ---
    try:
        with open(final_output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"\nSuccessfully generated Markdown file: {final_output_path}")
    except Exception as e:
        print(f"\nError writing output file {final_output_path}: {e}")
        sys.exit(1)

    # --- Estimate Tokens ---
    tokens = token_estimator.estimate_tokens(markdown_content)
    # tokens = token_estimator.estimate_tokens_tiktoken(markdown_content) # If using tiktoken
    print(f"Estimated token count (basic): ~{tokens}")

if __name__ == "__main__":
    cli()
```

## src/repo_formatter/token_estimator.py
```py
# Basic token estimation (can be replaced with tiktoken later)

def estimate_tokens(text: str) -> int:
    """
    Provides a very rough estimate of token count.
    A common rule of thumb is ~4 characters per token.
    """
    # Simple character-based estimate
    estimated_tokens = len(text) / 4

    # Alternative: Word count based estimate (often closer)
    # word_count = len(text.split())
    # estimated_tokens = word_count * 1.3 # Adjust multiplier as needed

    return int(estimated_tokens)

# Example using tiktoken (if installed)
# import tiktoken
# def estimate_tokens_tiktoken(text: str, encoding_name: str = "cl100k_base") -> int:
#     """Estimates tokens using tiktoken library."""
#     try:
#         encoding = tiktoken.get_encoding(encoding_name)
#         num_tokens = len(encoding.encode(text))
#         return num_tokens
#     except Exception as e:
#         print(f"Warning: tiktoken estimation failed ({e}). Falling back to basic estimation.")
#         return estimate_tokens(text)
```

## src/repo_formatter/tree.py
```py
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
```

