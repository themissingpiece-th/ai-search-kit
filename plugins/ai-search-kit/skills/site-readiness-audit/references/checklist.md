# เกณฑ์ตรวจความพร้อมเว็บ (Access → Understand → Trust)

ใช้แปลผล `audit.json` · แต่ละข้อมี: ฟิลด์ที่ดู → เกณฑ์ → ทำไมสำคัญ
หลักคิดจาก *AI SEO For Dummies* บทที่ 2, 10, 11, 22 (สรุปเอง) + เอกสารทางการ Google / OpenAI

## ชั้น 1 — Access (bot เข้ามาอ่านได้ไหม)
| ข้อ | ฟิลด์ | ✅ ผ่าน | ❌ / ⚠️ | ทำไมสำคัญ |
|---|---|---|---|---|
| A1 Status | `pages[].status` | 200 | ❌ 4xx/5xx · ⚠️ ข้อความน้อยมากแต่ตอบ 200 (อาจ soft 404) | หน้าที่ตอบผิดไม่ถูก index และไม่ถูกหยิบไปตอบ |
| A2 Redirect | `redirect_chain` | 0–1 ทอด | ⚠️ ≥2 ทอด · ❌ วน | redirect หลายทอดเสียเวลา bot และเสี่ยงหลุด |
| A3 HTTPS | `https` | true | ❌ false | มาตรฐานพื้นฐาน |
| A4 robots.txt ราย bot | `robots.per_bot[*].allowed` | bot ฝั่ง search อนุญาต | ❌ Googlebot / Bingbot / OAI-SearchBot ถูกบล็อกหน้าสำคัญ · ⚠️ GPTBot / Google-Extended / ClaudeBot ถูกบล็อก = เจ้าของเลือกได้ (training) อธิบายผล | Googlebot = Search + AI Overviews/AI Mode · OAI-SearchBot = ChatGPT search · GPTBot = training · Google-Extended = ใช้ข้อมูลกับ Gemini/AI อื่นของ Google ไม่กระทบอันดับ Search · บล็อกตัว search = หายจากคำตอบ AI นั้น |
| A5 Firewall / CDN | `ua_test`, `ua_blocked` | ทุก bot ได้ 200 เหมือน browser | ❌ bot ได้ 403/429/503 ขณะ browser ได้ 200 | robots.txt อนุญาตแต่ firewall บล็อก = bot เข้าไม่ได้จริง (ทดสอบแบบจำลอง UA) |
| A6 noindex / nosnippet | `meta_robots`, `x_robots_tag` | ไม่มี noindex/nosnippet · max-snippet:-1 หรือไม่ระบุ | ❌ noindex บนหน้าสำคัญ · ⚠️ nosnippet / max-snippet ต่ำ | noindex = ไม่ขึ้นทั้ง Search และ AI · nosnippet = Google ใช้เนื้อหาใน AI Overviews ไม่ได้ |
| A7 Canonical | `canonical`, `canonical_is_self` | ชี้ตัวเอง (หรือชี้หน้าหลักที่ตั้งใจ) | ⚠️ ไม่มี · ❌ ชี้ไปหน้าอื่นโดยไม่ตั้งใจ | บอก Google ว่าหน้าไหนคือหน้าหลัก |
| A8 Sitemap | `sitemaps[]` | 200 และมี `<loc>` · ประกาศใน robots.txt | ⚠️ ไม่ประกาศใน robots · ❌ 404 | ช่วยให้ค้นพบหน้าได้ครบ — ส่งใน GSC + Bing Webmaster Tools ด้วย |
| A9 เนื้อหาใน HTML | `visible_text_chars`, `likely_js_dependent`, `text_sample` | มีข้อความหลักใน HTML ดิบ | ❌ ข้อความน้อยมาก + script เยอะ = อาจต้องรอ JavaScript | bot บางตัวไม่รัน JavaScript เห็นแต่ HTML ดิบ |
| A10 ความเร็ว | `pagespeed` | ผ่าน Core Web Vitals | ⚠️ ต่ำกว่าเกณฑ์ · ❔ ไม่มี key | ประสบการณ์ผู้ใช้ + เป็นสัญญาณหนึ่งของ Google |
| info llms.txt | `llms_txt.status` | — | — | รายงานว่ามี/ไม่มีเท่านั้น: "ทดลองได้ ยังไม่มีหลักฐาน" ไม่นับเป็นปัญหา |

