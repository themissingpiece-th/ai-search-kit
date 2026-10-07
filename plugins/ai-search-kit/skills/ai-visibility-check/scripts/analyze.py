#!/usr/bin/env python3
"""Summarise AI visibility tracking results.

Usage: python3 analyze.py <results.csv|prompt-set-*.xlsx> [--brand BYD] [--out report]
Input A: tracking export CSV from the class system, columns:
  run_date,run_label,project_brand,prompt,topic,branded,stage,platform,run_no,status,
  brand_mentioned,first_position,brands_mentioned,our_domain_cited,cited_domains,answer_text
Input B: the "Tracking (วัดด้วยมือ)" sheet of prompt-finder's Excel (needs openpyxl).
Writes <out>.json (numbers for the AI to reason over) and <out>.md (tables for the user).
Only rows with status=ok count in rates; errors / no answer are reported separately.
"""
import csv, json, sys
from collections import Counter, defaultdict

POS_W = {1: 1.0, 2: 0.8, 3: 0.6, 4: 0.4}  # >=5 -> 0.2, absent -> 0
PLAT = {'ai_overview': 'Google AI Overviews', 'ai_mode': 'Google AI Mode', 'chatgpt': 'ChatGPT', 'gemini': 'Gemini'}
PLAT_IN = {v.lower(): k for k, v in PLAT.items()}
ORDER = list(PLAT)


def yn(v):
    return str(v).strip().upper() in ('Y', 'YES', 'TRUE', '1', 'ใช่')


def pos_w(p):
    try:
        p = int(p)
    except (TypeError, ValueError):
        return 0
    return POS_W.get(p, 0.2) if p > 0 else 0


def load(path):
    if path.endswith('.xlsx'):
        from openpyxl import load_workbook
        ws = load_workbook(path, read_only=True)['Tracking (วัดด้วยมือ)']
        it = ws.iter_rows(values_only=True); next(it)
        meta = {}
        try:
            for r in load_workbook(path, read_only=True)['Prompt Set (track)'].iter_rows(min_row=2, values_only=True):
                meta[r[1]] = {'topic': r[2], 'branded': 'Y' if r[3] == 'Branded' else 'N', 'stage': r[4]}
        except KeyError:
            pass
        rows = []
        for r in it:
            if not r[4]:
                continue  # not filled in
            m = meta.get(r[1], {})
            rows.append({'run_date': str(r[0] or ''), 'prompt': r[1], 'platform': PLAT_IN.get(str(r[2]).lower(), r[2]),
                         'run_no': r[3], 'status': 'ok', 'brand_mentioned': r[4], 'first_position': r[5],
                         'brands_mentioned': str(r[6] or '').replace(',', '|'), 'our_domain_cited': r[7],
                         'cited_domains': str(r[8] or '').replace(',', '|'), 'topic': m.get('topic', ''),
                         'branded': m.get('branded', 'N'), 'stage': m.get('stage', '')})
        return rows
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def split(v):
    return [x.strip() for x in str(v or '').split('|') if x.strip()]


def rate(rows):
    ok = [r for r in rows if r.get('status', 'ok') == 'ok']
    return (round(100 * sum(yn(r['brand_mentioned']) for r in ok) / len(ok)) if ok else None), len(ok)


