# Validation

Verified locally on Windows with Python 3.13.7. Publication is authorized; fresh remote results are tracked in GitHub Actions.

| Check | Command or method | Result |
| --- | --- | --- |
| Normal tests | `python -m unittest discover -s tests -v` | PASS: 12 tests, including 16 invalid-input subcases |
| Optimized tests | `python -O -m unittest discover -s tests -v` | PASS: the same 12 tests |
| Security scanner | `python -m bandit subnet_calc.py` | PASS: zero findings, zero skips |
| Syntax | `python -m py_compile subnet_calc.py tests/test_subnet_calc.py` | PASS |
| Example | `python subnet_calc.py 192.0.2.0/24` | PASS: matches the README output |
| Large subnet | CLI `/0` test with a five-second subprocess limit | PASS: 4,294,967,294 usable addresses without enumeration |
| Workflow YAML | Safe-load both workflow files and verify triggers, minimum permissions, action pins and checkout settings | PASS after quoting the pip command containing a YAML colon |
| ECC self-review | Source, callers, tests and actual staged diff | PASS: the workflow quoting issue was corrected; no remaining actionable findings |
| Remote CI / CodeQL | Published workflows | Verification pending on the first published source revision |
| Python 3.10 and Ubuntu | Prepared CI matrix | NOT RUN locally |

The calculator has no third-party runtime dependencies. Bandit is an optional development tool pinned in `requirements-security.txt`; development-tool transitive dependencies are not hash-locked. No suppression was added to the calculator scanner.

The worker draft was reviewed before execution or adoption. Codex removed its stray language marker, required an explicit decimal CIDR prefix, replaced a broad exception catch, preserved bounded arithmetic, and added independent test oracles. The sanitized receipt reports 579 input tokens and 666 output tokens (1,245 total), zero reasoning tokens, HTTP 200, and a completed response. Fresh free-price and privacy checks passed. These are actual worker counts, not measured savings.

All results are bounded verification of this local version, not a claim that every future modification or network deployment is safe. No network configuration is inspected or changed.
