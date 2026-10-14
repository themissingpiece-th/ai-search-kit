# Changelog — AI Search Kit

## 0.3.6 — 2026-10-14
เช็กกับเนื้อหาคอร์สฉบับสุดท้าย (สไลด์ M0–M6) และให้ kit มีเฉพาะสิ่งที่สอนในคลาส (Ice 14 ต.ค.)
- ลบ skill ที่ไม่อยู่ในชุด (`action-plan-30d` · `ai-search-manager` · `build-prompt-tracker` · `build-site-checker`) และป้าย "(กำลังมา)" ออกทุกจุด — README · marketplace · kit-guide · ai-visibility-check · action-playbook · ขั้นถัดไปชี้ไปลูปจริง (Mention Lab วัดซ้ำ จ./พฤ. → `/ai-visibility-check`) และแผน 30 วันของ Module 6
- `ai-visibility-check` (analyze.py): **Share of Voice = ชื่อเรา ÷ ชื่อทุกแบรนด์ในคำตอบ** (นับแบรนด์ละ 1 ครั้งต่อคำตอบ) ตามนิยามในคลาส แทนสูตรถ่วงตำแหน่ง · Mention Rate บอก **n และ ±** (95%) ทุกตาราง · SoV รวมและรายหัวข้อพร้อมช่วง <5% แทบไม่มีเสียง · 5–10% อยู่ในวง · 10–20% กลุ่มนำ · 20%+ เจ้าที่ (M3)
- `site-readiness-audit`: ชั้นแรกชื่อ **Discover** (เดิม Access) ให้ตรง M4 และ AI Discover Check · A5 ได้ 403 ในชื่อ Googlebot = ต้องเช็กซ้ำใน GSC URL Inspection ก่อนสรุป · llms.txt = info (Google ไม่ได้ใช้ใน Search)
- `ai-citable-page-check` · `ai-content-writer` · `kit-guide`: หลังเผยแพร่ → **Request Indexing ใน Google Search Console** (URL Inspection) ตาม M5 · kit-guide มีแผน 30 วันรายสัปดาห์ตาม M6
- kit-images/post/: เพิ่ม `skill-map-30d-ci-6skills.png` (แผนที่ 6 skill · ไฟล์เดิมยังอยู่)
- tests: เพิ่มเทสต์ SoV ตามนิยามคลาส + n/±

## 0.3.5 — 2026-10-13
- `prompt-finder`: ชุดคลาสเปลี่ยนเป็น **10 ข้อ = 5 หัวข้อ × 2 (ในนั้นมีชื่อแบรนด์ 2–3 ข้อ)** แทน 2–3 หัวข้อ · non-branded 7 + branded 3 — ให้ตรงกับสไลด์ Workshop 1 · make_outputs.py เตือนเมื่อหัวข้อไม่ใช่ 5 × 2 หรือ branded ไม่ใช่ 2–3 · ใช้งานจริงแนะนำหัวข้อละ 10–20 prompt (Ice OK 13 ต.ค.)
- `kit-guide`: คำอธิบาย /prompt-finder ตามกติกาใหม่

