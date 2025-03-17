from .path_gen import construct_surl_mu2e
from .lfn2pfn import lfn2pfn_MU2E

SUPPORTED_VERSION=[">=36.0"]

def get_algorithms():
    return { 'lfn2pfn': { 'MU2E': lfn2pfn_MU2E }, 'surl': { 'mu2e': construct_surl_mu2e } }
