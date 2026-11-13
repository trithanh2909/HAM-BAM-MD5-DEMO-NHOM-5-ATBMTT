#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Các chức năng đọc tệp, tính MD5 tệp và kiểm tra tính toàn vẹn:
from md5_core import md5


def read_file(path):
    with open(path, "rb") as file:
        return file.read()


def hash_file(path):
    return md5(read_file(path))


def verify_file(path, expected_digest):
    actual = hash_file(path)
    normalized = expected_digest.strip().lower()
    is_valid_digest = len(normalized) == 32 and all(
        char in "0123456789abcdef" for char in normalized
    )
    matched = is_valid_digest and (actual == normalized)
    return matched, actual


__all__ = ["read_file", "hash_file", "verify_file"]
