from . import address
from . import prio
from .transaction import PaymentManager


class Account(object):
    index = None

    def __init__(self, backend, index):
        self.index = index
        self._backend = backend
        self.incoming = PaymentManager(index, backend, 'in')
        self.outgoing = PaymentManager(index, backend, 'out')

    def balances(self):
        return self._backend.balances(account=self.index)

    def balance(self, unlocked=False):
        return self._backend.balances(account=self.index)[1 if unlocked else 0]

    def address(self):
        """
        Return account's main address.
        """
        return self._backend.addresses(account=self.index)[0]

    def addresses(self):
        return self._backend.addresses(account=self.index)

    def new_address(self, label=None):
        return self._backend.new_address(account=self.index, label=label)

    def transfer(self, address, amount,
            priority=prio.NORMAL, ringsize=5, payment_id=None, unlock_time=0,
            relay=True):
        return self._backend.transfer(
            [(address, amount)],
            priority,
            ringsize,
            payment_id,
            unlock_time,
            account=self.index,
            relay=relay)

    def transfer_multiple(self, destinations,
            priority=prio.NORMAL, ringsize=5, payment_id=None, unlock_time=0,
            relay=True):
        """
        destinations = [(address, amount), ...]
        """
        return self._backend.transfer(
            destinations,
            priority,
            ringsize,
            payment_id,
            unlock_time,
            account=self.index,
            relay=relay)
