# Tiếng Anh Không Khó · quy trình tạo video

Quy tắc của anh Tuấn, chốt ngày 26/11/2026.

## Nơi tạo và gửi video

- Mọi video dài và reel đều được tạo trong phiên chat "Tổng hợp video dài và ngắn", rồi **gửi thẳng vào phiên này** bằng SendUserFile. Gửi đủ các file: video, thumbnail, phụ đề, `seo_3_nen_tang.txt`.
- **Không dùng trang duyệt bài nữa** (anh Tuấn chốt 26/11/2026). Không tải file lên đó, không ghi dữ liệu vào đó.
- Hai lịch tự động cũ ("Video dài Tiếng Anh Không Khó", "Reel vệ tinh") đã tắt. Chúng chưa bị xóa.

## Lịch làm video

Cả hai lịch đều chạy ngay trong phiên này.

- **21h tối Chủ nhật đến thứ 5:** làm 1 reel quảng bá cho video dài của thứ 7 gần nhất trước ngày đăng. Reel đăng vào ngày hôm sau, tức thứ 2 đến thứ 6.
- **20h tối thứ 4:** lịch "Đề xuất chủ đề video dài" chạy trong một phiên riêng và đề xuất 3 chủ đề kèm từ khóa, tiêu đề và dàn ý. Kết quả được gửi email cho anh Tuấn, đồng thời gửi tin nhắn "[Đề xuất chủ đề video dài thứ 7 …]" vào phiên này. Anh Tuấn chốt chủ đề bằng cách nhắn trong phiên này. Khi anh chốt, ghi chủ đề vào `data/plan.json` với status `approved`.
- **21h tối thứ 6:** làm video dài để đăng thứ 7 hôm sau. Thứ tự chọn chủ đề: mục `approved` trong plan, rồi đến chủ đề anh đã chốt trong phiên. Nếu anh chưa chốt thì làm chủ đề 1 và nói rõ điều đó.
- **Không làm trùng:** nếu `data/catalog.json` đã có video cùng loại cho ngày đăng đó thì không làm thêm, chỉ báo lại cho anh Tuấn.

## Dữ liệu (lưu trong repo này)

- `data/catalog.json`: danh sách video và reel đã làm (ngày, loại, chủ đề, từ khóa, tiêu đề, video mẹ, bộ hình). Dùng để tránh trùng và để biết video mẹ.
- `data/videos_covered.json`, `data/reels_covered.json`: nội dung chi tiết đã dạy. Video mới không được lặp lại các nội dung này.
- `data/plan.json`: kế hoạch đã duyệt. Nếu có mục `approved` cho ngày đăng thì làm đúng mục đó.
- `data/videostyle.json`, `data/reelstyle.json` (gồm mục diversity), `data/introrule.json`, `data/performance.json`: phong cách, intro và bài học từ kết quả thật.
- `assets/intro-13s.mp4`, `assets/logo.png`.
- Bộ công cụ dựng video nằm trong `tools/`, xem `tools/README.md`.
- **Sau mỗi video:** nối thêm một mục vào `data/catalog.json` và vào file covered tương ứng, đổi mục trong `data/plan.json` (nếu có) sang `done`, rồi commit và push lên nhánh `claude/determined-gauss-dry0g1`. Không commit file video.

## SEO bắt buộc cho mỗi video

1. Tiêu đề phải chứa từ khóa SEO chính, lấy từ gợi ý tìm kiếm của YouTube hoặc Google.
2. Mỗi video có mô tả chuẩn SEO riêng cho 3 nền tảng:
   - YouTube: tiêu đề, mô tả, tags.
   - TikTok: caption và hashtag.
   - Facebook: caption và hashtag.
3. Viết sao cho dễ copy: **mỗi câu là một đoạn riêng, cách nhau một dòng trống**, không để các câu dính liền nhau. Riêng các danh sách (mục lục có mốc thời gian, nguồn, khối liên kết) thì mỗi mục nằm trên một dòng.
4. Gửi kèm file `seo_3_nen_tang.txt`, đồng thời dán từng phần vào một khối code riêng trong tin nhắn trả lời để bấm copy.

## Các quy tắc cũ vẫn giữ

- Giọng đọc và model cố định: voice `ueSxRO0nLF1bj93J2hVt`, model `eleven_v3`. Khóa API nằm trong biến môi trường `EL_KEY` và `PX_KEY`; không in giá trị ra.
- Video dài phải ghép intro kênh 13 giây.
- Tên file chuẩn SEO: không dấu, nối bằng gạch ngang.
- Không dùng tên "Lan".
- Video dài có phần thưởng ở cuối.
- Mọi dữ kiện đều phải được nghiên cứu, có factCheck và dẫn nguồn (trên hình và trong mô tả).
- Có SFX ở mọi chuyển cảnh.
- Không tự đăng lên bất kỳ nền tảng nào.
