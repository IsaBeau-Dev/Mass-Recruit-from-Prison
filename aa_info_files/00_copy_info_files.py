import os
import shutil
from pathlib import Path

def copy_info_files(source_dir):
    source_dir = Path(source_dir).resolve()
    target_dir = Path(__file__).parent.resolve()

    if not source_dir.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(".info"):
                src_file = Path(root) / file
                dst_file = target_dir / file

                # Avoid overwriting: auto-rename if needed
                counter = 1
                while dst_file.exists():
                    dst_file = target_dir / f"{dst_file.stem}_{counter}{dst_file.suffix}"
                    counter += 1

                shutil.copy2(src_file, dst_file)
                print(f"Copied: {src_file} -> {dst_file}")

if __name__ == "__main__":
    # Change this to your source directory
    source_path = r"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game"
    copy_info_files(source_path)
