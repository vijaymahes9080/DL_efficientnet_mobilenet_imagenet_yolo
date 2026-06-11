import os
import pandas as pd
import logging

# Basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Use the same config if possible, or fallback
try:
    import config
except ImportError:
    class Config:
        BASE_PATH = os.getcwd()
        DATASET_PATH = os.path.join(BASE_PATH, 'dataset')
        MODEL_PATH = os.path.join(BASE_PATH, 'models')
        LOG_PATH = os.path.join(BASE_PATH, 'logs')
    config = Config()

def run_ablation_scenario(name, disable_aug=False, epochs=5):
    logger.info(f"--- Running Ablation Scenario: {name} ---")

    try:
        from ultralytics import YOLO
    except ImportError:
        logger.error("ultralytics not installed. Run: pip install ultralytics")
        return 0.0

    model_file = os.path.join(config.MODEL_PATH, 'champion_model_mastery.pt')
    if not os.path.exists(model_file):
        # Fallback to the .pt model in the root folder
        model_file = 'yolov8n-cls.pt'

    # Augmentation flags via YOLO training args
    aug_args = {} if disable_aug else {
        'fliplr': 0.5,
        'degrees': 20.0,
    }
    no_aug_args = {
        'fliplr': 0.0,
        'degrees': 0.0,
    } if disable_aug else {}
    train_args = {**aug_args, **no_aug_args}

    try:
        model = YOLO(model_file)
        results = model.train(
            data=config.DATASET_PATH,
            epochs=epochs,
            imgsz=224,
            batch=16,
            verbose=False,
            project=config.LOG_PATH,
            name=f'ablation_{name.replace(" ", "_")}',
            exist_ok=True,
            fraction=0.2,
            **train_args
        )
        # Get top-1 accuracy from results
        val_acc = float(results.results_dict.get('metrics/accuracy_top1', 0.0))
        logger.info(f"Scenario '{name}' completed with Val Accuracy: {val_acc:.4f}")
        return val_acc
    except Exception as e:
        logger.error(f"YOLO training failed for scenario '{name}': {e}")
        return 0.0


def main():
    results = []

    results.append({'scenario': 'Standard Pipeline',
                    'accuracy': run_ablation_scenario('Standard', disable_aug=False, epochs=10)})
    results.append({'scenario': 'No Augmentation',
                    'accuracy': run_ablation_scenario('No Augmentation', disable_aug=True, epochs=10)})

    df = pd.DataFrame(results)
    df['performance_drop'] = df['accuracy'].iloc[0] - df['accuracy']

    output_path = os.path.join(config.LOG_PATH, 'ablation_results.csv')
    df.to_csv(output_path, index=False)
    logger.info(f"Ablation results saved to {output_path}")
    logger.info(f"Summary:\n{df.to_string(index=False)}")


if __name__ == "__main__":
    main()
