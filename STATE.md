# State

The GUI update adds separate address/prefix fields, Calculate/Enter, selectable readonly results, input errors and prefix notes. Local tests pass with a required Tk display. See the update PR's current checks for remote results; the paragraphs below describe the earlier CLI release.

Local version 1 is implemented and verified. Twelve tests pass normally and under optimized Python; Bandit reports zero findings. Syntax, sample output, workflow policy and the staged diff were checked. See VALIDATION.md for the exact limits.

Published at https://github.com/jfrance167/ipv4-subnet-calculator with Jake's explicit authorization. The first published source revision passes the Windows/Ubuntu Python 3.10/3.13 test matrix, Bandit and CodeQL. Local development receipts and knowledge records are excluded from publication. Follow the repository's required checks for future changes; this is an educational offline CLI, not a network scanner or deployment tool.
