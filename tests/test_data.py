import pytest

def channel_list_test(userID):
    """add user"""
    assert channel_list_test(1) == 1
    assert channel_list_test(2) == 2
    """remove userID(1) from channel 1 add to channel 2"""
    assert channel_list_test(1) == 2
    """raises exception error"""