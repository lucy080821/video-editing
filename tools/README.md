# Bộ công cụ dựng video (phiên 26/11/2026)

Video mẫu: posts/2026-11-28, "Học từ vựng tiếng Anh qua bài đọc", phong cách documentary-vox-motion, khung 1920×1080.

## Khôi phục môi trường dựng

```bash
mkdir -p ~/doc && cp tools/doc/* ~/doc/ && cp -r tools/sfx ~/doc/sfx
cd ~/doc
npm init -y
npm i @fontsource/anton @fontsource/be-vietnam-pro @fontsource/patrick-hand @fontsource/noto-serif @fontsource/montserrat
```

Chép thêm intro và logo từ repo:

```bash
cp assets/logo.png ~/doc/logo.png && cp assets/intro-13s.mp4 ~/doc/intro.mp4
```

## Quy trình

1. Viết kịch bản `doc_script.json`. Các cảnh dùng các loại có sẵn trong `stage.html`; mọi trường `at` hoặc `*_at` phải là cụm nguyên văn trong `vo` của cảnh đó.
2. `python3 doc_media.py doc_script.json out` tạo giọng đọc (voice và model cố định), nhạc nền và cảnh quay tư liệu Pixabay cho các cảnh `stock`.
3. `python3 timeline.py doc_script.json out` tạo dòng thời gian, phụ đề, mục lục và bản trộn âm thanh `mix.m4a`. Sau đó chạy `python3 prep_stock.py` để tách khung hình cho các cảnh `stock`.
4. Kiểm tra thử: `node render.js out still t1,t2,...` để chụp vài khung hình rồi xem.
5. Dựng thật: `node render.js out 4` (4 luồng, khoảng 25 phút cho 12 phút video). Sau đó ghép các phần, ghép âm thanh và ghép intro, theo lệnh trong `data/introrule.json`.
6. Tạo bản xem trước dưới 15 MB, tạo thumbnail từ `thumb.html`, rồi chạy `build_doc.py` để có SEO 3 nền tảng. Phần `build_doc.py` ghi document cho trang duyệt bài giờ không cần nữa; chỉ dùng phần tạo `seo_3_nen_tang.txt`.

## Reel (khung dọc 1080×1920)

Viết lại `stage.html` theo khổ dọc và theo `data/reelstyle.json`, mục diversity. Mỗi reel phải dùng một bộ hình mới, không lặp lại reel trước.
