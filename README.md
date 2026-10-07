# AI Search Kit (The Missing Piece)

ชุด skill ภาษาไทยสำหรับ Claude Cowork / Claude Code ช่วยทำ SEO & AI Search โดยไม่ต้องซื้อ tool เพิ่ม
แจกในคอร์ส "Building Your AI Search Strategy (SEO, AEO & GEO)"

## ติดตั้งใน Claude Cowork (แท็บ Home) — ทางหลักสำหรับผู้เรียน
1. ดาวน์โหลดไฟล์จาก **themissingpiece.co.th/ai-search-kit** (= `dist/ai-search-kit.plugin` เวอร์ชันล่าสุด)
2. Claude Desktop → Home → Cowork → แชตใหม่ → **+ → Add files or photos** → เลือกไฟล์
3. พิมพ์: "ติดตั้ง" → ถ้าถาม Running command กด Allow once
4. กดปุ่ม **Save plugin** บนการ์ดที่ Claude ส่งกลับ → "Plugin changes applied"
5. **Settings → Capabilities** → เปิด *Cloud code execution and file creation* + *Allow network egress* → Domain allowlist = **All domains** (skill ที่ตรวจเว็บต้องอ่านหน้าเว็บจริง)
6. ใช้งาน: แชตใหม่ พิมพ์ `/prompt-finder` (หรือ `/` แล้วเลือก) · ไม่แน่ใจว่าใช้ตัวไหน → `/kit-guide`
อัปเดตเวอร์ชัน: ดาวน์โหลดไฟล์ใหม่แล้วทำข้อ 2–4 ซ้ำ (ระบบจะถาม Replace)

## ติดตั้งใน Claude Code (แท็บ Code) — ทางเลือก
Settings → Plugins → **+ Add → Add marketplace → Add from a repository** → `themissingpiece-th/ai-search-kit` → Sync → Add · (Cowork ไม่เห็น plugin ที่ติดตั้งทางนี้)

## Skill ในชุด
| Skill | ทำอะไร | สถานะ |
|---|---|---|
| `kit-guide` | ไม่แน่ใจว่าใช้ตัวไหน → พิมพ์ `/kit-guide` ถามว่าอยากทำอะไร แล้วชี้ skill ที่ถูก + สิ่งที่ต้องเตรียม + ประโยคสั่ง | ✅ v0.1 |
| `prompt-finder` | เลือก prompt ที่ควร track ด้วย Prompt Map 5 ขั้น → Prompt Set 10 ข้อ (Excel + CSV นำเข้าระบบวัดผล) · มี prompt อยู่แล้ว? วางมาให้คะแนน 5 ด้าน + ติดธงข้อที่วัดเพี้ยน | ✅ v0.3 |
| `ai-visibility-check` | อ่านผลวัด บอกว่าแบรนด์ไม่ถูกแสดงในคำถามไหน ใครถูกแสดงแทน และควรทำอะไร ทำอย่างไร | ✅ v0.1 |
| `site-readiness-audit` | ตรวจความพร้อมเว็บ AI Discover / Understand / Trust → Top 3 fixes + ข้อความส่งทีมเว็บ | ✅ v0.1 |
| `brand-brain` | ให้ AI เรียนรู้แบรนด์และสินค้า (จากข้อมูลที่ให้ + ศึกษาจากเว็บเอง) แล้วจำไว้เป็นไฟล์ Brand Brain | ✅ v0.1 |
| `ai-content-writer` | เขียน content จาก Brand Brain ให้ตอบ prompt ที่แพ้ และต่อยอดจุดที่ยังพัฒนาได้ | ✅ v0.1 |
| `ai-citable-page-check` | ตรวจ content ก่อนเผยแพร่ว่า AI หยิบไปตอบได้ไหม + ข้อมูลถูกต้องไหม | ✅ v0.1 |
| `action-plan-30d` | แผน 30 วันจากผลวัดและผลตรวจเว็บ | กำลังทำ |
| `ai-search-manager` | ผู้ช่วยตัวหลักที่แบ่งงานให้ agent 5 ตัว | กำลังทำ |

## หมายเหตุ
หลักคิดอ้างอิง Nathan Gotch, *AI SEO For Dummies* (Wiley 2026) เป็นรายบท และเอกสารทางการของ Google / OpenAI — เนื้อหาใน skill เขียนสรุปด้วยคำของเราเอง ไม่มีข้อความจากหนังสือ
ผลตรวจเป็นหลักฐาน ณ เวลานั้น ไม่รับประกันอันดับหรือการถูกเอ่ยชื่อใน AI