## 0.3.4 — 2026-10-11
แก้บั๊กจากการรันเคส BYD ก่อนคลาส 18 ต.ค. (ลำดับขั้นและลูป 30 วันเหมือนเดิม · Ice OK 11 ต.ค.)
- `ai-visibility-check` (analyze.py): จับคู่ผลกับ prompt ด้วยรหัส P01–P10 · เทียบข้อความแบบ NFC + ตัดช่องว่างเกิน (ไม่ใช้ NFKC) · ถ้อยคำไม่ตรงชุดเดิม → เตือนบนหัวรายงาน (จับคู่ได้เมื่อตรงกัน ≥90%) · ตรวจป้าย branded กับชื่อแบรนด์/ชื่อเรียกอื่นในข้อความ ข้อที่ขัดกันยังไม่นับในสถิติจนกว่าจะยืนยัน · ไม่มีคอลัมน์ branded → คิดจากข้อความและแจ้ง · ไม่มี Brand Brain → เตือนว่าข้อมูล branded ต้องตรวจ · ตัวเลือกใหม่ `--aliases` `--prompts` `--brain`
- `prompt-finder` (make_outputs.py): ใส่รหัส P01–P10 ใน Excel และ CSV (คอลัมน์ `prompt_id` ต่อท้าย — Mention Lab ข้ามคอลัมน์ที่ไม่รู้จัก) · `source=ai` ได้ demand = 1 เสมอ · คะแนนที่ใส่มาไม่ตรงกับที่คำนวณ → เตือน · คะแนนเท่ากันเรียงตามที่มา ลูกค้า > GSC > keyword > ผู้ใช้ให้มา > AI · ติดธงเมื่อเลือกข้อ AI แทนข้อลูกค้าในหัวข้อ/ขั้นเดียวกัน
- `brand-brain`: ถามทีละเอกสารก่อนรวม (เผยแพร่ได้ / ภายใน / ห้ามเผยแพร่) · ป้ายที่มา + สถานะต่อบรรทัด · ข้อมูลภายในแยกไฟล์ `-internal` ไม่แนบตอนสั่งเขียน
- `ai-content-writer` · `ai-citable-page-check`: ขั้นแรกอัปเดต Brand Brain เมื่อมีข้อมูลทางการใหม่กว่า (ป้าย ผู้ยืนยัน วันที่) · ใช้เฉพาะข้อมูลเผยแพร่ได้ · citable-check ตรวจว่าตัวเลขในหน้าคำนวณลงตัว (ราคา − ส่วนลด = ราคาสุทธิ) ในข้อ 10
- skill ที่ยังไม่มา (`action-plan-30d` · `ai-search-manager` · `build-prompt-tracker` · `build-site-checker`) ติดป้าย "(กำลังมา)" ทุกจุด พร้อมวิธีทำมือ
- ทุก skill ปิดท้ายด้วยคำสั่งถัดไปที่เติมชื่อไฟล์ให้แล้ว (คำสั่งรูปสั้น `/ชื่อ-skill` เหมือนเดิม)
- เพิ่ม tests/ (`python3 -m pytest tests/` หรือ `python3 tests/run.py`)

## 0.3.3 — 2026-10-07
- `kit-guide`: คู่มือหลังเรียนอัปเดตตาม Mention Lab เวอร์ชันวันเรียน — ตารางเก็บข้อมูลอัตโนมัติ จ./พฤ. 09:00 (baseline + 9 รอบ ถึง 16 พ.ย.), งบ $3/บัญชี, ชื่อปุ่มใหม่ (เริ่มวัดผลวันเรียน · วัดใหม่ทั้งชุด · แก้คำถาม · ตรวจเว็บ) · skill อื่นไม่เปลี่ยน (Ice OK v0.3.3 7 ต.ค.)

## 0.3.2 — 2026-10-07
- `prompt-finder`: เพิ่ม **โหมดให้คะแนน** — วาง prompt ที่มีอยู่แล้ว → คะแนน 5 ด้านรายข้อ · เก็บ/ตัด · ติดธงข้อที่วัดเพี้ยน + เสนอถ้อยคำใหม่ · Excel + CSV เหมือนเดิม (`source=user`) — โดยห้อง Training (Ice OK 7 ต.ค.)
- README: วิธีติดตั้งใน Cowork ด้วยไฟล์ `dist/ai-search-kit.plugin` (แนบในแชต → Save plugin) · marketplace = Claude Code เท่านั้น
- kit-images/pre-cowork/: ภาพขั้นตอนติดตั้งใน Cowork 6 รูป
## 0.3.1 — 2026-10-07
- ลบ `< >` ออกจาก description ของ `brand-brain` (Cowork plugin validation ไม่รับ XML tag)
## 0.3.0 — 2026-10-07
- เพิ่ม `kit-guide` (`/kit-guide` ถามว่าอยากทำอะไร แล้วชี้ skill + สิ่งที่ต้องเตรียม + ประโยคสั่ง)
- description ทุก skill ขึ้นต้น "ใช้เมื่อ…"
## 0.2.0 — 2026-10-07
- เผยแพร่ครั้งแรก: prompt-finder · ai-visibility-check · site-readiness-audit · brand-brain · ai-content-writer · ai-citable-page-check
