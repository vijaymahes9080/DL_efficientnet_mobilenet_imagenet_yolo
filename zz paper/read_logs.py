import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'd:\college\DL 4 models'
folders = ['DL - efficientnet b0', 'DL - imagenet', 'DL - mobilenet', 'DL -YOLO']

for f in folders:
    print(f'========================================')
    print(f'FOLDER: {f} / logs/')
    print(f'========================================')
    log_dir = os.path.join(base, f, 'logs')
    if os.path.exists(log_dir):
        files = os.listdir(log_dir)
        print(f'Files in logs: {files}')
        for fn in sorted(files):
            fpath = os.path.join(log_dir, fn)
            if os.path.isfile(fpath):
                print(f'\n--- File: {fn} ({os.path.getsize(fpath)} bytes) ---')
                # Read first 15 lines and last 15 lines of log files to understand structure
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                if len(lines) <= 30:
                    for l in lines:
                        print(l.rstrip())
                else:
                    print('[FIRST 15 LINES]')
                    for l in lines[:15]:
                        print(l.rstrip())
                    print('...')
                    print('[LAST 15 LINES]')
                    for l in lines[-15:]:
                        print(l.rstrip())
            else:
                print(f'\n--- Directory: {fn}/ ---')
    else:
        print('Logs directory does not exist.')
    print('\n' + '='*40 + '\n')
