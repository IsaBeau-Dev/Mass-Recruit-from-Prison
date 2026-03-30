#!/usr/bin/env python3
# BASED ON A SCRIPT BY Dlonem | SPN
"""
Create non-English CK3 localization folders/files from the English source.

- Duplicates every .yml under localization/english into each target language folder.
- Renames filenames suffix (_english.yml -> _<lang>.yml).
- Rewrites the header key on the first non-empty line (e.g., l_english: -> l_spanish:).
- Writes files with UTF-8 BOM and Windows line endings (CRLF) which CK3 expects.
- Skips copying if destination file already exists unless --overwrite is provided.

Usage:
  py create_localizations.py
  py create_localizations.py --src localization/english --langs spanish german french --overwrite
"""

from __future__ import annotations
from pathlib import Path
import argparse
import re

DEFAULT_SRC = Path("localization/english")
DEFAULT_LANGS = ["spanish","french","german","korean","polish","russian","simp_chinese"]

HEADER_MAP = {
    "english": "l_english",
    "spanish": "l_spanish",
    "french": "l_french",
    "german": "l_german",
    "korean": "l_korean",
    "polish": "l_polish",
    "russian": "l_russian",
    "simp_chinese": "l_simp_chinese",
}

def find_yml_files(src_dir: Path):
    return [p for p in src_dir.rglob("*.yml") if p.is_file()]

def target_from_source(src_file: Path, src_dir: Path, lang: str) -> Path:
    rel = src_file.relative_to(src_dir)  # e.g., events/abc_english.yml
    name = rel.name
    if name.lower().endswith("_english.yml"):
        new_name = name[:-len("_english.yml")] + f"_{lang}.yml"
    else:
        new_name = f"{rel.stem}_{lang}.yml"
    return Path("localization") / lang / rel.parent / new_name

def rewrite_header_to_lang(text: str, lang: str) -> str:
    lines = text.splitlines()
    target_header = HEADER_MAP[lang] + ":"
    original_lang = "unknown"
    for i, line in enumerate(lines):
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if raw.startswith("l_") and raw.endswith(":"):
            original_lang = raw.split("_")[1].rstrip(":")
            lines[i] = line.replace(raw, target_header, 1)
            comment = f"# THIS FILE IS A MIRROR OF THE {original_lang.upper()} LOCALIZATION WITHOUT PROPER TRANSLATION"
            lines.insert(i + 1, comment)
            break
        else:
            comment = f"# THIS FILE IS A MIRROR OF THE {original_lang.upper()} LOCALIZATION WITHOUT PROPER TRANSLATION"
            lines.insert(i, target_header)
            lines.insert(i + 1, comment)
            break
    else:
        comment = f"# THIS FILE IS A MIRROR OF THE {original_lang.upper()} LOCALIZATION WITHOUT PROPER TRANSLATION"
        lines.append(target_header)
        lines.append(comment)
    # Return with CRLF endings; file open uses newline='\r\n' to preserve
    return "\r\n".join(lines) + "\r\n"

def parse_localization_keys(text: str) -> dict[str, str]:
    """Extract localization keys and their values from the text."""
    # Updated regex to capture keys with special characters, numbers, and different formats
    pattern = re.compile(r"^([\w\.\-]+):\d*\s*\"(.*?)\"", re.MULTILINE)
    return {match[1]: match[2] for match in pattern.finditer(text)}

