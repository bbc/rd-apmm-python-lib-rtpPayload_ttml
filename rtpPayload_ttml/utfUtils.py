# Copyright 2020 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from __future__ import annotations
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE

ENCODING_ALIASES = {
    "UTF-8": "utf_8",
    "UTF-16": "utf_16_be",  # Defaults to UTF-16BE as per Unicode Clause D98
    "UTF-16LE": "utf_16_le",
    "UTF-16BE": "utf_16_be"
}


SUPPORTED_ENCODINGS = sorted(ENCODING_ALIASES.keys())


BOMS = {
    "UTF-8": BOM_UTF8,
    "UTF-16": BOM_UTF16_BE,  # Defaults to UTF-16BE as per Unicode Clause D98
    "UTF-16LE": BOM_UTF16_LE,
    "UTF-16BE": BOM_UTF16_BE
}


def utfEncode(s: str, encoding: str = "UTF-8", bom: bool = False) -> bytearray:
    '''
    Encode a string as a utf bytearray

    Attributes:
        s (str): The string to encode
        encoding (str): One of UTF-8, UTF-16, UTF-16LE, and UTF-16BE
        bom (bool): Should encoded documents start with a byte-order mark
    '''
    encoded = bytearray()
    if not isinstance(s, str):
        raise AttributeError("s must be a str")

    if encoding not in ENCODING_ALIASES:
        raise AttributeError("Encoding {} not suport".format(encoding))

    if bom:
        encoded = bytearray(BOMS[encoding])

    encoded += bytearray(s, ENCODING_ALIASES[encoding])

    return encoded


def utfDecode(s: bytearray, encoding: str = "UTF-8") -> str:
    '''
    Decode a utf bytearray as a str

    Attributes:
        s (bytearray): The bytearray to decode
        encoding (str): One of UTF-8, UTF-16, UTF-16LE, and UTF-16BE
    '''
    toDecode = s
    useEncoding = encoding

    if not isinstance(s, bytearray):
        raise AttributeError("s must be a bytearray")

    if encoding not in ENCODING_ALIASES:
        raise AttributeError("Encoding {} not suported".format(encoding))

    for bom in BOMS.values():
        if s.startswith(bom):
            if (encoding == "UTF-16") and (bom == BOMS["UTF-16LE"]):
                # UTF-16 can be either BE or LE
                useEncoding = "UTF-16LE"
            elif bom != BOMS[encoding]:
                raise ValueError(
                    "BOM doesn't match expected encoding")
            toDecode = s[len(bom):]
            break

    return toDecode.decode(ENCODING_ALIASES[useEncoding])
