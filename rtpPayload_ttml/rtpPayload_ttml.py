from __future__ import annotations
from encodings.aliases import aliases  # type: ignore


SUPPORTED_ENCODINGS = [
    "utf_8",
    "utf-8",
    "utf_8_sig",
    "utf_16",
    "utf_16_le",
    "utf_16_be",
    "utf-16"]


class LengthError(Exception):
    '''
    Data is an invalid length.
    '''

    pass


class RTPPayload_TTML:
    '''
    A data structure for storing TTML RTP payloadsas defined by RFC XXXX.

    Attributes:
        reserved (bytearray): The reserved bits. MUST be set to ``0``.
        userDataWords (str): The TTML document.
    '''

    def __init__(
       self,
       reserved: bytearray = bytearray(b'\x00\x00'),
       userDataWords: str = "",
       encoding: str = "utf-8") -> None:
        self._userDataWords: bytearray
        self.reserved = reserved

        if aliases.get(encoding, encoding) in SUPPORTED_ENCODINGS:
            self._encoding = encoding
        else:
            raise ValueError("Encoding must be a valid python codec alias for "
                             "utf-8 or utf-16")

        self.userDataWords = userDataWords

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RTPPayload_TTML):
            return NotImplemented

        return (
            (type(self) == type(other)) and
            (self.reserved == other.reserved) and
            (self.userDataWords == other.userDataWords) and
            (self._encoding == other._encoding))

    @property
    def reserved(self) -> bytearray:
        return self._reserved

    @reserved.setter
    def reserved(self, p: bytearray) -> None:
        if type(p) != bytearray:
            raise AttributeError("Payload value must be bytearray")
        if p != bytearray(b'\x00\x00'):
            # TODO: Include RFC number in error
            raise ValueError("Reserved bits must be '\x00\x00' under RFC XXXX")
        else:
            self._reserved = p

    @property
    def userDataWords(self) -> str:
        return self._userDataWords.decode(self._encoding)

    @userDataWords.setter
    def userDataWords(self, p: str) -> None:
        workingUDW = None
        if isinstance(p, str):
            workingUDW = bytearray(p, self._encoding)
        else:
            raise AttributeError("userDataWords must be a str")

        if (len(workingUDW) >= 2**16):
            raise LengthError(
                "userDataWords must be fewer than 2**16 bytes")
        else:
            self._userDataWords = workingUDW

    def fromBytearray(self, packet: bytearray) -> RTPPayload_TTML:
        '''
        Populate instance from a bytearray.
        '''

        self.reserved = packet[0:2]
        length = int.from_bytes(packet[2:4], byteorder='big')
        self._userDataWords = packet[4:]
        if length != len(self._userDataWords):
            raise LengthError(
                "Length field does not match length of userDataWords")

        return self

    def toBytearray(self) -> bytearray:
        '''
        Encode instance as a bytearray.
        '''

        packetLen = 4 + len(self._userDataWords)

        packet = bytearray(packetLen)

        packet[0:2] = self.reserved
        packet[2:4] = len(self._userDataWords).to_bytes(2, byteorder='big')
        packet[4:] = self._userDataWords

        return packet

    def __bytes__(self) -> bytes:
        return bytes(self.toBytearray())
