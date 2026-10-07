---
name: site-readiness-audit
description: ใช้เมื่ออยากรู้ว่าเว็บพร้อมให้ AI เข้าถึง-เข้าใจ-เชื่อถือไหม ("ตรวจเว็บ", "robots.txt บล็อก AI ไหม", "AI readiness", "website audit") หรือมีรายงาน AI Discover Check จาก Mention Lab ให้แปลเป็นงาน — ตรวจ 3 ชั้น Access → Understand → Trust (Google AI Overviews / AI Mode, ChatGPT, Gemini, Perplexity) แล้วสรุป Top 3 สิ่งที่ต้องแก้ก่อน + ข้อความส่งทีมเว็บ
---

# Site Readiness Audit (ตรวจความพร้อมเว็บสำหรับ SEO & AI Search)

ตรวจเว็บของผู้ใช้ 1–4 หน้า แล้วออกรายงานภาษาไทยที่คนไม่ใช่ dev อ่านรู้เรื่อง: ผ่าน / มีปัญหา / ตรวจไม่ได้ + Top 3 สิ่งที่ต้องแก้ + สิ่งที่ต้องเช็คเองใน Google Search Console

## 1. ขอข้อมูล (ถามเฉพาะที่ขาด)
- URL หน้าแรก + หน้าสำคัญ 1–3 หน้า (หน้าสินค้า/บริการ/หน้าที่อยากให้ AI หยิบไปตอบ) — โดเมนเดียวกัน
- (ไม่บังคับ) ธุรกิจทำอะไร / หน้าไหนสำคัญต่อยอดขายที่สุด — ใช้จัดลำดับความสำคัญ

## 2. รันสคริปต์ (โหมดเต็ม)
```bash
python3 scripts/audit.py <URL1> <URL2> ... --out audit.json
```
- ใช้ไลบรารีมาตรฐานของ Python เท่านั้น ไม่ต้องติดตั้งอะไร
- ถ้าผู้ใช้มี PageSpeed Insights API key ให้เพิ่ม `--psi-key KEY` (ไม่มีก็ข้าม แล้วแนะนำให้เปิด pagespeed.web.dev เอง)
- สคริปต์ตรวจ: robots.txt ราย bot, sitemap, llms.txt, status/redirect, X-Robots-Tag, meta robots (noindex/nosnippet/max-snippet), canonical, hreflang, title/meta, H1/H2, ข้อความใน HTML ดิบ, ตาราง/ลิสต์, alt รูป, JSON-LD schema, ลิงก์ About/Contact และ **ทดสอบ user-agent ของ bot หลัก** ว่าโดน firewall/CDN บล็อกไหม

## 3. ถ้ารันไม่ได้ → โหมดสำรอง
ถ้า `network_blocked: true` หรือ error ประมาณ "Tunnel connection failed: 403" / "proxy":
1. บอกผู้ใช้ตรงๆ ว่า sandbox ออกอินเทอร์เน็ตไม่ได้ และวิธีเปิด: **Settings → Capabilities → Code execution → network egress = All domains** (บัญชี Team/Enterprise ต้องให้แอดมินเปิด) แล้วรันใหม่
2. ระหว่างนั้นตรวจเท่าที่ทำได้ด้วยเครื่องมืออ่านเว็บของ Claude (web fetch): `/robots.txt`, `/sitemap.xml`, `/llms.txt`, เนื้อหาหน้า (หัวข้อ, คำตอบต้นหน้า, ตาราง, ข้อมูลราคา/เงื่อนไข)
3. ข้อที่ตรวจไม่ได้ในโหมดนี้ ให้ใส่ ❔ "ตรวจไม่ได้ในโหมดสำรอง": status code, redirect, header, meta robots, canonical, schema, การบล็อก bot ราย user-agent — **ห้ามเดาผล**

## 4. แปลผลเป็นรายงาน
อ่าน `references/checklist.md` (เกณฑ์ทุกข้อ + วิธีให้คะแนนลำดับการแก้) แล้วเขียนรายงานตามโครงนี้ และบันทึกเป็นไฟล์ `site-readiness-report-<โดเมน>.md` ให้ผู้ใช้ดาวน์โหลด:

1. **สรุป 3 บรรทัด** — ภาพรวม Access / Understand / Trust อย่างละ 1 บรรทัด
2. **Top 3 สิ่งที่ต้องแก้ก่อน** — แต่ละข้อ: ปัญหา · กระทบอะไร (Google / AI ตัวไหน) · แก้ที่ไหน · ส่งต่อให้ใคร (marketing / dev / agency)
3. **ตารางผลตรวจ** แยก 3 ชั้น: ข้อ · ผล (✅ ผ่าน / ⚠️ ควรปรับ / ❌ มีปัญหา / ❔ ตรวจไม่ได้) · หลักฐานที่เจอ (ค่าจริงจากสคริปต์) · ทำไมสำคัญ
4. **ต้องเช็คเอง** (สคริปต์มองไม่เห็น): GSC URL Inspection + รายงาน Pages, Rich Results Test, PageSpeed Insights, Bing Webmaster Tools
5. **ข้อจำกัดของการตรวจนี้** — ตรวจเฉพาะหน้าที่ระบุ ไม่ใช่ทั้งเว็บ · การทดสอบ user-agent เป็นการจำลอง (bot จริงยืนยันด้วย IP) · การเข้าถึงได้ ≠ ถูก index แล้ว

## กติกา
- เขียนภาษาไทย ศัพท์เทคนิคใช้อังกฤษ + ไทยในวงเล็บครั้งแรก เช่น "canonical (หน้าหลักที่ต้องการให้ index)"
- รายงานแต่ข้อที่มีหลักฐานจากผลตรวจ — ถ้าไม่มีข้อมูล เขียน ❔ ไม่สรุปเอง
- llms.txt, Web API, Wikidata = "ทดลองได้ ยังไม่มีหลักฐานว่าช่วย" ไม่นับเป็นปัญหา
- Schema / FAQ = "factor ที่ช่วยเพิ่มโอกาส ไม่ใช่การันตี" (Google ไม่มี schema พิเศษสำหรับ AI)
- ไม่แนะนำให้บล็อก/เปิด bot แทนเจ้าของเว็บ — อธิบายผลของแต่ละทางให้เขาตัดสินใจ
- อ้างอิงแนวคิด: Nathan Gotch, *AI SEO For Dummies* (Wiley 2026) บทที่ 2, 10, 11, 22 · Google Search Central (AI features) · เอกสาร crawler ของ OpenAI — สรุปด้วยคำของเรา ไม่คัดลอกข้อความจากหนังสือ
