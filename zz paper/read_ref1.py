import sys, fitz
sys.stdout.reconfigure(encoding='utf-8')

# Read model ref.pdf - clean text per page
print("=== MODEL REF.PDF - CLEAN TEXT ===")
doc1 = fitz.open(r'd:\college\DL 4 models\zz paper\model ref.pdf')
print(f'Total pages: {len(doc1)}')
for i, page in enumerate(doc1):
    text = page.get_text()
    print(f'\n--- PAGE {i+1} ---')
    print(text)
doc1.close()
