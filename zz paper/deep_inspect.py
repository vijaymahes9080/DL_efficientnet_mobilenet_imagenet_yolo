import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'd:\college\DL 4 models'
models = {
    'EfficientNetB0': 'DL - efficientnet b0',
    'ResNet50': 'DL - imagenet',
    'MobileNetV2': 'DL - mobilenet',
    'YOLOv8': 'DL -YOLO'
}

all_data = {}

for name, folder in models.items():
    print(f'\n========== {name} ==========')
    m_data = {'cycles': [], 'log_events': [], 'hyper': []}
    
    # 1. Experiment history
    exp_path = os.path.join(base, folder, 'logs', 'experiment_history.json')
    if os.path.exists(exp_path):
        with open(exp_path, 'r') as f:
            data = json.load(f)
        print(f'  Experiment Cycles: {len(data)}')
        for entry in data:
            c = entry['cycle']
            r = entry['result']
            row = {
                'cycle': c,
                'change': entry.get('change', 'N/A'),
                'reason': entry.get('reason', 'N/A'),
                'accuracy': r.get('accuracy', r.get('val_accuracy', 0)),
                'val_accuracy': r.get('val_accuracy', 0),
                'train_accuracy': r.get('train_accuracy', 0),
                'val_loss': r.get('val_loss', 0),
                'mastery_score': r.get('mastery_score', 0),
                'precision_macro': r.get('precision_macro', 0),
                'recall_macro': r.get('recall_macro', 0),
                'f1_macro': r.get('f1_macro', 0),
                'mcc': r.get('mcc', 0),
                'auc_roc': r.get('auc_roc', 0),
                'log_loss': r.get('log_loss', 0),
                'cohen_kappa': r.get('cohen_kappa', 0),
                'inference_time_ms': r.get('inference_time_ms', 0),
                'params_millions': r.get('params_millions', 0),
                'model_size_mb': r.get('model_size_mb', 0),
                'val_loss_history': r.get('val_loss_history', []),
            }
            m_data['cycles'].append(row)
            print(f'  Cycle {c}: change={row["change"]} | acc={row["accuracy"]:.4f} | val_acc={row["val_accuracy"]:.4f} | f1={row["f1_macro"]:.4f} | mcc={row["mcc"]:.4f} | mastery={row["mastery_score"]}')
    else:
        print(f'  [NO EXP JSON] at {exp_path}')
    
    # 2. hyper tuning CSV
    csv_path = os.path.join(base, folder, 'hyper_tuning_results.csv')
    if os.path.exists(csv_path):
        with open(csv_path, 'r', errors='replace') as f:
            lines = f.readlines()
        print(f'\n  Hyper tuning CSV ({len(lines)} rows):')
        for i, l in enumerate(lines[:50]):
            print(f'    {l.rstrip()}')
    
    # 3. Full training log – extract epoch lines
    log_path = os.path.join(base, folder, 'logs', 'training_full.log')
    if os.path.exists(log_path):
        with open(log_path, 'r', errors='replace') as f:
            lines = f.readlines()
        print(f'\n  Training log ({len(lines)} lines):')
        for l in lines:
            stripped = l.strip()
            if any(k in stripped for k in ['Epoch', 'Phase', 'CYCLE', 'Champion', 'METRICS', 'TERMINATING', 'Acc=', 'val_acc=', 'Final', 'Mastery']):
                print(f'    {stripped}')
    
    all_data[name] = m_data
    print()

# Also check per_class_report
for name, folder in models.items():
    rp = os.path.join(base, folder, 'logs', 'per_class_report.json')
    if os.path.exists(rp):
        with open(rp, 'r') as f:
            d = json.load(f)
        print(f'\n=== {name} Per-Class Report ===')
        print(json.dumps(d, indent=2))
