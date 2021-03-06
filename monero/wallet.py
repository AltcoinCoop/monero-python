from . import address
from . import prio
from . import account
from .transaction import Payment, PaymentManager

class Wallet(object):
    accounts = None

    def __init__(self, backend):
        self._backend = backend
        self.incoming = PaymentManager(0, backend, 'in')
        self.outgoing = PaymentManager(0, backend, 'out')
        self.refresh()

    def refresh(self):
        self.accounts = self.accounts or []
        idx = 0
        for _acc in self._backend.accounts():
            try:
                if self.accounts[idx]:
                    continue
            except IndexError:
                pass
            self.accounts.append(_acc)
            idx += 1

    def height(self):
        """
        Returns the height of the wallet.
        """
        return self._backend.height()

    def spend_key(self):
        """
        Returns private spend key.
        """
        return self._backend.spend_key()

    def view_key(self):
        """
        Returns private view key.
        """
        return self._backend.view_key()

    def seed(self):
        """
        Returns word seed.
        """
        return self._backend.seed()

    def new_account(self, label=None):
        acc, addr = self._backend.new_account(label=label)
        assert acc.index == len(self.accounts)
        self.accounts.append(acc)
        return acc

    def confirmations(self, txn_or_pmt):
        if isinstance(txn_or_pmt, Payment):
            txn = txn_or_pmt.transaction
        else:
            txn = txn_or_pmt
        try:
            return max(0, self.height() - txn.height)
        except TypeError:
            return 0

    # Following methods operate on default account (index=0)
    def balances(self):
        return self.accounts[0].balances()

    def balance(self, unlocked=False):
        return self.accounts[0].balance(unlocked=unlocked)

    def address(self):
        return self.accounts[0].addresses()[0]

    def addresses(self):
        return self.accounts[0].addresses()

    def new_address(self, label=None):
        return self.accounts[0].new_address(label=label)

    def transfer(self, address, amount,
            priority=prio.NORMAL, ringsize=5, payment_id=None, unlock_time=0,
            relay=True):
        return self.accounts[0].transfer(
                address,
                amount,
                priority=priority,
                ringsize=ringsize,
                payment_id=None,
                unlock_time=unlock_time,
                relay=relay)

    def transfer_multiple(self, destinations,
            priority=prio.NORMAL, ringsize=5, payment_id=None, unlock_time=0,
            relay=True):
        """
        destinations = [(address, amount), ...]
        """
        return self.accounts[0].transfer_multiple(
                destinations,
                priority=priority,
                ringsize=ringsize,
                payment_id=None,
                unlock_time=unlock_time,
                relay=relay)
