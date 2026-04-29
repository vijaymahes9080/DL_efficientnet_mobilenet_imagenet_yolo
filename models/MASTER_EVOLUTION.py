import os
import subprocess
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define target directories
MODEL_DIRECTORIES = [
    "DL -YOLO",
    "DL - imagenet",
    "DL - efficientnet b0",
    "DL - mobilenet"
]

def log_message(message, model_name="SYSTEM"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{model_name}] {message}")

def run_model_pipeline(path, name, base_path):
    """
    Executes the full evolution pipeline for a specific model node.
    """
    full_path = os.path.join(base_path, path)
    log_message(f"--- STARTING PARALLEL EVOLUTION ---", name)
    
    # 1. Training Phase
    log_message(f"EXECUTING TRAINING: train_local.py", name)
    train_result = subprocess.run(
        [sys.executable, "train_local.py"],
        cwd=full_path,
        capture_output=False,
        text=True
    )
    
    if train_result.returncode != 0:
        log_message(f"CRITICAL FAILURE: Training aborted.", name)
        return False

    # 2. Post-Ops (Evaluation, XAI, Reporting)
    log_message(f"STARTING POST-OPS (Audit & XAI)", name)
    
    # Auto-Test
    subprocess.run([sys.executable, "AUTO_TEST_MODELS.py", "--evaluate"], cwd=full_path)
    
    # XAI
    subprocess.run([sys.executable, "xai_ablation.py", name.lower()], cwd=full_path)
    
    # Report Generation
    if os.path.exists(os.path.join(full_path, "generate_report.py")):
        subprocess.run([sys.executable, "generate_report.py"], cwd=full_path)
        
    log_message(f"--- EVOLUTION MISSION COMPLETE ---", name)
    return True

def run_evolution():
    log_message("==================================================")
    log_message("      NEURAL SYNERGY - PARALLEL MASTERY 40X       ")
    log_message("==================================================")
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    models = [
        ("DL -YOLO", "YOLOv8"),
        ("DL - imagenet", "ResNet50"),
        ("DL - efficientnet b0", "EfficientNet"),
        ("DL - mobilenet", "MobileNet")
    ]

    log_message(f"Initializing ThreadPoolExecutor with {len(models)} workers...")
    
    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = {
            executor.submit(run_model_pipeline, path, name, base_path): name 
            for path, name in models
        }
        
        for future in as_completed(futures):
            name = futures[future]
            try:
                success = future.result()
                if success:
                    log_message(f"Global status: SUCCESS", name)
                else:
                    log_message(f"Global status: FAILED", name)
            except Exception as exc:
                log_message(f"Generated an exception: {exc}", name)

    log_message("==================================================")
    log_message("      ALL NEURAL NODES SYNCHRONIZED               ")
    log_message("==================================================")


if __name__ == "__main__":
    run_evolution()

