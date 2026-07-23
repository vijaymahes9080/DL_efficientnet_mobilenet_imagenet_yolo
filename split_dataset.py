"""
=============================================================================
High-Performance Stratified Dataset Splitter
=============================================================================
Description:
    Automatically splits image datasets into Train (70%), Validation (15%), 
    and Testing (15%) subsets with class-wise stratification, corruption 
    verification, and high-speed multi-threaded file operations.

Supported Extensions:
    .jpg, .jpeg, .png, .bmp, .tif, .tiff, .webp

Execution:
    python split_dataset.py
=============================================================================
"""

import os
import shutil
import random
from pathlib import Path
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from sklearn.model_selection import train_test_split

# Optional import for PIL image corruption verification
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# =============================================================================
# CONFIGURATION & PARAMETERS
# =============================================================================
# 1. Primary source dataset directory and output folder
SOURCE_DATASET = "dataset"
OUTPUT_FOLDER = "dataset_split"

# 2. List of model dataset directories to process each model folder separately
MODEL_DATASETS = [
    r"d:\college\DL 4 models\DL -YOLO\dataset",
    r"d:\college\DL 4 models\DL - mobilenet\dataset",
    r"d:\college\DL 4 models\DL - imagenet\dataset",
    r"d:\college\DL 4 models\DL - efficientnet b0\dataset"
]

# 3. Split proportions (Must sum to 1.0)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# 4. Global Random Seed for reproducibility
SEED = 42

# 5. Supported file extensions
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# 6. Maximum parallel threads for fast IO operations
MAX_WORKERS = min(32, (os.cpu_count() or 4) * 4)


# =============================================================================
# IMAGE VERIFICATION & UTILITIES
# =============================================================================
def set_seed(seed: int = 42) -> None:
    """Set global random seed for exact reproducibility."""
    random.seed(seed)


def verify_single_image(file_path: Path) -> Tuple[Path, bool]:
    """
    Validates image file existence, size, and header integrity.
    Returns (file_path, is_valid_boolean).
    """
    if not file_path.is_file() or file_path.stat().st_size == 0:
        return file_path, False

    if file_path.suffix.lower() not in VALID_EXTENSIONS:
        return file_path, False

    if PIL_AVAILABLE:
        try:
            with Image.open(file_path) as img:
                img.verify()
            return file_path, True
        except Exception:
            return file_path, False
    else:
        try:
            with open(file_path, "rb") as f:
                header = f.read(10)
                return file_path, len(header) > 0
        except Exception:
            return file_path, False


