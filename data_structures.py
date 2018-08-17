"""
Data structures for my Gadget frontend.
Adapted from https://mail.python.org/mm3/archives/list/yt-users@python.org/
message/NXCC32FF5IW7DB2PGW2QCLHKH62WLCLJ/
"""

from yt.frontends.gadget.data_structures import \
    GadgetDataset

from .fields import \
    MyGadgetFieldInfo

class MyGadgetDataset(GadgetDataset):
    _field_info_class = MyGadgetFieldInfo
