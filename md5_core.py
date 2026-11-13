#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Lõi thuật toán MD5 tự cài đặt theo đặc tả RFC 1321:
#Module này chỉ chứa hằng số và các phép tính của MD5.
#Không sử dụng hashlib hoặc thư viện hỗ trợ MD5 có sẵn.
_MASK32 = 0xFFFFFFFF
_MASK64 = 0xFFFFFFFFFFFFFFFF

_SHIFT = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

_K = [
    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE,
    0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
    0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
    0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
    0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
    0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
    0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
    0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039,
    0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
    0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
    0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391,
]

_INITIAL_STATE = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)


def _left_rotate(value, amount):
    value &= _MASK32
    return ((value << amount) | (value >> (32 - amount))) & _MASK32


def _append_little_endian_64(target, value):
    for shift in range(0, 64, 8):
        target.append((value >> shift) & 0xFF)


def _read_words_little_endian(block):
    words = []
    for offset in range(0, 64, 4):
        word = (
            block[offset]
            | (block[offset + 1] << 8)
            | (block[offset + 2] << 16)
            | (block[offset + 3] << 24)
        )
        words.append(word)
    return words


def _state_to_hex_little_endian(state_words):
    digest_bytes = bytearray()
    for word in state_words:
        for shift in (0, 8, 16, 24):
            digest_bytes.append((word >> shift) & 0xFF)
    return "".join(f"{value:02x}" for value in digest_bytes)


def _pad(message):
    original_length_bits = (len(message) * 8) & _MASK64
    padded = bytearray(message)
    padded.append(0x80)

    while len(padded) % 64 != 56:
        padded.append(0)

    _append_little_endian_64(padded, original_length_bits)
    return bytes(padded)


def md5(message, *, trace=False):
    if not isinstance(message, (bytes, bytearray, memoryview)):
        raise TypeError("md5() cần bytes; hãy mã hóa văn bản bằng UTF-8 trước.")

    data = _pad(bytes(message))
    a0, b0, c0, d0 = _INITIAL_STATE
    trace_rows = []

    for block_index in range(0, len(data), 64):
        block = data[block_index:block_index + 64]
        words = _read_words_little_endian(block)
        a, b, c, d = a0, b0, c0, d0

        for i in range(64):
            if i < 16:
                function = (b & c) | ((~b) & d)
                word_index = i
                round_number = 1
            elif i < 32:
                function = (d & b) | ((~d) & c)
                word_index = (5 * i + 1) % 16
                round_number = 2
            elif i < 48:
                function = b ^ c ^ d
                word_index = (3 * i + 5) % 16
                round_number = 3
            else:
                function = c ^ (b | (~d))
                word_index = (7 * i) % 16
                round_number = 4

            mixed = (a + function + _K[i] + words[word_index]) & _MASK32
            rotated = _left_rotate(mixed, _SHIFT[i])

            old_b, old_c, old_d = b, c, d
            a = old_d
            b = (old_b + rotated) & _MASK32
            c = old_b
            d = old_c

            if trace:
                trace_rows.append(
                    {
                        "block": block_index // 64 + 1,
                        "step": i + 1,
                        "round": round_number,
                        "word_index": word_index,
                        "A": f"{a:08x}",
                        "B": f"{b:08x}",
                        "C": f"{c:08x}",
                        "D": f"{d:08x}",
                    }
                )

        a0 = (a0 + a) & _MASK32
        b0 = (b0 + b) & _MASK32
        c0 = (c0 + c) & _MASK32
        d0 = (d0 + d) & _MASK32

    digest = _state_to_hex_little_endian((a0, b0, c0, d0))
    return (digest, trace_rows) if trace else digest


def md5_text(text):
    return md5(text.encode("utf-8"))


__all__ = ["md5", "md5_text"]
