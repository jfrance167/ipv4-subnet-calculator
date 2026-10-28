# Validation

## Desktop GUI update

PASS locally on Windows / Python 3.13.7: 17 tests normally and under optimized Python, with all Tk widget tests executed; Bandit scans the CLI, GUI and .pyw entry point with zero findings and zero skips. A visible-window check confirmed the sample 192.168.1.73/24 calculation.

ECC self-review covers new GUI/launcher/test files, unchanged shared parser and the task diff. Validation uses the existing bounded parser, clears stale results and notes, and keeps imports free of window creation. No remaining actionable findings. CI now requires a working display and runs GUI tests under Xvfb on Ubuntu, alongside Windows; check the update PR for remote outcomes. Required check names, action pins, permissions and protections are preserved.

The GUI's reviewed OmniRoute draft used 551 input and 1,109 output tokens (1,660 total), after fresh zero-price/privacy checks. Codex removed duplicate integer validation, added resize weights and stale-result handling, and corrected contextual prefix notes. Draft/receipt files remain local. No further worker request was needed to prepare publication.

## Earlier CLI release

Verified locally on Windows with Python 3.13.7 and through the published GitHub Actions workflows. The initial published source revision `dd309cd662e51285c358e2892dfe5428f09b9fda` passes the remote matrix and security checks; subsequent revisions have their own check results in GitHub Actions.

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
| Remote CI / CodeQL | Published workflows | PASS: tests, Bandit and CodeQL on the initial published source revision |
| Windows/Ubuntu, Python 3.10/3.13 | GitHub-hosted matrix | PASS: all four combinations; Python 3.10/Ubuntu were not run locally |

The calculator has no third-party runtime dependencies. Bandit is an optional development tool pinned in `requirements-security.txt`; development-tool transitive dependencies are not hash-locked. No suppression was added to the calculator scanner.

The worker draft was reviewed before execution or adoption. Codex removed its stray language marker, required an explicit decimal CIDR prefix, replaced a broad exception catch, preserved bounded arithmetic, and added independent test oracles. The sanitized receipt reports 579 input tokens and 666 output tokens (1,245 total), zero reasoning tokens, HTTP 200, and a completed response. Fresh free-price and privacy checks passed. These are actual worker counts, not measured savings.

All results are bounded verification of this local version, not a claim that every future modification or network deployment is safe. No network configuration is inspected or changed.
