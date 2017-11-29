from binascii import hexlify, unhexlify
from sha3 import keccak_256

from . import base58

class Address(object):
    def __init__(self, address):
        address = str(address)
        if len(address) != 95:
            raise ValueError("Address must be 95 characters long, is %d" % len(address))
        self._decode(address)

    def _decode(self, address):
        self._decoded = unhexlify(base58.decode(address))
        checksum = self._decoded[-4:]
        if checksum != keccak_256(self._decoded[:-4]).digest()[:4]:
            raise ValueError("Invalid checksum")

    def is_testnet(self):
        return self._decoded[0] in bytes([53, 54])

    def get_view_key(self):
        return hexlify(self._decoded[33:65]).decode()

    def get_spend_key(self):
        return hexlify(self._decoded[1:33]).decode()

    def with_payment_id(self, payment_id=0):
        if isinstance(payment_id, (bytes, str)):
            payment_id = int(payment_id, 16)
        elif not isinstance(payment_id, int):
            raise TypeError("payment_id must be either int or hexadecimal str or bytes")
        prefix = 54 if self.is_testnet() else 19
        data = bytes([prefix]) + self._decoded[1:65] + payment_id.to_bytes(8, byteorder='big')
        checksum = keccak_256(data).digest()[:4]
        return IntegratedAddress(base58.encode(hexlify(data + checksum)))

    def __repr__(self):
        return base58.encode(hexlify(self._decoded))

    def __eq__(self, other):
        if isinstance(other, Address):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other
        return super()


class IntegratedAddress(Address):
    def __init__(self, address):
        address = str(address)
        if len(address) != 106:
            raise ValueError("Integrated address must be 106 characters long, is %d" % len(address))
        self._decode(address)

    def get_payment_id(self):
        return hexlify(self._decoded[65:-4]).decode()

    def get_base_address(self):
        prefix = 53 if self.is_testnet() else 18
        data = bytes([prefix]) + self._decoded[1:65]
        checksum = keccak_256(data).digest()[:4]
        return Address(base58.encode(hexlify(data + checksum)))


def address(addr):
    addr = str(addr)
    if len(addr) == 95:
        return Address(addr)
    elif len(addr) == 106:
        return IntegratedAddress(addr)
    raise ValueError("Address must be either 95 or 106 characters long")