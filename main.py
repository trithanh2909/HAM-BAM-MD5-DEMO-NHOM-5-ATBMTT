#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Giao diện dòng lệnh cho chương trình minh họa thuật toán MD5."""

from md5_core import md5, md5_text
from integrity import read_file, verify_file
from self_test import self_test


def ask_path():
    """Nhận và kiểm tra đường dẫn tệp do người dùng nhập."""
    raw = input("Nhập đường dẫn tệp (có thể kéo-thả tệp vào CMD): ").strip().strip('"')
    if not raw:
        print("Đường dẫn không được để trống.")
        return None

    try:
        # Mở tệp ở chế độ nhị phân để kiểm tra đường dẫn và quyền đọc.
        with open(raw, "rb") as file:
            file.read(1)
    except OSError:
        print("Không tìm thấy tệp. Hãy kiểm tra đường dẫn rồi thử lại.")
        return None
    return raw


def menu():
    """Hiển thị menu và điều phối các chức năng của chương trình."""
    while True:
        print("\n========== DEMO HÀM BĂM MD5 ==========")
        print("1. Tính MD5 cho văn bản")
        print("2. Tính MD5 cho một tệp")
        print("3. Kiểm tra tính toàn vẹn của tệp")
        print("4. Chạy bộ tự kiểm thử")
        print("0. Thoát")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            text = input("Nhập văn bản: ")
            print(f"Độ dài UTF-8: {len(text.encode('utf-8'))} byte")
            print(f"MD5 = {md5_text(text)}")

        elif choice == "2":
            path = ask_path()
            if path:
                try:
                    data = read_file(path)
                    print(f"Tệp: {path}")
                    print(f"Kích thước: {len(data)} byte")
                    print(f"MD5 = {md5(data)}")
                except OSError as error:
                    print(f"Không thể đọc tệp: {error}")

        elif choice == "3":
            path = ask_path()
            if path:
                expected = input("Nhập digest MD5 tham chiếu (32 ký tự hex): ").strip()
                try:
                    matched, actual = verify_file(path, expected)
                    print(f"MD5 tính được: {actual}")
                    print(
                        "KẾT QUẢ: KHỚP."
                        if matched
                        else "KẾT QUẢ: KHÔNG KHỚP hoặc digest tham chiếu không hợp lệ."
                    )
                    print("Lưu ý: MD5 không bảo đảm chống giả mạo trước đối thủ chủ động.")
                except OSError as error:
                    print(f"Không thể đọc tệp: {error}")

        elif choice == "4":
            self_test()

        elif choice == "0":
            print("Kết thúc demo.")
            return

        else:
            print("Lựa chọn không hợp lệ. Hãy nhập 1, 2, 3, 4 hoặc 0.")


def main():
    """Điểm bắt đầu chương trình."""
    menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
        raise SystemExit(130)
