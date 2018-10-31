# -*- coding: utf-8 -*-

from datahandling import append_pings, SmokeyTransfer
from globalvars import GlobalVars
import pytest


# noinspection PyMissingTypeHints
def test_append_pings():
    assert append_pings("foo", ["user1", "some user"]) == "foo (@user1 @someuser)"
    assert append_pings("foo", [u"Doorknob 冰"]) == u"foo (@Doorknob冰)"


def test_smokey_transfer(monkeypatch):
    mp = monkeypatch
    blacklisted_users = {1: (2, 3), 4: (5, 6)}
    mp.setattr(GlobalVars, 'blacklisted_users', blacklisted_users)

    s = SmokeyTransfer.dump()
    assert s.startswith(SmokeyTransfer.HEADER + "\n\n")
    assert s.endswith("\n\n" + SmokeyTransfer.ENDING)
    print(s)
    SmokeyTransfer.load(s, False)
    assert GlobalVars.blacklisted_users == blacklisted_users

    with pytest.raises(ValueError) as e:
        SmokeyTransfer.load("hahaha")
    assert "invalid data" in str(e).lower()

    with pytest.raises(ValueError):
        SmokeyTransfer.load(SmokeyTransfer.HEADER + "\nmmmmmm\n" + SmokeyTransfer.ENDING)
