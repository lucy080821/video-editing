import json, sys, datetime
sc = json.load(open('doc_script.json', encoding='utf-8'))
tl = json.load(open('out/timeline.json'))
chapters = open('out/chapters.txt', encoding='utf-8').read().strip()
srt = open('out/subtitles.srt', encoding='utf-8').read()
preview_id, thumb_id, dur_full, size_mb = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
KW = 'học từ vựng tiếng anh qua bài đọc'

# markdown script by chapter
md, cur = [], '## Mở đầu'
md.append(cur)
for s in sc['scenes']:
    if s['t'] == 'chapter':
        md.append(''); md.append('## ' + s['title'].replace('“', '').replace('”', ''))
    md.append(''); md.append(s['vo'])
script = '\n'.join(md)

sources = [
 ("Waring & Takaki (2003), At what rate do learners learn and retain new vocabulary from reading a graded reader?, Reading in a Foreign Language 15(2)", "https://nflrc.hawaii.edu/rfl/item/78"),
 ("Webb (2007), The effects of repetition on vocabulary knowledge, Applied Linguistics 28(1), 46–65", "https://eric.ed.gov/?id=EJ757328"),
 ("Pellicer-Sánchez & Schmitt (2010), Incidental vocabulary acquisition from an authentic novel: Do Things Fall Apart?, Reading in a Foreign Language 22(1), 31–55", "https://nflrc.hawaii.edu/rfl/item/207"),
 ("Uchihara, Webb & Yanagisawa (2019), The effects of repetition on incidental vocabulary learning: A meta-analysis of correlational studies, Language Learning 69(3)", "https://doi.org/10.1111/lang.12343"),
 ("Hu & Nation (2000), Unknown vocabulary density and reading comprehension, Reading in a Foreign Language 13(1)", "https://scholarspace.manoa.hawaii.edu/items/dfe724c0-c66f-4afe-9164-d6c6a59585d4"),
 ("Laufer & Ravenhorst-Kalovski (2010), Lexical threshold revisited, Reading in a Foreign Language 22(1), 15–30", "https://scholarspace.manoa.hawaii.edu/items/eaead47e-853e-4797-ba6f-596df150c1d7"),
 ("Kremmel, Indrarathne, Kormos & Suzuki (2023), Unknown vocabulary density and reading comprehension: Replicating Hu and Nation (2000), Language Learning", "https://eprints.lancs.ac.uk/id/eprint/210922"),
 ("Extensive Reading Foundation, Guide to Extensive Reading", "https://erfoundation.org/wordpress/wp-content/uploads/2024/03/ERF_Guide_English_2023.pdf"),
 ("Nation & Waring (2013), Extensive Reading and Graded Readers", "https://erfoundation.org/wordpress/wp-content/uploads/2026/05/CM_ER_Booklet_eng.pdf"),
 ("Mondria (2003), The effects of inferring, verifying, and memorizing on the retention of L2 word meanings, Studies in Second Language Acquisition 25(4)", "https://doi.org/10.1017/S0272263103000202"),
 ("Karpicke & Roediger (2008), The critical importance of retrieval for learning, Science 319", "https://doi.org/10.1126/science.1152408"),
 ("Murre & Dros (2015), Replication and analysis of Ebbinghaus' forgetting curve, PLOS ONE 10(7): e0120644", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120644"),
]
def paras(*sentences):
    return '\n\n'.join(sentences)
src_lines = '\n'.join(f'- {t}: {u}' for t, u in sources)
desc = paras(
 "Học từ vựng tiếng Anh qua bài đọc có thật sự giúp bạn nhớ lâu không?",
 "Video này tổng hợp các nghiên cứu về học từ vựng qua đọc và giải thích vì sao đọc nhiều mà vẫn quên từ.",
 "Bạn sẽ biết phải gặp một từ bao nhiêu lần mới nhớ, theo Webb (2007), Pellicer-Sánchez & Schmitt (2010) và phân tích gộp của Uchihara và cộng sự (2019).",
 "Bạn cũng sẽ biết vì sao bài đọc nên có khoảng 98% từ đã biết, cách chọn graded readers vừa sức, và cách đọc chủ động để nhớ từ lâu hơn.",
 "Xem đến cuối để nhận phần thưởng: quy trình 5 bước Đọc → Đoán → Kiểm tra → Ghi cụm → Ôn lại, kèm bài tập làm thử có đáp án và lịch luyện 7 ngày, mỗi ngày 15–20 phút.",
 "Mục lục:\n" + chapters,
 "Nguồn tham khảo:\n" + src_lines,
 "Lưu ý: con số 98% là kim chỉ nam, không phải luật cứng.",
 "Số lần gặp từ cần thiết cũng thay đổi theo người học và cách đo.",
 "Đăng ký kênh Tiếng Anh Không Khó để học tiếng Anh mỗi tuần nhé!",
 "📘 Facebook: https://www.facebook.com/tienganhkhongkhovn\n🌐 Website học tiếng Anh Lucy Tutor: https://lucytutor.online\n🎵 TikTok: https://www.tiktok.com/@tienganhkhongkho7",
 "#hoctuvung #tienganh #tienganhkhongkho")
YT_TITLE = "Học từ vựng tiếng Anh qua bài đọc: vì sao đọc nhiều vẫn quên từ?"
tiktok = paras(
 "Học từ vựng tiếng Anh qua bài đọc mà vẫn quên từ?",
 "Đây là lý do!",
 "Nghiên cứu cho thấy phải gặp một từ khoảng 10 lần thì việc nhớ từ mới tăng rõ rệt.",
 "Bài đọc nên có khoảng 98% từ bạn đã biết, tức chừng 1 từ lạ trong 50 từ.",
 "Xem hết video để nhận quy trình 5 bước Đọc → Đoán → Kiểm tra → Ghi cụm → Ôn lại.",
 "Video đầy đủ có trên kênh YouTube Tiếng Anh Không Khó.",
 "#hoctuvung #hoctienganh #tienganh #cachhoctuvungtienganh #gradedreaders #tienganhkhongkho")
facebook = paras(
 "Học từ vựng tiếng Anh qua bài đọc: vì sao đọc nhiều mà vẫn quên từ?",
 "Mình vừa làm một video tổng hợp các nghiên cứu về chuyện này.",
 "Một nghiên cứu cho thấy sau 3 tháng, người học chỉ còn nhớ nghĩa khoảng 1 trong 25 từ mục tiêu gặp trong một cuốn truyện.",
 "Lý do chính là gặp lại từ quá ít lần, và bài đọc thường quá sức.",
 "Trong video, mình chỉ cách chọn bài đọc có khoảng 98% từ đã biết, cách đọc graded readers vừa sức, và quy trình 5 bước Đọc → Đoán → Kiểm tra → Ghi cụm → Ôn lại.",
 "Câu hỏi cho bạn: trong câu “The bread is always warm and fragrant”, từ fragrant nghĩa là gì?",
 "Bình luận đáp án cho mình nha!",
 "Video đầy đủ “Học từ vựng tiếng Anh qua bài đọc” có trên kênh YouTube Tiếng Anh Không Khó.",
 "#hoctuvung #hoctienganh #tienganhkhongkho #gradedreaders")
factCheck = [
 {"claim": "Waring & Takaki (2003): đọc graded reader A Little Princess (400 từ gốc), 25 từ mục tiêu; sau 3 tháng chỉ nhớ nghĩa khoảng 1/25 từ; từ gặp dưới 8 lần không ai còn nhớ nghĩa; cần đọc một lượng rất lớn, không phải lý do để bỏ graded reading", "sources": ["https://eric.ed.gov/?id=EJ676380", "https://nflrc.hawaii.edu/rfl/item/78", "https://files.eric.ed.gov/fulltext/EJ1401553.pdf"]},
 {"claim": "Murre & Dros (2015) lặp lại thành công đường cong quên của Ebbinghaus (1880), kết quả tương tự dữ liệu gốc", "sources": ["https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120644"]},
 {"claim": "Webb (2007): 121 sinh viên Nhật, gặp từ 1/3/7/10 lần, 10 bài kiểm tra cho 5 mặt kiến thức từ; tăng đáng kể ở 10 lần; có thể cần hơn 10 lần để biết đầy đủ", "sources": ["https://eric.ed.gov/?id=EJ757328", "https://www.researchgate.net/publication/31064743_The_Effects_of_Repetition_on_Vocabulary_Knowledge"]},
 {"claim": "Pellicer-Sánchez & Schmitt (2010): tiểu thuyết Things Fall Apart; từ gặp hơn 10 lần: nhận ra nghĩa 84%, nhớ lại nghĩa 55%", "sources": ["https://eric.ed.gov/?id=EJ887875", "https://nflrc.hawaii.edu/rfl/item/207"]},
 {"claim": "Uchihara, Webb & Yanagisawa (2019): 45 hệ số từ 26 nghiên cứu, N = 1.918, r = .34 (mức trung bình); yếu tố điều tiết gồm tuổi, vốn từ, học giãn cách, hình ảnh hỗ trợ, mức tham gia", "sources": ["https://api.semanticscholar.org/graph/v1/paper/DOI:10.1111/lang.12343?fields=title,abstract,year,venue", "https://doi.org/10.1111/lang.12343"]},
 {"claim": "Hu & Nation (2000): cần biết khoảng 98% số từ để hiểu đầy đủ (khoảng 1 từ lạ / 50 từ)", "sources": ["https://eprints.lancs.ac.uk/id/eprint/210922", "https://scholarspace.manoa.hawaii.edu/items/dfe724c0-c66f-4afe-9164-d6c6a59585d4", "https://erfoundation.org/wordpress/wp-content/uploads/2024/03/ERF_Guide_English_2023.pdf"]},
 {"claim": "Laufer & Ravenhorst-Kalovski (2010): 95% (khoảng 4.000–5.000 họ từ) cho hiểu tối thiểu, 98% (khoảng 8.000 họ từ) cho hiểu tốt", "sources": ["https://scholarspace.manoa.hawaii.edu/items/eaead47e-853e-4797-ba6f-596df150c1d7", "https://cris.haifa.ac.il/en/publications/lexical-threshold-revisited-lexical-text-coverage-learners-vocabu/"]},
 {"claim": "Kremmel và cộng sự (2023): lặp lại với 104 người học trưởng thành, không tái lập được hoàn toàn; số liệu gốc dựa trên 66 sinh viên", "sources": ["https://eprints.lancs.ac.uk/id/eprint/210922"]},
 {"claim": "ERF: dưới 90% đọc chậm, nản; 90–98% vùng học; từ 98% trở lên đọc nhanh, thích thú; graded readers kiểm soát từ vựng, 6–8 cấp từ Starter đến Advanced; trường thường yêu cầu khoảng 1 cuốn/tuần", "sources": ["https://erfoundation.org/wordpress/wp-content/uploads/2024/03/ERF_Guide_English_2023.pdf", "https://www.slideshare.net/slideshow/guide-to-extensivereadingweb/25367377"]},
 {"claim": "Nation & Waring (2013): phép thử một trang (không quá 3–4 từ lạ mỗi trang), hai kiểu đọc mở rộng (có vài từ lạ / rất dễ cho trôi chảy, đọc lại sách cũ), người học giỏi nhất là người đọc nhiều nhất", "sources": ["https://erfoundation.org/wordpress/wp-content/uploads/2026/05/CM_ER_Booklet_eng.pdf"]},
 {"claim": "Mondria (2003): phương pháp đoán–kiểm tra–học thuộc cho mức nhớ tương đương phương pháp cho sẵn nghĩa nhưng tốn thời gian hơn; bước học thuộc có hiệu quả lớn nhất", "sources": ["https://api.semanticscholar.org/graph/v1/paper/DOI:10.1017/S0272263103000202?fields=title,abstract,year", "https://doi.org/10.1017/S0272263103000202"]},
 {"claim": "Karpicke & Roediger (2008): 40 cặp từ Swahili–Anh; sau 1 tuần nhóm tự kiểm tra lặp lại nhớ khoảng 80%, các nhóm khác khoảng 35%", "sources": ["https://www.apa.org/monitor/2008/06/testing", "https://www.purdue.edu/uns/x/2008a/080214KarpickeTest.html"]},
 {"claim": "frail /freɪl/ = yếu, dễ tổn thương; fragrant /ˈfreɪɡrənt/ = thơm; drift /drɪft/ = trôi đi nhẹ nhàng", "sources": ["https://www.oxfordlearnersdictionaries.com/definition/english/frail", "https://www.oxfordlearnersdictionaries.com/definition/english/fragrant?q=fragrant", "https://www.oxfordlearnersdictionaries.com/definition/english/drift_1", "https://www.britannica.com/dictionary/fragrant"]},
]
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(timespec='seconds')
doc = {
 "kind": "video", "date": "2026-11-28", "topic": "Học từ vựng tiếng Anh qua bài đọc: vì sao đọc nhiều vẫn không nhớ từ, và cách đọc để thật sự học được từ mới",
 "category": "Phương pháp học / từ vựng", "style": "documentary-vox-motion", "format": "documentary-vox-motion",
 "visual": {"kit": "Documentary (stock Pixabay chỉnh màu ấm, letterbox) + Vox giấy kem (thẻ nghiên cứu có băng dính, con dấu năm, bút dạ quét chữ, gạch chân vẽ tay) + motion graphic nền xanh đêm (đếm số, vòng tròn %, cột, đường cong quên, thang 3 vùng độ khó)",
   "palette": ["#F4ECD8", "#14254A", "#F2B705", "#E4572E", "#1f8a70", "#0d1626"],
   "animations": ["slam từng chữ", "bút dạ quét", "gõ máy chữ", "vẽ nét SVG", "đếm số", "vòng tròn % chạy", "cột mọc", "con dấu năm nghiên cứu", "lật thẻ 3D", "nhân vật leo cầu thang cấp độ", "kính lúp quét trang", "đồng hồ đếm ngược 3-2-1", "pháo giấy"],
   "transitions": ["wipe", "zoom", "whip pan", "trượt lên", "iris tròn (thẻ phần)", "lật 3D"],
   "images": ["sách lật trang trên bãi biển (Pixabay 185096)", "thư viện (Pixabay 846)", "sinh viên đọc sách trong thư viện (Pixabay 122233)", "icon SVG: sách, bình thí nghiệm, bia, não, cân, hộp quà, bóng đèn, kính lúp"],
   "fonts": ["Noto Serif", "Anton", "Be Vietnam Pro", "Montserrat", "Patrick Hand"],
   "music": "ElevenLabs Music: piano ấm + string pad, ~90 BPM, nhạc nâng 0.10→0.30 ở 9 khoảng ngắt"},
 "status": "cho-duyet", "revision": 1, "requestedBy": "anh Tuấn yêu cầu trực tiếp trong phiên chat 26/11/2026 (theo mục kế hoạch đã duyệt 28/11)",
 "keywords": {"primary": KW, "secondary": ["học từ vựng qua bài đọc", "cách học từ vựng tiếng anh nhớ lâu", "graded readers", "học từ vựng qua ngữ cảnh", "cách học từ vựng tiếng anh"]},
 "research": {"candidates": [{"topic": "Học từ vựng tiếng Anh qua bài đọc (kế hoạch 28/11)", "seeds": ["học từ vựng qua bài đọc", "học từ vựng tiếng anh qua bài đọc", "cách học từ vựng tiếng anh nhớ lâu", "graded readers", "cách học từ vựng tiếng anh qua đọc"],
   "googleSuggest": ["học từ vựng qua bài đọc", "học từ vựng tiếng anh qua bài đọc", "cách học từ vựng tiếng anh nhớ lâu", "cách học từ vựng tiếng anh nhanh nhớ lâu", "graded readers là gì", "graded readers b1", "graded readers a2"],
   "youtubeSuggest": ["học từ vựng qua ngữ cảnh", "cách học từ vựng tiếng anh nhớ lâu", "cách học từ vựng tiếng anh nhanh nhớ lâu", "cách học thuộc từ vựng tiếng anh nhớ lâu", "graded readers", "graded readers english", "graded readers a1", "cách học từ vựng tiếng anh"],
   "score": {"demand": 4, "audience": 5, "platform": 4, "fit": 4}}],
  "chosen": "Học từ vựng tiếng Anh qua bài đọc", "why": "Theo kế hoạch anh Tuấn đã duyệt ngày 2026-11-25 (mục 28/11) và yêu cầu trực tiếp ngày 26/11; Google gợi ý nguyên văn 'học từ vựng tiếng anh qua bài đọc', YouTube gợi ý mạnh cụm 'cách học từ vựng tiếng anh nhớ lâu' nên đưa vào title/description làm từ khóa phụ.",
  "competitors": [], "checkedAt": now},
 "factCheck": factCheck,
 "reward": {"promise": "Xem đến cuối để nhận quy trình 5 bước Đọc, Đoán, Kiểm tra, Ghi cụm, Ôn lại, kèm bài tập làm thử có đáp án và lịch luyện 7 ngày.",
   "steps": ["Đọc: bài vừa sức (vài từ lạ mỗi trang), đọc lấy ý chính, không dừng tra", "Đoán: gạch từ lạ quan trọng, đoán nghĩa từ ngữ cảnh", "Kiểm tra: tra từ điển, nghe phát âm", "Ghi cụm: chép cụm + câu gốc, mặt trước câu trống, mặt sau nghĩa", "Ôn lại: che nghĩa, tự nhớ lại sau 1–3–7 ngày, đọc thêm bài cùng chủ đề"],
   "exercise": "Every morning, Minh walks to the bakery near his house. The bread is always warm and fragrant, and the sweet smell drifts down the whole street. Đoán fragrant và drifts. Đáp án: fragrant /ˈfreɪɡrənt/ = thơm ngát; drift /drɪft/ = trôi đi, bay đi nhẹ nhàng; cụm ghi sổ: the smell drifts down the street.",
   "schedule": "15–20 phút/ngày. Ngày 1–2: bài 1 đủ 5 bước; ngày 3: bài 2 cùng chủ đề + ôn cụm cũ; ngày 4: bài 3 + ôn; ngày 5: graded reader thật dễ; ngày 6: ôn cả sổ bằng cách che nghĩa; ngày 7: đọc lại bài 1, đếm cụm còn nhớ.",
   "mistakes": ["Chọn bài quá khó → hạ cấp độ", "Chép quá nhiều từ → 5–8 cụm mỗi bài", "Đọc lại sổ không che nghĩa → tự hỏi trước, xem sau"],
   "progress": ["Gặp lại từ cũ và nhận ra ngay", "Đọc nhanh hơn, ít phải dừng", "Tự dùng được vài cụm khi nói/viết"]},
 "script": script, "srt": srt,
 "seo": {"title": YT_TITLE, "description": desc, "youtube": {"title": YT_TITLE, "description": desc}, "tiktok": {"caption": tiktok, "tip": "Video ngang 12 phút: TikTok cho phép tải video dài; bật phụ đề tự động trước khi đăng."}, "facebook": {"caption": facebook}, "format": "Mỗi câu một đoạn (cách 1 dòng trống) để dễ copy",
   "tags": ["học từ vựng tiếng anh qua bài đọc", "học từ vựng qua bài đọc", "cách học từ vựng tiếng anh nhớ lâu", "cách học từ vựng tiếng anh nhanh nhớ lâu", "cách học từ vựng tiếng anh", "học từ vựng tiếng anh", "học từ vựng qua ngữ cảnh", "graded readers", "graded readers là gì", "extensive reading", "đọc sách tiếng anh", "học tiếng anh qua đọc sách", "tiếng anh không khó"]},
 "video": {"previewAssetId": preview_id, "duration": dur_full, "introSeconds": 13, "contentDuration": tl['total'],
   "pauses": len(tl['pauses']), "chapterScenes": sum(1 for s in sc['scenes'] if s['t'] == 'chapter'),
   "sfxMarks": len(tl['sfx']), "fullNote": f"Bản 1080p đầy đủ ({size_mb} MB, đã ghép intro 13 giây) nằm trong phiên chat ngày 26/11/2026 (gửi bằng thẻ file), tên hoc-tu-vung-tieng-anh-qua-bai-doc.mp4.",
   "filename": "hoc-tu-vung-tieng-anh-qua-bai-doc.mp4", "previewFilename": "hoc-tu-vung-tieng-anh-qua-bai-doc-preview.mp4", "srtFilename": "hoc-tu-vung-tieng-anh-qua-bai-doc.srt",
   "stock": [{"scene": k, **v} for k, v in json.load(open('out/stock.json')).items()]},
 "images": [{"platform": "youtube", "kind": "thumbnail", "assetId": thumb_id, "filename": "hoc-tu-vung-tieng-anh-qua-bai-doc-thumbnail.png", "alt": "Thumbnail: Đọc nhiều mà vẫn quên từ? – sinh viên đọc sách trong thư viện, nhãn vàng Nghiên cứu nói gì?"}],
 "sources": [{"title": t, "url": u} for t, u in sources],
 "createdAt": now,
}
json.dump(doc, open('out/doc.json', 'w'), ensure_ascii=False, indent=1)
open('out/seo_3_nen_tang.txt','w',encoding='utf-8').write('=== YOUTUBE · TIÊU ĐỀ ===\n\n'+YT_TITLE+'\n\n=== YOUTUBE · MÔ TẢ ===\n\n'+desc+'\n\n=== YOUTUBE · TAGS ===\n\n'+', '.join(doc['seo']['tags'])+'\n\n=== TIKTOK · CAPTION ===\n\n'+tiktok+'\n\n=== FACEBOOK · CAPTION ===\n\n'+facebook+'\n')
print('title len', len(doc['seo']['title']), 'desc len', len(desc), 'Lan?', 'Lan ' in json.dumps(doc, ensure_ascii=False))
