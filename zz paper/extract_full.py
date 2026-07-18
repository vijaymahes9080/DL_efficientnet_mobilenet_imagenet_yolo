import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

base = r'd:\college\DL 4 models'
models_folders = {
    'EfficientNetB0': 'DL - efficientnet b0',
    'ResNet50': 'DL - imagenet',
    'MobileNetV2': 'DL - mobilenet',
    'YOLOv8': 'DL -YOLO'
}

for name, folder in models_folders.items():
    print(f'\n========== {name} FULL EXPERIMENT HISTORY ==========')
    exp_path = os.path.join(base, folder, 'logs', 'experiment_history.json')
    if os.path.exists(exp_path):
        with open(exp_path, 'r') as f:
            data = json.load(f)
        print(json.dumps(data, indent=2))
    else:
        print(f'[MISSING] {exp_path}')
    
    print(f'\n--- {name} PER-CLASS REPORT ---')
    for fn in ['per_class_report.json', 'class_report.json', 'evaluation_report.json', 'champion_metrics.json']:
        rp = os.path.join(base, folder, 'logs', fn)
        if os.path.exists(rp):
            with open(rp, 'r') as f:
                d = json.load(f)
            print(f'[FILE: {fn}]')
            print(json.dumps(d, indent=2))
            break
    else:
        # Try logs folder listing
        logs_dir = os.path.join(base, folder, 'logs')
        if os.path.isdir(logs_dir):
            print(f'Log files in {logs_dir}:')
            for fn in os.listdir(logs_dir):
                fpath = os.path.join(logs_dir, fn)
                size = os.path.getsize(fpath)
                print(f'  {fn} ({size} bytes)')
