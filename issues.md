# Lab 5 — Static Analysis Issue Log

**Analyzed file:** `vehicle_service.py`

Line numbers in the first column below refer to the original repository version before fixes. Analyzer line numbers can vary if the starting file has changed.

| Issue | Type / tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command built from input | Security — Bandit | 61 | `subprocess.call(..., shell=True)` passed a constructed command to a shell, creating command-injection risk. | Removed shell execution and used `pathlib.Path` plus `shutil.copy2`; check source and destination before copying. |
| Hard-coded password | Security — manual review | 8 | A demo administrator password was stored directly in source code and was not used by the application. | Removed the unused credential from source. Real credentials should be stored in a secret manager or environment configuration. |
| MD5 for job-card identifier | Security / quality — Bandit review | 39 | MD5 is not appropriate where a collision-resistant digest is desired. | Replaced MD5 with SHA-256. The value is still only an identifier, not an authentication token. |
| Mutable default argument | Bug / quality — Pylint | 12 | `history=[]` was shared between calls, so unrelated calls could accidentally share state. | Changed the default to `None` and creates a new list inside the function. |
| Broad exception handler | Bug / quality — Pylint | 23 | `except Exception` caught unrelated errors and obscured the expected missing-record case. | Replaced exception-driven lookup with `service_records.get()` and a specific no-records result. |
| Missing input validation | Robustness — manual review | 12, 38 | Empty vehicle identifiers and unknown service types could create misleading records or zero-cost jobs. | Added checks for non-empty vehicle identifiers and supported service types; invalid input raises `ValueError`. |
| Implicit text encoding | Portability — Pylint | 50 | The JSON save file relied on the platform's default text encoding. | Opened the file with explicit UTF-8 encoding. |
| Style and naming | Style — Flake8/Pylint | Throughout | Mixed naming styles, inconsistent spacing, and manual accumulation made the code harder to read. | Applied snake_case function names, consistent spacing, f-strings for printed output, a `sum()` expression, docstrings, and formatted logging. |
| Script runs on import | Maintainability — manual review | 80 | Calling `main()` unconditionally made importing functions execute the demonstration and write a file. | Put the entry point behind `if __name__ == "__main__":`. |

## Verification checklist

- [ ] Run Pylint, Bandit, and Flake8 on the original file and save baseline reports.
- [ ] Run all three tools on the fixed `vehicle_service.py` and save final reports.
- [ ] Confirm the fixed file has no Flake8 output and review any remaining Pylint/Bandit findings rather than suppressing them blindly.
- [ ] Run `python -m unittest -v` and `python -m py_compile vehicle_service.py`.
