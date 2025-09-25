#!/usr/bin/env python3
"""
copy_up_one_dir.py

Copies:
- full_gene/full_gene.fasta           -> parent directory
- CDS/CDS_gene.fasta                  -> parent directory
- protein/protein.fasta OR proteins/protein.fasta -> parent directory

Uses shutil.copy2 to preserve timestamps/metadata.
Run from the project root (the directory that contains full_gene/, CDS/, protein(s)/).
"""

import sys
from pathlib import Path
from shutil import copy2

def copy_up(src_rel: str) -> None:
    src = Path(src_rel)
    if not src.exists():
        print(f"[SKIP] Not found: {src}")
        return
    dest = src.parent.parent / src.name  # copy to parent of the directory containing the file
    try:
        copy2(src, dest)
        print(f"[OK]  Copied {src} -> {dest}")
    except Exception as e:
        print(f"[ERR] Failed to copy {src} -> {dest}: {e}")

def main():
    # full_gene
    copy_up("full_gene/full_gene.fasta")

    # CDS
    copy_up("CDS/CDS_gene.fasta")

    # protein/proteins (support both)
    if Path("protein/protein.fasta").exists():
        copy_up("protein/protein.fasta")
    else:
        copy_up("proteins/protein.fasta")

if __name__ == "__main__":
    sys.exit(main())
