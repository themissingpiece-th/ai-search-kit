#!/usr/bin/env python3
"""Turn a prompt-finder JSON file into an Excel workbook + an import CSV for the tracking system.

Usage: python3 make_outputs.py prompts.json <brand-slug> [out_dir]
Writes: prompt-set-<brand>.xlsx and prompt-set-import-<brand>.csv
Needs openpyxl for the .xlsx (pip install openpyxl). The CSV is written even without it.

JSON shape:
{
  "brand": "BYD", "aliases": ["BYD", "บีวายดี"], "website": "https://www.byd.com/th",
  "product": "...", "audience": "...", "competitors": ["MG", "Tesla"], "market": "TH", "language": "th",
  "topics": [{"name": "ชาร์จสะดวก", "evidence": "ลูกค้าถามบ่อยเรื่องชาร์จที่คอนโด"}],
  "prompts": [
    {"prompt": "...", "topic": "ชาร์จสะดวก", "stage": "Discovery|Evaluation|Comparison|Decision",
     "branded": false, "source": "customer|gsc|keyword|ai",
     "scores": {"business": 3, "demand": 2, "mention": 3, "win": 2, "risk": 2},
     "selected": true, "why": "..."}
  ]
}
"""
import csv, json, os, sys

W = {'business': .30, 'demand': .20, 'mention': .20, 'win': .15, 'risk': .15}
STAGES = ('Discovery', 'Evaluation', 'Comparison', 'Decision')
SRC = {'customer': 'ลูกค้าถามจริง', 'gsc': 'Google Search Console', 'keyword': 'keyword / AI volume', 'ai': 'AI ช่วยคิด'}
PLATFORMS = ('Google AI Overviews', 'Google AI Mode', 'ChatGPT', 'Gemini')


def score(p):
    s = p.get('scores', {})
    if p.get('branded'):
        s = {**s, 'mention': 3}
    return round(sum(W[k] * s.get(k, 1) for k in W), 1)


def check(d, chosen):
    warn = []
    nb = [p for p in chosen if not p.get('branded')]
    b = [p for p in chosen if p.get('branded')]
    if len(chosen) != 10:
        warn.append(f'เลือก {len(chosen)} ข้อ (ควรเป็น 10)')
    if len(nb) != 7 or len(b) != 3:
        warn.append(f'non-branded {len(nb)} / branded {len(b)} (ควรเป็น 7 / 3)')
    if sum(p.get('stage') in ('Comparison', 'Decision') for p in nb) < 5:
        warn.append('non-branded ที่เป็น Comparison/Decision น้อยกว่า 5 ข้อ')
    if sum(p.get('stage') == 'Discovery' for p in chosen) > 1:
        warn.append('Discovery เกิน 1 ข้อ')
    names = [a.lower() for a in d.get('aliases', [])] + [d.get('brand', '').lower()]
    for p in nb:
        if any(n and n in p['prompt'].lower() for n in names):
            warn.append(f'non-branded มีชื่อแบรนด์: {p["prompt"][:40]}…')
    for p in chosen:
        if p.get('stage') not in STAGES:
            warn.append(f'stage ไม่ถูกต้อง: {p.get("stage")}')
    return warn


def write_csv(chosen, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['prompt', 'topic', 'branded', 'stage', 'source', 'score', 'why'])
        for p in chosen:
            w.writerow([p['prompt'], p.get('topic', ''), 'Y' if p.get('branded') else 'N', p.get('stage', ''),
                        p.get('source', 'ai'), p['score'], p.get('why', '')])


