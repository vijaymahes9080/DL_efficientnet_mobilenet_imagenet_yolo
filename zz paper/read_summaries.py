import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'd:\college\DL 4 models'
folders = ['DL - efficientnet b0', 'DL - imagenet', 'DL - mobilenet', 'DL -YOLO']
files_to_check = ['PROJECT_SUMMARY.md', 'DEEP_LEARNING_BLUEPRINT.md', 'PHASE_REPORT.txt', 'config.py']

for f in folders:
    print(f'========================================')
    print(f'FOLDER: {f}')
    print(f'========================================')
    for fn in files_to_check:
        fpath = os.path.join(base, f, fn)
        if os.path.exists(fpath):
            print(f'--- File: {fn} ---')
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                for l in lines[:100]:  # read first 100 lines for extensive details
                    print(l.rstrip())
            print('\n' + '='*40 + '\n')
