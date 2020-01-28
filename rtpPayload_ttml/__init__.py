#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from .rtpPayload_ttml import RTPPayload_TTML, LengthError, SUPPORTED_ENCODINGS

__all__ = ["RTPPayload_TTML", "LengthError", "SUPPORTED_ENCODINGS"]

template = True