def write_xlsx(d, ps, chosen, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    head = PatternFill('solid', fgColor='152641')
    pick = PatternFill('solid', fgColor='F7F5EC')

    def sheet(ws, headers, rows, widths):
        ws.append(headers)
        for c in ws[1]:
            c.font = Font(bold=True, color='FFFFFF'); c.fill = head
            c.alignment = Alignment(vertical='center', wrap_text=True)
        for r in rows:
            ws.append(r)
        for i, wd in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = wd
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(vertical='top', wrap_text=True)
        ws.freeze_panes = 'A2'

    wb = Workbook()
    ws = wb.active; ws.title = 'Prompt Set (track)'
    sheet(ws, ['#', 'Prompt', 'หัวข้อ (เกณฑ์ตัดสินใจ)', 'Branded?', 'ขั้น', 'ที่มา', 'คะแนน (1–3)', 'ทำไมเลือก'],
          [[i + 1, p['prompt'], p.get('topic'), 'Branded' if p.get('branded') else 'Non-branded', p.get('stage'),
            SRC.get(p.get('source'), p.get('source')), p['score'], p.get('why', '')] for i, p in enumerate(chosen)],
          [4, 60, 20, 13, 12, 18, 11, 40])

    ws = wb.create_sheet('ผู้สมัครทั้งหมด')
    rows = sorted(ps, key=lambda p: (p.get('topic', ''), -p['score']))
    keys = list(W)
    sheet(ws, ['Prompt', 'หัวข้อ', 'Branded?', 'ขั้น', 'ที่มา', 'ธุรกิจ 30%', 'ความต้องการ 20%', 'เอ่ยชื่อ 20%',
               'โอกาสชนะ 15%', 'ความเสี่ยง 15%', 'คะแนน', 'เลือก'],
          [[p['prompt'], p.get('topic'), 'Branded' if p.get('branded') else 'Non-branded', p.get('stage'),
            SRC.get(p.get('source'), p.get('source'))] + [p.get('scores', {}).get(k) for k in keys] +
           [p['score'], '✓' if p.get('selected') else ''] for p in rows],
          [60, 18, 13, 12, 18, 9, 11, 9, 10, 10, 8, 7])
    for row in ws.iter_rows(min_row=2):
        if row[-1].value == '✓':
            for c in row:
                c.fill = pick

    ws = wb.create_sheet('Tracking (วัดด้วยมือ)')
    sheet(ws, ['วันที่', 'Prompt', 'แพลตฟอร์ม', 'รอบที่', 'ถูกเอ่ยชื่อไหม (Y/N)', 'ลำดับที่เอ่ยครั้งแรก',
               'แบรนด์ที่ถูกเอ่ยทั้งหมด', 'เว็บเราถูกอ้างไหม (Y/N)', 'เว็บที่ถูกอ้าง', 'ข้อมูลถูกต้องไหม', 'หมายเหตุ'],
          [['', p['prompt'], pl, r, '', '', '', '', '', '', ''] for p in chosen for pl in PLATFORMS for r in (1, 2, 3)],
          [11, 50, 18, 7, 13, 12, 28, 14, 28, 14, 24])

    ws = wb.create_sheet('วิธีใช้')
    info = [
        ['แบรนด์', f"{d.get('brand', '')} ({', '.join(d.get('aliases', []))})"], ['เว็บไซต์', d.get('website', '')],
        ['สินค้า / บริการ', d.get('product', '')], ['กลุ่มลูกค้า', d.get('audience', '')],
        ['คู่แข่ง', ', '.join(d.get('competitors', []))], ['ตลาด / ภาษา', f"{d.get('market', '')} / {d.get('language', '')}"],
        ['หัวข้อที่โฟกัส', ' · '.join(t['name'] for t in d.get('topics', []))],
        ['', ''],
        ['ชีต Prompt Set', '10 ข้อที่ควร track: non-branded 7 (AI เลือกเราไหม) + branded 3 (AI พูดถึงเราถูกไหม)'],
        ['นำเข้าระบบวัดผล', 'ใช้ไฟล์ prompt-set-import-*.csv ที่ได้มาพร้อมกัน'],
        ['วัดด้วยมือ', 'ชีต Tracking: ถามแต่ละข้อใน Google AI Overviews → Google AI Mode → ChatGPT → Gemini รอบละ 3 ครั้ง (ไม่ login) แล้วกรอก · วัดซ้ำรายสัปดาห์ด้วยถ้อยคำเดิม'],
        ['Mention rate', 'จำนวนคำตอบที่มีชื่อเรา ÷ คำตอบทั้งหมด (คิดแยก non-branded กับ branded) · ไม่มี "อันดับใน AI" ให้ดูแนวโน้ม'],
        ['คะแนน', '0.30×ธุรกิจ + 0.20×ความต้องการ + 0.20×เอ่ยชื่อ + 0.15×โอกาสชนะ + 0.15×ความเสี่ยงถ้า AI ตอบผิด (แต่ละด้าน 1–3)'],
        ['ข้อควรรู้', 'prompt ไม่มี search volume จริง · ที่มา "AI ช่วยคิด" ควรเทียบกับคำถามลูกค้าจริงก่อนใช้ · ไม่ใส่ปีใน prompt'],
        ['อ้างอิงแนวคิด', 'Prompt Map · แนวคิดจาก AI SEO For Dummies (Nathan Gotch, Wiley 2026) บทที่ 5, 9 — สรุปด้วยคำของเรา'],
    ]
    for r in info:
        ws.append(r)
    ws.column_dimensions['A'].width = 18; ws.column_dimensions['B'].width = 100
    for row in ws.iter_rows():
        row[0].font = Font(bold=True)
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(path)


def main(src, slug, out='.'):
    d = json.load(open(src, encoding='utf-8'))
    ps = d['prompts']
    for p in ps:
        p['score'] = score(p)
    chosen = [p for p in ps if p.get('selected')]
    chosen.sort(key=lambda p: (p.get('branded', False), -p['score']))
    os.makedirs(out, exist_ok=True)
    csv_path = os.path.join(out, f'prompt-set-import-{slug}.csv')
    write_csv(chosen, csv_path)
    print(f'saved {csv_path}')
    try:
        xlsx_path = os.path.join(out, f'prompt-set-{slug}.xlsx')
        write_xlsx(d, ps, chosen, xlsx_path)
        print(f'saved {xlsx_path}: {len(chosen)} selected / {len(ps)} candidates')
    except ImportError:
        print('openpyxl not installed → only CSV written (pip install openpyxl for the Excel file)')
    for w in check(d, chosen):
        print('WARN:', w)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
