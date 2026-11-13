#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Bộ tự kiểm thử cho lõi MD5 và chức năng kiểm tra tính toàn vẹn.
#Chỉ module kiểm thử này sử dụng hashlib để đối chiếu và tempfile để tạo các tệp thử nghiệm tạm thời. Các module thuật toán không dùng thư viện đó.
from md5_core import md5, md5_text
from integrity import hash_file, verify_file


def self_test():
    import hashlib
    import tempfile

    vectors = [
        (b"", "d41d8cd98f00b204e9800998ecf8427e"),
        (b"a", "0cc175b9c0f1b6a831c399e269772661"),
        (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
        (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
        (b"abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
        (
            b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "d174ab98d277d9f5a5611c2c9f419d9f",
        ),
        (b"1234567890" * 8, "57edf4a22be3c955ac49da2e2107b67a"),
    ]

    total = 0
    passed = 0

    def check(name, condition):
        nonlocal total, passed
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}")

    print("\n========== TỰ KIỂM THỬ MD5 ==========")

    for index, (message, expected) in enumerate(vectors, start=1):
        check(f"RFC 1321 test vector {index}", md5(message) == expected)

    boundary_ok = True
    for length in (0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1024):
        data = bytes(i % 256 for i in range(length))
        if md5(data) != hashlib.md5(data).hexdigest():
            boundary_ok = False
            break
    check("Độ dài biên padding và khối dữ liệu", boundary_ok)

    unicode_text = "Xin chào Việt Nam"
    unicode_ok = md5_text(unicode_text) == hashlib.md5(
        unicode_text.encode("utf-8")
    ).hexdigest()
    check("Văn bản tiếng Việt UTF-8", unicode_ok)

    try:
        md5("abc")
        type_ok = False
    except TypeError:
        type_ok = True
    check("Từ chối đầu vào chuỗi chưa mã hóa thành bytes", type_ok)

    trace_message = b"MD5 trace test"
    trace_result = md5(trace_message, trace=True)
    trace_ok = (
        isinstance(trace_result, tuple)
        and trace_result[0] == hashlib.md5(trace_message).hexdigest()
        and len(trace_result[1]) == 64
    )
    check("Trace có đủ 64 bước cho thông điệp kiểm thử một khối", trace_ok)

    with tempfile.TemporaryDirectory() as directory:
        sample = directory + "/sample.txt"
        with open(sample, "wb") as file:
            file.write(b"MD5 integrity test")

        original_digest = hash_file(sample)
        match_ok = verify_file(sample, original_digest.upper())[0]
        check("Tệp nguyên bản khớp digest tham chiếu", match_ok)

        with open(sample, "wb") as file:
            file.write(b"MD5 integrity test changed")
        mismatch_ok = not verify_file(sample, original_digest)[0]
        check("Tệp thay đổi không khớp digest cũ", mismatch_ok)

        invalid_ok = not verify_file(sample, "not-a-digest")[0]
        check("Từ chối digest sai định dạng", invalid_ok)

    print(f"\nKết quả: {passed}/{total} kiểm tra đạt.")
    print("OK" if passed == total else "CÓ KIỂM TRA THẤT BẠI")
    return passed == total


__all__ = ["self_test"]
