# Requirements Meeter Output

## Zipsafe Decision
- **Result**: false
- **Reason**: Packages with data files — `boto3` contains JSON service resource definitions under `boto3/data/`; `botocore` contains JSON service models, endpoint rules, paginators, waiters, and a PEM certificate bundle under `botocore/data/` and `botocore/cacert.pem`. These non-Python files cannot be read from inside a zip archive at runtime.

## CLI Tools
None required. Analysis section "6. CLI Tool Dependencies" explicitly states no CLI tool dependencies.

## Python Dependencies
- `boto3==1.42.97` — Has data files (JSON service resource definitions in `boto3/data/`). Note: version 1.43.102 specified in analysis does not exist on PyPI; 1.42.97 is the latest available.
- `botocore==1.42.97` — Has data files (JSON service models, endpoint rules, paginators, waiters, cacert.pem in `botocore/data/`).
- `jmespath==1.1.0` — Pure Python.
- `python-dateutil==2.9.0.post0` — Pure Python. Version adjusted from 2.9.0 to 2.9.0.post0 as resolved by pip for boto3 1.42.97.
- `s3transfer==0.16.1` — Pure Python. Version adjusted from 0.19.2 to 0.16.1 as required by boto3 1.42.97 dependency constraints.
- `six==1.17.0` — Pure Python. Transitive dependency of python-dateutil; added explicitly for reproducibility.
- `tabulate==0.10.0` — Pure Python.

## Setup.py Changes
- VENDOR_FOLDER added: no (already present as a constant in the existing setup.py)
- data_files updated: no (setup.py already handles the `zip_safe: False` path and conditionally includes the vendor directory only if it exists; no CLI tools required, so no vendor binaries to bundle)
