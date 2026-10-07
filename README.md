# AI Search Kit (The Missing Piece)

ชุด skill ภาษาไทยสำหรับ Claude Cowork / Claude Code ช่วยทำ SEO & AI Search โดยไม่ต้องซื้อ tool เพิ่ม
แจกในคอร์ส "Building Your AI Search Strategy (SEO, AEO & GEO)"

## ติดตั้ง (Claude Desktop / Cowork)
1. คลิกอีเมลของคุณมุมซ้ายล่าง → **Settings** → Customize → **Plugins**
2. มุมขวาบน **+ Add ▾** → **Add marketplace** → **Add from a repository**
3. ช่อง URL พิมพ์ `themissingpiece-th/ai-search-kit` → **Sync**
4. "AI Search Kit" จะขึ้นในแท็บ Yours → **Install** → เปิด "Sync automatically" เพื่อรับเวอร์ชันใหม่
5. **Settings → Capabilities** → เปิด *Cloud code execution and file creation* + *Allow network egress* → Domain allowlist = **All domains** (skill ที่ตรวจเว็บต้องอ่านหน้าเว็บจริง)
6. ใช้งาน: เปิดแชตใหม่ พิมพ์ `/` แล้วเลือก skill (เช่น `/prompt-finder`) หรือพิมพ์สั่งงานภาษาไทยธรรมดา · ไม่แน่ใจว่าใช้ตัวไหน → `/kit-guide`

ทางเลือก: ดาวน์โหลด zip ใน `dist/` แล้วใช้ **+ Add ▾ → Upload plugin**

## Skill ในชุด
| Skill | ทำอะไร | สถานะ |
|---|---|---|
| `kit-guide` | ไม่แน่ใจว่าใช้ตัวไหน → พิมพ์ `/kit-guide` ถามว่าอยากทำอะไร แล้วชี้ skill ที่ถูก + สิ่งที่ต้องเตรียม + ประโยคสั่ง | ✅ v0.1 |
| `prompt-finder` | เลือก prompt ที่ควร track ด้วย Prompt Map 5 ขั้น → Prompt Set 10 ข้อ (Excel + CSV นำเข้าระบบวัดผล) | ✅ v0.2 |
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
