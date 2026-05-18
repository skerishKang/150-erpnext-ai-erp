#!/usr/bin/env python3
"""Check file sizes in a codebase.

Usage:
    python scripts/check_file_size.py --root padiem_ai/padiem_ai --max-lines 500 --warn-lines 350
"""

import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Check file sizes in codebase")
    parser.add_argument(
        "--root",
        default="padiem_ai/padiem_ai",
        help="Root directory to scan (default: padiem_ai/padiem_ai)",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=500,
        help="Hard limit for lines (exit 1 if exceeded, default: 500)",
    )
    parser.add_argument(
        "--warn-lines",
        type=int,
        default=350,
        help="Warning threshold (default: 350)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Show top N largest files (default: 10)",
    )
    return parser.parse_args()


# Patterns to exclude
EXCLUDE_DIRS = {
    ".git", "node_modules", "env", ".venv", "sites", "frappe", "erpnext",
    "__pycache__", ".tox", ".pytest_cache", "build", "dist", ".eggs",
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".pyo", ".min.js", ".min.css", ".map", ".bundle.js",
}

EXCLUDE_PATTERNS = [
    ".env", "site_config", "password", "secret", "key", "token",
    "backup", "fixture", "demo",
]


def should_exclude(path: str) -> bool:
    """Check if path should be excluded from size check."""
    parts = path.split(os.sep)
    
    # Check directory exclusion
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    
    # Check extension exclusion
    _, ext = os.path.splitext(path)
    if ext.lower() in EXCLUDE_EXTENSIONS:
        return True
    
    # Check pattern exclusion (env, secret, key, etc.)
    path_lower = path.lower()
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_lower:
            return True
    
    return False


def count_lines(path: str) -> int:
    """Count physical lines in a file."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (IOError, OSError):
        return 0


def scan_directory(root: str):
    """Scan directory and return file sizes."""
    files = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out excluded directories in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            if should_exclude(filepath):
                continue
            
            lines = count_lines(filepath)
            if lines > 0:
                files.append((filepath, lines))
    
    return files


def main():
    args = parse_args()
    
    if not os.path.isdir(args.root):
        print(f"Error: {args.root} is not a directory")
        sys.exit(2)
    
    files = scan_directory(args.root)
    files.sort(key=lambda x: x[1], reverse=True)
    
    # Categorize files
    errors = []
    warnings = []
    
    for filepath, lines in files:
        if lines > args.max_lines:
            errors.append((filepath, lines))
        elif lines > args.warn_lines:
            warnings.append((filepath, lines))
    
    # Print warnings
    if warnings:
        print(f"\n⚠️  Warnings (>{args.warn_lines} lines):")
        for filepath, lines in warnings:
            print(f"  {lines:>4} lines: {filepath}")
    
    # Print errors
    if errors:
        print(f"\n❌ Errors (>{args.max_lines} lines):")
        for filepath, lines in errors:
            print(f"  {lines:>4} lines: {filepath}")
    
    # Print top files
    print(f"\n📊 Top {args.top} largest files:")
    for filepath, lines in files[:args.top]:
        marker = " (!)" if lines > args.max_lines else ""
        print(f"  {lines:>4} lines: {filepath}{marker}")
    
    # Summary
    print(f"\n📈 Summary:")
    print(f"  Total files checked: {len(files)}")
    print(f"  Warning threshold: {args.warn_lines}")
    print(f"  Hard limit: {args.max_lines}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Errors: {len(errors)}")
    
    # Exit codes
    if errors:
        print("\n❌ FAIL: Files exceed hard limit")
        sys.exit(1)
    else:
        print("\n✅ PASS: All files within limits")
        sys.exit(0)


if __name__ == "__main__":
    main()