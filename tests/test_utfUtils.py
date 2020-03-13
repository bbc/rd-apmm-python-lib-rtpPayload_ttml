#!/usr/bin/python
#
# Copyright 2020 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase
from hypothesis import given, strategies as st
from rtpPayload_ttml import SUPPORTED_ENCODINGS, utfEncode, utfDecode
from rtpPayload_ttml.utfUtils import BOMS, ENCODING_ALIASES


class TestExtension (TestCase):
    @given(st.text())
    def test_encode_default(self, doc):
        ret = utfEncode(doc)

        self.assertEqual(ret, bytearray(doc, "utf_8"))

    @given(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans())
    def test_encode_encodings(self, doc, encoding, bom):
        ret = utfEncode(doc, encoding, bom)

        if bom:
            self.assertTrue(ret.startswith(BOMS[encoding]))
            ret = ret[len(BOMS[encoding]):]

        self.assertEqual(doc, ret.decode(ENCODING_ALIASES[encoding]))

    @given(
        st.text(),
        st.text().filter(lambda x: x not in SUPPORTED_ENCODINGS),
        st.booleans())
    def test_encode_invalid(self, doc, enc, bom):
        with self.assertRaises(AttributeError):
            utfEncode(doc, enc, bom)

    @given(st.tuples(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans()))
    def test_decode(self, data):
        doc, encoding, bom = data
        encoded = utfEncode(doc, encoding, bom)
        decoded = utfDecode(encoded, encoding)

        self.assertEqual(doc, decoded)

    @given(st.text())
    def test_decode_utf16(self, doc):
        # UTF-16 can decode both little and big endian
        for enc in ["UTF-16LE", "UTF-16BE"]:
            encoded = utfEncode(doc, enc, True)
            decoded = utfDecode(encoded, "UTF-16")

            self.assertEqual(doc, decoded)

    @given(st.text())
    def test_decode_wrongBom(self, doc):
        for enc, dec in [
           ("UTF-16LE", "UTF-16BE"),
           ("UTF-16LE", "UTF-8"),
           ("UTF-16BE", "UTF-16LE"),
           ("UTF-16BE", "UTF-8"),
           ("UTF-8", "UTF-16BE"),
           ("UTF-8", "UTF-16LE")
           ]:
            encoded = utfEncode(doc, enc, True)

            with self.assertRaises(ValueError):
                utfDecode(encoded, dec)

    @given(
        st.binary(),
        st.text().filter(lambda x: x not in SUPPORTED_ENCODINGS))
    def test_decode_invalid(self, doc, enc):
        with self.assertRaises(AttributeError):
            utfDecode(bytearray(doc), enc)
