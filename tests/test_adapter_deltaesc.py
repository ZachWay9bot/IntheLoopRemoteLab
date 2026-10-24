"""No physical serial I/O: G30 read-only adapter behavior with stock vs DeltaESC."""
import struct
import unittest
from remotelab.adapters.deltaesc import DeltaEscReadOnlyAdapter
from remotelab.adapters.xbot.protocol import decode_frame, frame

class MockSerial:
    def __init__(self, name="DELTAESC-G30D0"):
        self.port="MOCK";self.name=name;self.pending=bytearray()
        self.requests=[];self.closed=False
    def reset_input_buffer(self): self.pending.clear()
    def close(self):self.closed=True
    def write(self,packet):
        p=decode_frame(packet)
        self.requests.append(p)
        if p["cmd"]!=1:
            raise AssertionError("non-read operation sent")
        reg=p["index"]
        if reg==0x10: value=self.name.encode("ascii")[:14].ljust(14,b"\x00")
        elif reg==0xD0:
            value=bytearray(16);value[:4]=b"DESC";value[8]=2
            struct.pack_into("<HHH",value,10,0,16000,4000)
        elif reg==0xD9:
            value=bytearray(16);struct.pack_into("<H",value,6,8);value[8]=1
        elif reg==0xFF:
            value=bytearray(12);value[:4]=b"PF13";value[4]=15
            struct.pack_into("<H",value,6,800);value[11]=1
        else:raise AssertionError(f"Unknown read 0x{reg:02X}")
        if not isinstance(value,bytes):value=bytes(value)
        assert p["data"]==bytes((len(value),))
        self.pending.extend(packet) # common single-wire TX echo
        self.pending.extend(frame(4,reg,value,src=0x20,dst=0x3d))
        return len(packet)
    def read(self,n):
        if not self.pending:return b""
        z=bytes(self.pending[:n]);del self.pending[:n];return z

class AdapterTest(unittest.TestCase):
    def test_identify_stock_only(self):
        fake=MockSerial("DRV1.8.7")
        a=DeltaEscReadOnlyAdapter(port="MOCK",serial_factory=lambda _:fake)
        result=a.identify()
        self.assertEqual(result["identity"],"DRV1.8.7")
        self.assertFalse(result["is_deltaesc"])
        self.assertEqual([r["index"] for r in fake.requests],[0x10])
        self.assertTrue(fake.closed)
    def test_diagnose_stock_avoids_delta_regs(self):
        fake=MockSerial("DRV1.8.7")
        a=DeltaEscReadOnlyAdapter(port="MOCK",serial_factory=lambda _:fake)
        r=a.diagnose()
        self.assertFalse(r["is_deltaesc"])
        self.assertEqual([p["index"] for p in fake.requests],[0x10])
    def test_diagnose_delta(self):
        fake=MockSerial()
        a=DeltaEscReadOnlyAdapter(port="MOCK",serial_factory=lambda _:fake)
        result=a.diagnose()
        self.assertTrue(result["is_deltaesc"])
        self.assertEqual(result["pole_pairs"],15)
        self.assertEqual(result["pwm_hz"],16000)
        self.assertEqual(result["control_hz"],4000)
        self.assertEqual(result["commissioning_guard_mask"],8)
        self.assertFalse(result["real_motor_run_verified"])
        self.assertFalse(result["iap_or_recovery_verified"])
        self.assertEqual([p["index"] for p in fake.requests],[0x10,0xD0,0xD9,0xFF])
    def test_no_flash_api(self):
        adapter=DeltaEscReadOnlyAdapter(port="MOCK")
        with self.assertRaises(PermissionError):adapter.flash(b"binary")
        with self.assertRaises(PermissionError):adapter.run_test("motor")

if __name__ == "__main__":
    unittest.main()
