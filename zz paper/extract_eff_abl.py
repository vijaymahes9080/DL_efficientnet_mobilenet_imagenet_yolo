import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

base = r'd:\college\DL 4 models'

# EfficientNet experiment history
print("=== EfficientNetB0 EXPERIMENT HISTORY ===")
ep = os.path.join(base, 'DL - efficientnet b0', 'logs', 'experiment_history.json')
with open(ep, 'r') as f:
    d = json.load(f)
print(json.dumps(d, indent=2))

print("\n=== ABLATION CSVs ===")
for name, folder in [('EfficientNetB0','DL - efficientnet b0'),('ResNet50','DL - imagenet'),('MobileNetV2','DL - mobilenet'),('YOLOv8','DL -YOLO')]:
    cp = os.path.join(base, folder, 'logs', 'ablation_results.csv')
    if os.path.exists(cp):
        with open(cp, 'r') as f:
            print(f'\n[{name}] ablation_results.csv:')
            print(f.read())

print("\n=== ResNet50 TRAINING LOG (full) ===")
lp = os.path.join(base, 'DL - imagenet', 'logs', 'training_full.log')
with open(lp, 'r', errors='replace') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for l in lines:
    stripped = l.strip()
    if any(k in stripped for k in ['Phase','Epoch','Cycle','cycle','acc=','Acc=','val_acc=','Champion','METRICS','TERMINATING','Mastery','STARTING']):
        print(f'  {stripped}')

print("\n=== MobileNetV2 TRAINING LOG (key lines) ===")
lp = os.path.join(base, 'DL - mobilenet', 'logs', 'training_full.log')
with open(lp, 'r', errors='replace') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for l in lines:
    stripped = l.strip()
    if any(k in stripped for k in ['Phase','Epoch','Cycle','cycle','acc=','Acc=','val_acc=','Champion','METRICS','TERMINATING','Mastery','STARTING', 'Validation Acc', 'Final']):
        print(f'  {stripped}')

print("\n=== EfficientNetB0 TRAINING LOG (key lines) ===")
lp = os.path.join(base, 'DL - efficientnet b0', 'logs', 'training_full.log')
with open(lp, 'r', errors='replace') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for l in lines:
    stripped = l.strip()
    if any(k in stripped for k in ['Phase','Epoch','Cycle','cycle','acc=','Acc=','val_acc=','Champion','METRICS','TERMINATING','Mastery','STARTING', 'Validation Acc', 'Final']):
        print(f'  {stripped}')
