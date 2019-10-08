#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase
from hypothesis import given, strategies as st
from rtpPayload_ttml import RTPPayload_TTML, LengthError


class TestExtension (TestCase):
    def setUp(self):
        self.thisP = RTPPayload_TTML()

    @given(st.text().filter(lambda x: len(bytearray(x, "utf-8")) < 2**16))
    def test_init(self, doc):
        reservedBits = bytearray(b'\x00\x00')
        newP = RTPPayload_TTML(reservedBits, doc)

        self.assertEqual(newP.reserved, reservedBits)
        self.assertEqual(newP.userDataWords, doc)

    def test_reserved_default(self):
        self.assertEqual(self.thisP.reserved, bytearray(b'\x00\x00'))

    def test_reserved_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisP.reserved = ""

    @given(st.binary().filter(lambda x: x != bytearray(b'\x00\x00')))
    def test_reserved_invalid(self, value):
        with self.assertRaises(ValueError):
            self.thisP.reserved = bytearray(value)

    def test_userDataWords_default(self):
        self.assertEqual(self.thisP.userDataWords, "")

    @given(st.text().filter(lambda x: len(bytearray(x, "utf-8")) < 2**16))
    def test_userDataWords(self, doc):
        self.thisP.userDataWords = doc
        self.assertEqual(self.thisP.userDataWords, doc)

    def test_userDataWords_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisP.userDataWords = 0

    def test_userDataWords_tooLong(self):
        doc = ""
        for x in range(2**16):
            doc += "a"
        with self.assertRaises(LengthError):
            self.thisP.userDataWords = doc

    def test_eq(self):
        reservedBits = bytearray(b'\x00\x00')
        newP = RTPPayload_TTML(reservedBits, "")

        self.assertEqual(newP, self.thisP)

    def test_bytearray_default(self):
        expected = bytearray(4)
        self.assertEqual(bytes(self.thisP), expected)

        newP = RTPPayload_TTML().fromBytearray(expected)
        self.assertEqual(newP, self.thisP)

    @given(st.binary(min_size=2, max_size=2).filter(
        lambda x: x != b'\x00\x00'))
    def test_fromBytearray_invalidLen(self, length):
        bArray = bytearray(4)
        bArray[2:4] = length

        with self.assertRaises(LengthError):
            RTPPayload_TTML().fromBytearray(bArray)

    @given(st.text())
    def test_toBytearray(self, doc):
        self.thisP.userDataWords = doc

        bDoc = bytearray(doc, "utf-8")
        expected = bytearray(2)
        expected += int(len(bDoc)).to_bytes(2, byteorder='big')
        expected += bDoc

        self.assertEqual(expected, self.thisP.toBytearray())

    @given(st.text())
    def test_fromBytearray(self, doc):
        expected = RTPPayload_TTML(userDataWords=doc)

        bDoc = bytearray(doc, "utf-8")
        bArray = bytearray(2)
        bArray += int(len(bDoc)).to_bytes(2, byteorder='big')
        bArray += bDoc

        self.thisP.fromBytearray(bArray)

        self.assertEqual(expected, self.thisP)