def main(path, brand=None, out='report'):
    rows = load(path)
    brand = brand or (rows[0].get('project_brand') if rows else '') or 'เรา'
    errors = Counter(r.get('status') for r in rows if r.get('status', 'ok') != 'ok')
    res = {'brand': brand, 'rows': len(rows), 'errors': dict(errors), 'run_dates': sorted({r.get('run_date', '') for r in rows})}

    for label, flag in (('non_branded', 'N'), ('branded', 'Y')):
        sub = [r for r in rows if str(r.get('branded', 'N')).upper() == flag]
        m, n = rate(sub)
        block = {'mention_rate': m, 'answers': n, 'by_platform': {}, 'by_topic': {}, 'prompts': []}
        for p in ORDER:
            pr, pn = rate([r for r in sub if r.get('platform') == p])
            if pn:
                block['by_platform'][PLAT[p]] = {'mention_rate': pr, 'answers': pn}
        for t in sorted({r.get('topic', '') for r in sub}):
            tr, tn = rate([r for r in sub if r.get('topic', '') == t])
            block['by_topic'][t or '-'] = {'mention_rate': tr, 'answers': tn}
        # share of voice (position weighted) + competitor counts, per platform
        sov = defaultdict(lambda: defaultdict(float)); comp = Counter()
        for r in sub:
            if r.get('status', 'ok') != 'ok':
                continue
            names = split(r.get('brands_mentioned'))
            for i, b in enumerate(names, 1):
                sov[r['platform']][b] += POS_W.get(i, 0.2)
                if b.lower() != brand.lower():
                    comp[b] += 1
        block['sov'] = {PLAT.get(p, p): {b: round(100 * v / sum(d.values()), 1) for b, v in sorted(d.items(), key=lambda x: -x[1])[:6]}
                        for p, d in sov.items() if sum(d.values())}
        block['top_competitors'] = comp.most_common(6)
        # per prompt × platform status
        for pr in dict.fromkeys(r['prompt'] for r in sub):
            prs = [r for r in sub if r['prompt'] == pr]
            entry = {'prompt': pr, 'topic': prs[0].get('topic', ''), 'stage': prs[0].get('stage', ''), 'platforms': {}}
            for p in ORDER:
                ps = [r for r in prs if r.get('platform') == p and r.get('status', 'ok') == 'ok']
                if not ps:
                    continue
                ours = sum(yn(r['brand_mentioned']) for r in ps)
                others = Counter(b for r in ps for b in split(r.get('brands_mentioned')) if b.lower() != brand.lower())
                best = others.most_common(1)[0] if others else (None, 0)
                status = 'Absent' if ours == 0 else ('Lead' if ours >= best[1] else 'Chasing')
                posl = [int(r['first_position']) for r in ps if yn(r['brand_mentioned']) and str(r.get('first_position', '')).isdigit()]
                entry['platforms'][PLAT[p]] = {
                    'status': status, 'mentioned': f'{ours}/{len(ps)}', 'avg_position': round(sum(posl) / len(posl), 1) if posl else None,
                    'shown_instead': [b for b, _ in others.most_common(3)],
                    'our_site_cited': sum(yn(r.get('our_domain_cited')) for r in ps),
                    'cited_domains': [d for d, _ in Counter(d for r in ps for d in split(r.get('cited_domains'))).most_common(5)]}
            st = [v['status'] for v in entry['platforms'].values()]
            entry['overall'] = 'Absent' if st and all(s == 'Absent' for s in st) else ('Lead' if st and all(s == 'Lead' for s in st) else 'Mixed')
            block['prompts'].append(entry)
        res[label] = block

    cited = Counter(d for r in rows if r.get('status', 'ok') == 'ok' for d in split(r.get('cited_domains')))
    res['top_cited_domains'] = cited.most_common(15)
    json.dump(res, open(out + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = [f'# AI Visibility — {brand}', f'ข้อมูล: {len(rows)} คำตอบ · รอบ: {", ".join(res["run_dates"])}' +
         (f' · ไม่นับ (error/ไม่มีคำตอบ): {dict(errors)}' if errors else ''), '']
    for label, name in (('non_branded', 'Non-branded — AI เลือกเราไหม'), ('branded', 'Branded — AI พูดถึงเราอย่างไร')):
        b = res[label]
        if not b['answers']:
            continue
        L += [f'## {name}', f'Mention rate รวม: **{b["mention_rate"]}%** ({b["answers"]} คำตอบ)', '',
              '| แพลตฟอร์ม | Mention rate | SoV (ถ่วงตำแหน่ง) ของเรา | ผู้นำ SoV |', '|---|---|---|---|']
        for p, v in b['by_platform'].items():
            s = b['sov'].get(p, {})
            lead = next(iter(s.items()), ('-', 0))
            L.append(f'| {p} | {v["mention_rate"]}% | {s.get(brand, 0)}% | {lead[0]} {lead[1]}% |')
        L += ['', '| หัวข้อ | Mention rate |', '|---|---|'] + [f'| {t} | {v["mention_rate"]}% |' for t, v in b['by_topic'].items()]
        L += ['', '| Prompt | ' + ' | '.join(PLAT[p] for p in ORDER) + ' | ใครถูกแสดงแทน |', '|---|' + '---|' * (len(ORDER) + 1)]
        for e in b['prompts']:
            cells = [f'{e["platforms"][PLAT[p]]["status"]} {e["platforms"][PLAT[p]]["mentioned"]}' if PLAT[p] in e['platforms'] else '-' for p in ORDER]
            inst = sorted({x for v in e['platforms'].values() for x in v['shown_instead']})
            L.append(f'| {e["prompt"]} | ' + ' | '.join(cells) + f' | {", ".join(inst[:4])} |')
        L.append('')
    L += ['## เว็บที่ AI อ้างบ่อย', '| โดเมน | ครั้ง |', '|---|---|'] + [f'| {d} | {c} |' for d, c in res['top_cited_domains']]
    open(out + '.md', 'w', encoding='utf-8').write('\n'.join(L))
    print(f'saved {out}.json + {out}.md')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    kw = {}
    if '--brand' in a:
        i = a.index('--brand'); kw['brand'] = a[i + 1]; del a[i:i + 2]
    if '--out' in a:
        i = a.index('--out'); kw['out'] = a[i + 1]; del a[i:i + 2]
    main(a[0], **kw)
