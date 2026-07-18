import sys, fitz
sys.stdout.reconfigure(encoding='utf-8')

print("=== MODEL REFERENCES.PDF - CLEAN TEXT ===")
doc2 = fitz.open(r'd:\college\DL 4 models\zz paper\model references.pdf')
print(f'Total pages: {len(doc2)}')
for i, page in enumerate(doc2):
    text = page.get_text()
    print(f'\n--- PAGE {i+1} ---')
    print(text)
doc2.close()