def generate_untranslated_file(untranslated_keys: dict[str, dict[str, str]], lang: str):
    """Generate a file for untranslated keys and their values in the appropriate language folder."""
    # Create the language directory if it doesn't exist
    lang_dir = Path("localization") / lang
    lang_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the untranslated file in the language directory
    untranslated_file = lang_dir / f"untranslated_keys_l_{lang}.yml"
    with untranslated_file.open("w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(f"{HEADER_MAP[lang]}:\n")
        for file, keys in untranslated_keys.items():
            f.write(f"#/ {file}\n")
            for key, value in keys.items():
                f.write(f"  {key}: \"{value}\"\n")

def process_file(src_file: Path, dst_file: Path, lang: str, overwrite: bool = False) -> bool:
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    if dst_file.exists() and not overwrite:
        return False
    text = src_file.read_text(encoding="utf-8-sig")
    out = rewrite_header_to_lang(text, lang)
    with dst_file.open("w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(out)
    return True

def log(message: str, level: str = "info", verbose: bool = False):
    """Log messages with different levels (info, warning, error) and colors."""
    levels = {
        "info": ("[INFO]", "\033[0;32m"),       # Green
        "warning": ("[WARNING]", "\033[0;33m"), # Yellow
        "error": ("[ERROR]", "\033[0;31m"),     # Red
    }
    reset_color = "\033[0m"
    if level not in levels:
        level = "info"
    prefix, color = levels[level]
    if verbose or level in {"warning", "error"}:
        print(f"{color}{prefix} {message}{reset_color}")

def process_file_with_existing_check(src_file: Path, dst_file: Path, lang: str, overwrite: bool = False, verbose: bool = False):
    """Process a file, checking for existing translations."""
    untranslated_pairs = {}
    
    if dst_file.exists():
        # Read existing translations
        existing_text = dst_file.read_text(encoding="utf-8-sig")
        if "# THIS FILE IS A MIRROR OF THE" in existing_text:
            return "mirror"  # Indicate the file is a mirror

        existing_pairs = parse_localization_keys(existing_text)
        existing_keys = set(existing_pairs.keys())
        existing_locs = set(existing_pairs.values())

        # Read source translations
        src_text = src_file.read_text(encoding="utf-8-sig")
        src_pairs = parse_localization_keys(src_text)
        src_keys = set(src_pairs.keys())
        src_locs = set(src_pairs.values())

        # Find untranslated keys
        untranslated = {key: value for key, value in src_pairs.items() if key not in existing_keys}
        if untranslated:
            untranslated_pairs[str(dst_file)] = untranslated

        # Generate untranslated file
        if untranslated_pairs:
            generate_untranslated_file(untranslated_pairs, lang)

        return untranslated_pairs  # Return untranslated keys for summary

    # If the file doesn't exist, process as usual
    return process_file(src_file, dst_file, lang, overwrite)

def main():
    ap = argparse.ArgumentParser(
        description="Mirror your CK3 localization folders/files to other languages but keep already translated stuff intact."
    )
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="Source directory containing Source Language localization files.(English is the default)")
    ap.add_argument("--langs", nargs="*", default=DEFAULT_LANGS, help="Target languages to generate localization files for.")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing localization files if they already exist.")
    ap.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for detailed logging.")
    args = ap.parse_args()

    src_dir = args.src
    if not src_dir.exists():
        log(f"Source folder not found: {src_dir}", "error")
        raise SystemExit(1)
    files = find_yml_files(src_dir)
    if not files:
        log(f"No .yml files found under {src_dir}", "error")
        raise SystemExit(1)

    made = 0
    skipped_mirrors = {lang: [] for lang in args.langs}  # Track skipped mirrors per language
    untranslated_summary = {lang: {} for lang in args.langs}  # Track untranslated keys per language
    for src in files:
        for lang in args.langs:
            if lang not in HEADER_MAP:
                log(f"Skipping unknown language key: {lang}", "warning", args.verbose)
                continue
            dst = target_from_source(src, src_dir, lang)
            result = process_file_with_existing_check(src, dst, lang, overwrite=args.overwrite, verbose=args.verbose)
            if result == "mirror":
                skipped_mirrors[lang].append(dst)
            elif isinstance(result, dict):  # Untranslated keys found
                untranslated_summary[lang].update(result)
            elif result:
                made += 1
                log(f"Wrote {dst}", "info", args.verbose)

    #Skipped mirrors header
    if any(skipped_mirrors.values()):
        print("Skipped mirrors summary:")
    # Summarize skipped mirrors
    for lang, files in skipped_mirrors.items():
        if files:
            log(f"Skipped {len(files)} files as they were a mirror for language: {lang}", "warning", args.verbose)
            if args.verbose:
                for file in files:
                    log(f"  - {file}", "info", args.verbose)

    #Skipped keys header
    if any(untranslated_summary.values()):
        print("Skipped keys summary:")
    # Summarize untranslated keys
    for lang, files in untranslated_summary.items():
        if files:
            total_keys = sum(len(keys) for keys in files.values())
            log(f"Found {total_keys} untranslated keys for language: {lang}", "info", True)
            if args.verbose:
                for file, keys in files.items():
                    log(f"  - {file}: {len(keys)} untranslated keys", "info", args.verbose)

    log(f"Done. Created/updated {made} files.", "info")

if __name__ == "__main__":
    main()
