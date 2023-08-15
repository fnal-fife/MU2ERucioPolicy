# MU2ERucioPolicy
This is the Rucio policy package for MU2E.

## How to use this policy package
* Make sure the directory containing the `MU2ERucioPolicy` directory is in the `PYTHONPATH` for the Rucio server.
* Set `package = MU2ERucioPolicy` in the `policy` section of the Rucio configuration file.

## Source files
* `__init__.py` - registers the SURL and LFN2PFN algorithms when the package is loaded.
* `lfn2pfn.py` - contains the MU2E lfn2pfn algorithm which queries the Metacat metadata service and constructs PFNs based on the metadata returned.
* `path_gen.py` - contains the MU2E SURL algorithm which currently queries the SAM metadata service to get required information on the file.
* `permission.py` - permission functions for the policy package.
* `schema.py` - schema functions and data for the policy package. Currently just a copy of the generic code with no MU2E-specific customisation.

## More Information
* https://rucio.cern.ch/documentation/operator/policy_packages
