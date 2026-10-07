# Changelog — AI Search Kit

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
