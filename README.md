# Demo hàm băm MD5

Dự án minh họa thuật toán băm MD5 theo RFC 1321. Phần thuật toán được tự cài đặt bằng Python; không dùng `hashlib.md5()` để tạo digest trong chức năng chính.

## 1\. Cấu trúc dự án

```text
MD5_Project
├── main.py         :Giao diện dòng lệnh, nhận đầu vào và điều phối chức năng
├── md5_core.py    :Hằng số, padding, phép toán 32 bit và lõi MD5
├── integrity.py    :Đọc tệp, tính MD5 tệp và kiểm tra tính toàn vẹn
├── self_test.py   :Test vector và các kiểm thử đối chiếu
└── README.md       :Tài liệu hướng dẫn
```

## 2\. Yêu cầu

* Python 3.10 trở lên.
* Không dùng thư viện mật mã có sẵn cho phần lõi.
* Chỉ `self_test.py` import `hashlib` và `tempfile` để đối chiếu kết quả và tạo tệp tạm phục vụ kiểm thử.

## 3\. Chạy chương trình

Mở CMD/Terminal tại thư mục dự án và chạy:

```bash
python main.py
```

Menu gồm:

1. Tính MD5 cho văn bản.
2. Tính MD5 cho một tệp.
3. Kiểm tra tính toàn vẹn của tệp bằng digest tham chiếu.
4. Chạy bộ tự kiểm thử.
0. Thoát

## 4\. Chạy kiểm thử

Có thể chạy bộ tự kiểm thử mà không mở menu:

```bash
python -c "from self_test import self_test; self_test()"
```

Kết quả kỳ vọng: 14/14 hạng mục đạt và dòng cuối hiển thị `OK`.

## 5\. Phạm vi và giới hạn

* Phần lõi MD5 được tự cài đặt; 64 hằng số được khai báo theo RFC 1321.
* Hàm `hash_file()` hiện đọc toàn bộ nội dung tệp vào bộ nhớ, phù hợp với demo tệp nhỏ.
* MD5 không còn phù hợp cho ứng dụng cần khả năng chống va chạm. Chức năng đối chiếu digest chỉ minh họa phát hiện thay đổi thông thường, không cung cấp xác thực an toàn trước đối thủ chủ động.

## 6\. Tài liệu tham khảo

* R. Rivest, *The MD5 Message-Digest Algorithm*, RFC 1321, 1992: https://www.rfc-editor.org/rfc/rfc1321
* S. Turner and L. Chen, *Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms*, RFC 6151, 2011: https://www.rfc-editor.org/rfc/rfc6151

