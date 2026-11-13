#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Các chức năng đọc tệp, tính MD5 tệp và kiểm tra tính toàn vẹn."""

from md5_core import md5


def read_file(path):
    """Đọc toàn bộ nội dung tệp dưới dạng bytes."""
    with open(path, "rb") as file:
        return file.read()


def hash_file(path):
    """Tính giá trị MD5 của một tệp bằng lõi MD5 tự cài đặt."""
    return md5(read_file(path))


def verify_file(path, expected_digest):
    """So sánh digest của tệp với digest tham chiếu đã được cung cấp.

    Giá trị tham chiếu phải gồm đúng 32 ký tự hex. Hàm này chỉ minh họa
    đối chiếu digest; MD5 không bảo đảm chống giả mạo trước đối thủ chủ động.
    """
    actual = hash_file(path)
    normalized = expected_digest.strip().lower()
    is_valid_digest = len(normalized) == 32 and all(
        char in "0123456789abcdef" for char in normalized
    )
    matched = is_valid_digest and (actual == normalized)
    return matched, actual


__all__ = ["read_file", "hash_file", "verify_file"]
