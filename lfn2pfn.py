#!/usr/bin/env python
import rucio
import collections
import os.path
import hashlib

FILE_FAMILIES = {
    "raw":{"prod":"phy-raw","user":"phy-raw","type":"data"},
    "rec":{"prod":"phy-rec","user":"usr-dat","type":"data"},
    "ntd":{"prod":"phy-ntd","user":"usr-dat","type":"data"},
    "ext":{"prod":None,     "user":"usr-dat","type":"data"},
    "rex":{"prod":None,     "user":"usr-dat","type":"data"},
    "xnt":{"prod":None,     "user":"usr-dat","type":"data"},
    "cnf":{"prod":"phy-etc","user":"usr-etc","type":"common"},
    "sim":{"prod":"phy-sim","user":"usr-sim","type":"mc"},
    "dts":{"prod":"phy-sim","user":"usr-sim","type":"mc"},
    "mix":{"prod":"phy-sim","user":"usr-sim","type":"mc"},
    "dig":{"prod":"phy-sim","user":"usr-sim","type":"mc"},
    "mcs":{"prod":"phy-sim","user":"usr-sim","type":"mc"},
    "nts":{"prod":"phy-nts","user":"usr-nts","type":"mc"},
    "log":{"prod":"phy-etc","user":"usr-etc","type":"common"},
    "bck":{"prod":"phy-etc","user":"usr-etc","type":"common"},
    "etc":{"prod":"phy-etc","user":"usr-etc","type":"common"}}

Filename = collections.namedtuple('Filename',['data_tier', 'owner', 'description', 'configuration', 'sequencer', 'file_format'])

def lfn2pfn_MU2E(scope, name, rse, rse_attrs, protocol_attrs):
    # Mu2e Filename Schema
    # ====================
    # data_tier.owner.description.configuration.sequencer.file_format
    # sim.mu2e.beam_g4s1_dsregion.0429a.123456_12345678.art
    # ====================
    from rucio.common.types import InternalScope
    from rucio.rse import rsemanager
    from rucio.common.exception import DataIdentifierNotFound

    # check to see if PFN is already cached in Rucio's metadata system
    didclient = None
    didmd = {}
    internal_scope = InternalScope(scope)
    if getattr(rsemanager, 'CLIENT_MODE', None):
        from rucio.client.didclient import DIDClient
        didclient = DIDClient()
        try:
            didmd = didclient.get_metadata(internal_scope, name)
        except:
            pass
    if getattr(rsemanager, 'SERVER_MODE', None):
        from rucio.core.did import get_metadata
        try:
            didmd = get_metadata(internal_scope, name)
        except:
            pass

    # if it is, just return it
    md_key = 'PFN_' + rse
    if md_key in didmd:
        return didmd[md_key]

    fn = Filename(*name.split('.'))
    ff = get_file_family(fn)
    hs = hashlib.sha256(name.encode('utf-8')).hexdigest()

    pfn = os.path.join(
        ff,
        fn.data_tier,
        fn.owner, 
        fn.description,
        fn.configuration,
        fn.file_format,
        hs[0:2],
        hs[2:4],
        name
    )

    # Cache the PFN in the Rucio metadata for next time
    if getattr(rsemanager, 'CLIENT_MODE', None):
        try:
            didclient.set_metadata(internal_scope, name, md_key, pfn)
        except:
            pass
    if getattr(rsemanager, 'SERVER_MODE', None):
        from rucio.core.did import set_metadata
        try:
            set_metadata(internal_scope, name, md_key, pfn)
        except:
            pass

    return pfn

def get_file_family(fn):
    user_type = "prod" if fn.owner == 'mu2e' else 'user'
    return FILE_FAMILIES[fn.data_tier][user_type]