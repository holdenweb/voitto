#!/usr/bin/env python
# encoding: utf-8
# vim: shiftwidth=4 expandtab


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict
from tappio import loadf, dumpf
import six
from six.moves import map


ONLY=True


def flatten_accounts(accounts):
    flat_accounts = dict()

    for branch in accounts:
        _flatten_accounts(branch, flat_accounts)

    return flat_accounts


def _flatten_accounts(account, accounts):
    accounts[account.number] = account

    for subaccount in account.subaccounts:
        _flatten_accounts(subaccount, accounts)


def missing_accounts(*input_filenames):
    input_filenames = set(input_filenames)

    documents = ((filename, loadf(filename)) for filename in input_filenames)
    flat_accounts = dict((filename, flatten_accounts(document.accounts)) for (filename, document) in documents)

    all_accounts = dict()
    list(map(all_accounts.update, six.itervalues(flat_accounts)))
    
    havity = defaultdict(set)
    for account_num, account in six.iteritems(all_accounts):
        for filename, accounts in six.iteritems(flat_accounts):
            if account_num in accounts:
                havity[account_num].add(filename)

    for account_num, filenames in six.iteritems(havity):
        fmt_filenames = " ".join(filenames)

        if filenames == input_filenames:
            if not ONLY:
                print("{account_num}: ALL  {fmt_filenames}".format(**locals()))
        else:
            print("{account_num}: ONLY {fmt_filenames}".format(**locals()))
            

def main():
    from sys import argv
    missing_accounts(*argv[1:])


if __name__ == "__main__":
    main()
