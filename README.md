# rtpPayload_ttml

This python library provides a means to decode, encode, and interact with TTML RTP payloads. It is designed for use with an RTP library such as [RTP](https://github.com/bbc/rd-apmm-python-lib-rtp). It only encodes/decodes the payload bitstreams. It DOES NOT provide a means to render or edit TTML documents.

## Example usage
```python
from rtp import *
from rtpPayload_ttml import RTPPayload_TTML
from copy import deepcopy

baseRTP = RTP(
    marker=True,
    payloadType=PayloadType.L16_2chan,
    extension=Extension(
        startBits=getExtStartBits(),
        headerExtension=getExtBody()
        ),
    csrcList=getCSRCList()
)
thisRTPBitstream = thisRTP.toBytearray()

while runing:
    nextRTP = deepcopy(baseRTP)
    nextRTP.sequenceNumber += 1
    nextRTP.timestamp = getNextTimestamp()
    nextRTP.payload = RTPPayload_TTML(userDataWords=getNextDoc())

    transmit(nextRTP)
```

```python
from rtp import RTP
from rtpPayload_ttml import RTPPayload_TTML

decodedPayload = RTPPayload_TTML.fromBytearray(
    RTP().fromBytearray(getNextPacket()).payload)
document = decodedPayload.userDataWords

render(document)
```
