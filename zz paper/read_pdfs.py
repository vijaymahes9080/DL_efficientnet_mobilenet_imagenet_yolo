import sys, fitz
sys.stdout.reconfigure(encoding='utf-8')

print("=== MODEL REF.PDF ===")
doc1 = fitz.open(r'd:\college\DL 4 models\zz paper\model ref.pdf')
print(f'Pages: {len(doc1)}')
for i, page in enumerate(doc1):
    text = page.get_text()
    blocks = page.get_text("dict")["blocks"]
    print(f'\n--- PAGE {i+1} ---')
    # Print text blocks with font info
    for b in blocks:
        if b["type"] == 0:
            for line in b["lines"]:
                for span in line["spans"]:
                    txt = span["text"].strip()
                    if txt:
                        print(f'  [Font={span["font"]}, Size={span["size"]:.1f}, Color={span["color"]}] {txt[:120]}')
doc1.close()

print("\n\n=== MODEL REFERENCES.PDF ===")
doc2 = fitz.open(r'd:\college\DL 4 models\zz paper\model references.pdf')
print(f'Pages: {len(doc2)}')
for i, page in enumerate(doc2):
    blocks = page.get_text("dict")["blocks"]
    print(f'\n--- PAGE {i+1} ---')
    for b in blocks:
        if b["type"] == 0:
            for line in b["lines"]:
                for span in line["spans"]:
                    txt = span["text"].strip()
                    if txt:
                        print(f'  [Font={span["font"]}, Size={span["size"]:.1f}, Color={span["color"]}] {txt[:120]}')
doc2.close()
