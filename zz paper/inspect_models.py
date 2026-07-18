import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

models = {
    'EfficientNetB0': 'DL - efficientnet b0',
    'ResNet50': 'DL - imagenet',
    'MobileNetV2': 'DL - mobilenet',
    'YOLOv8': 'DL -YOLO'
}
base = r'd:\college\DL 4 models'

for name, folder in models.items():
    print(f'=== {name} ===')
    exp_path = os.path.join(base, folder, 'logs', 'experiment_history.json')
    if os.path.exists(exp_path):
        with open(exp_path, 'r') as f:
            data = json.load(f)
        for entry in data:
            c = entry['cycle']
            ch = entry['change']
            re = entry['reason']
            r = entry['result']
            print(f'  Cycle {c}: change={ch}, reason={re}')
            for k, v in r.items():
                print(f'    {k}: {v}')
            print()
    else:
        print(f'  [MISSING] {exp_path}')
    
    # Also check hyper tuning CSV
    csv_path = os.path.join(base, folder, 'hyper_tuning_results.csv')
    if os.path.exists(csv_path):
        print(f'  [CSV] hyper_tuning_results.csv EXISTS at {csv_path}')
    
    # Check training log
    log_path = os.path.join(base, folder, 'logs', 'training_full.log')
    if os.path.exists(log_path):
        with open(log_path, 'r', errors='replace') as f:
            lines = f.readlines()
        print(f'  [LOG] training_full.log: {len(lines)} lines')
        # Print last 30 lines
        for l in lines[-30:]:
            print(f'    {l.rstrip()}')
    print()