## ชั้น 2 — Understand (อ่านแล้วเข้าใจไหม)
| ข้อ | ฟิลด์ | ✅ | ⚠️ / ❌ | ทำไมสำคัญ |
|---|---|---|---|---|
| U1 Title | `title`, `title_len` | บอกชัดว่าหน้าเกี่ยวกับอะไร ~30–65 ตัวอักษร | ⚠️ ซ้ำหน้าแรก / ยาวมาก · ❌ ไม่มี | ประโยคแรกที่ทั้งคนและ AI เห็น |
| U2 Meta description | `meta_description` | มี และสรุปคำตอบ | ⚠️ ไม่มี | ใช้เป็น snippet |
| U3 H1 + โครงหัวข้อ | `h1_count`, `h1`, `h2` | H1 1 อัน บอกหัวข้อ · H2 เป็นลำดับ/เป็นคำถามจริง | ⚠️ H1 เป็นสโลแกน ไม่บอกหัวข้อ · หลาย H1 · ไม่มี H2 | ช่วยให้ระบบเข้าใจโครงเนื้อหา (H1 เดียว = แนวทางของหนังสือ ไม่ใช่กฎ Google) |
| U4 ตาราง / ลิสต์ | `tables`, `lists` | หน้าเปรียบเทียบ/ราคา มีตาราง HTML | ⚠️ ข้อมูลเปรียบเทียบอยู่ในรูปหรือย่อหน้ายาว | ตารางเป็นรูปแบบที่ AI หยิบไปสรุปง่าย |
| U5 Alt รูป | `images_missing_alt` | 0 หรือเกือบ 0 | ⚠️ ขาดหลายรูป | AI และคนตาบอดเข้าใจภาพจาก alt |
| U6 Structured data | `jsonld_types`, `jsonld_parse_errors` | มี Organization (หน้าแรก) + ชนิดที่ตรงหน้า (Product/Service/Article/BreadcrumbList/FAQPage) | ⚠️ ไม่มีเลย · ❌ JSON-LD parse error | factor ที่ช่วยเพิ่มโอกาส ไม่ใช่การันตี · ต้องตรงกับที่มองเห็น · ตรวจด้วย Rich Results Test |
| U7 ภาษา | `html_lang`, `hreflang` | lang ตรงภาษา · มี hreflang ถ้ามีหลายภาษา | ⚠️ ไม่มี lang | |
| U8 วันที่อัปเดต | `date_modified_hint` | มี | ⚠️ ไม่พบ | ความสด = หนึ่งในสัญญาณที่ AI ใช้ (บทที่ 1) |

## ชั้น 3 — Trust (น่าเชื่อถือพอให้ AI กล้าใช้ไหม)
สคริปต์เห็นได้แค่บางส่วน — ส่วนที่เหลือให้ Claude ดูจากเนื้อหาหน้า หรือทำเครื่องหมาย ❔
| ข้อ | ฟิลด์ | ✅ | ⚠️ |
|---|---|---|---|
| T1 About / Contact | `links_about`, `links_contact` | มีลิงก์ | ไม่พบ |
| T2 ราคา / ค่าธรรมเนียม / เงื่อนไข | `text_sample` + อ่านหน้า | เขียนชัดบนหน้า | ไม่มี → เว็บอื่นจะพูดแทน และ AI จะทวนข้อมูลนั้น (บทที่ 12) |
| T3 ตัวตนองค์กร | `jsonld_types` มี Organization | มี + sameAs | ไม่มี |
| T4 ผู้เขียน / ผู้เชี่ยวชาญ / รีวิว | อ่านหน้า | มี | ❔ ถ้าตรวจไม่ได้ |

## จัดลำดับ Top 3 (หลักคิดจากหนังสือ บทที่ 10–11)
ให้คะแนนแต่ละปัญหา 1–5 สี่ด้าน: **ความรุนแรง · ขอบเขต (กี่หน้า/ทั้งเว็บ) · ผลต่อรายได้ (หน้าสำคัญไหม) · ความเร็วที่แก้ได้** → รวมคะแนน → เลือก 3 อันดับแรก
**กฎเหนือคะแนน:** ปัญหาที่ทำให้หน้าสำคัญ "ไม่มีสิทธิ์ถูกใช้" (noindex, บล็อก bot ฝั่ง search, firewall บล็อก, หน้าไม่ตอบ 200, เนื้อหาไม่อยู่ใน HTML) ขึ้นอันดับ 1 เสมอ
ปัญหาเดียวกันหลายหน้าที่แก้จุดเดียว (template / plugin / ตั้งค่า CDN) = นับเป็น 1 งาน

## ต้องเช็คเองหลังรายงาน
- Google Search Console → URL Inspection (หน้า index แล้วไหม Google เห็นหน้าเหมือนเราไหม) + รายงาน Pages
- Rich Results Test (schema ใช้ได้ไหม) · PageSpeed Insights (ถ้าไม่ได้ใส่ key) · Bing Webmaster Tools