def scan_dataset(source_dir: Path) -> Tuple[List[Path], List[str], List[str]]:
    """
    Scans the class directories in parallel to collect all valid images and labels.
    """
    class_dirs = [d for d in source_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    class_names = sorted([d.name for d in class_dirs])

    candidate_files: List[Tuple[Path, str]] = []
    for class_dir in class_dirs:
        c_name = class_dir.name
        for f in class_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS:
                candidate_files.append((f, c_name))

    if not candidate_files:
        return [], [], class_names

    # Fast parallel image integrity verification
    valid_paths: List[Path] = []
    valid_labels: List[str] = []
    skipped_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_label = {
            executor.submit(verify_single_image, f_path): label
            for f_path, label in candidate_files
        }
        for future in as_completed(future_to_label):
            label = future_to_label[future]
            f_path, is_ok = future.result()
            if is_ok:
                valid_paths.append(f_path)
                valid_labels.append(label)
            else:
                skipped_count += 1
                print(f"[WARN] Skipped corrupted or invalid file: {f_path}")

    if skipped_count > 0:
        print(f"[INFO] Skipped {skipped_count} corrupted/unreadable images.")

    return valid_paths, valid_labels, class_names


def build_output_dirs(output_dir: Path, class_names: List[str]) -> Dict[str, Path]:
    """
    Creates target split folder structure (train, val, test) preserving class subfolders.
    """
    split_map = {}
    for split in ["train", "val", "test"]:
        s_dir = output_dir / split
        split_map[split] = s_dir
        for c_name in class_names:
            (s_dir / c_name).mkdir(parents=True, exist_ok=True)
    return split_map


def copy_single_file(item: Tuple[Path, str, Path]) -> None:
    """Helper worker to copy a single file efficiently."""
    src_file, label, target_split_dir = item
    dest_path = target_split_dir / label / src_file.name
    shutil.copy2(src_file, dest_path)


def copy_files_parallel(file_paths: List[Path], labels: List[str], target_split_dir: Path) -> None:
    """
    Multi-threaded fast copying of image files to target directory.
    """
    tasks = [(f, l, target_split_dir) for f, l in zip(file_paths, labels)]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        list(executor.map(copy_single_file, tasks))


def display_summary(
    class_names: List[str],
    train_labels: List[str],
    val_labels: List[str],
    test_labels: List[str]
) -> None:
    """
    Displays the formatted summary table of split statistics.
    """
    tr_counts = Counter(train_labels)
    va_counts = Counter(val_labels)
    te_counts = Counter(test_labels)

    print("\n" + "=" * 65)
    print(f"{'Class':<25} {'Train':<10} {'Val':<10} {'Test':<10} {'Total':<10}")
    print("-" * 65)

    tot_train = tot_val = tot_test = 0

    for c in class_names:
        tr = tr_counts.get(c, 0)
        va = va_counts.get(c, 0)
        te = te_counts.get(c, 0)
        tot = tr + va + te

        tot_train += tr
        tot_val += va
        tot_test += te

        print(f"{c:<25} {tr:<10} {va:<10} {te:<10} {tot:<10}")

    print("-" * 65)
    total_images = tot_train + tot_val + tot_test
    print(f"{'TOTAL':<25} {tot_train:<10} {tot_val:<10} {tot_test:<10} {total_images:<10}")
    print("=" * 65)

    print("\nTotal Images:")
    print(f"Training  : {tot_train}")
    print(f"Validation: {tot_val}")
    print(f"Testing   : {tot_test}")
    print(f"Grand Total: {total_images}\n")


# =============================================================================
# MAIN SPLITTING PIPELINE
# =============================================================================
def run_split(source_path: str, output_path: str, seed: int = SEED) -> None:
    """
    Executes complete stratified splitting workflow for a given dataset.
    """
    src_dir = Path(source_path).resolve()
    out_dir = Path(output_path).resolve()

    print(f"\n=========================================================")
    print(f"Processing Dataset Split")
    print(f"Source Folder : {src_dir}")
    print(f"Output Folder : {out_dir}")
    print(f"=========================================================")

    set_seed(seed)

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"[ERROR] Source folder does not exist: {src_dir}")
        return

    # Step 1: Scan and verify images
    print("[1/5] Scanning and verifying image integrity...")
    valid_paths, labels, class_names = scan_dataset(src_dir)

    if not valid_paths:
        print("[ERROR] No valid images found.")
        return

    print(f"[INFO] Found {len(valid_paths)} valid images across {len(class_names)} classes.")

    # Step 2: Stratified Split
    print("[2/5] Performing stratified train/val/test split...")
    temp_ratio = VAL_RATIO + TEST_RATIO  # 0.30
    train_paths, temp_paths, train_labels, temp_labels = train_test_split(
        valid_paths,
        labels,
        test_size=temp_ratio,
        random_state=seed,
        stratify=labels
    )

    val_relative_ratio = VAL_RATIO / temp_ratio  # 0.50
    val_paths, test_paths, val_labels, test_labels = train_test_split(
        temp_paths,
        temp_labels,
        test_size=(1.0 - val_relative_ratio),
        random_state=seed,
        stratify=temp_labels
    )

    # Step 3: Create Output Directory Structure
    print("[3/5] Building dataset_split directory tree...")
    split_map = build_output_dirs(out_dir, class_names)

    # Step 4: Parallel Copying
    print("[4/5] Copying images (parallel multi-threaded)...")
    copy_files_parallel(train_paths, train_labels, split_map["train"])
    copy_files_parallel(val_paths, val_labels, split_map["val"])
    copy_files_parallel(test_paths, test_labels, split_map["test"])

    # Step 5: Summary Table
    print("[5/5] Generating dataset distribution summary...")
    display_summary(class_names, train_labels, val_labels, test_labels)
    print(f"[SUCCESS] Completed split for {src_dir.name} -> {out_dir}\n")


if __name__ == "__main__":
    # Check if specified single SOURCE_DATASET exists
    if Path(SOURCE_DATASET).exists():
        run_split(SOURCE_DATASET, OUTPUT_FOLDER, seed=SEED)
    else:
        # Batch process each model dataset folder individually
        processed = False
        for model_path_str in MODEL_DATASETS:
            m_path = Path(model_path_str)
            if m_path.exists():
                out_path = m_path.parent / "dataset_split"
                run_split(str(m_path), str(out_path), seed=SEED)
                processed = True

        if not processed:
            # Fallback to run default configuration
            run_split(SOURCE_DATASET, OUTPUT_FOLDER, seed=SEED)
