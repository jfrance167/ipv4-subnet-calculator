# IPv4 Subnet Calculator

A small offline CLI that turns an IPv4 CIDR into a readable network summary. It uses Python's standard library and never connects to a network or enumerates host addresses.

## Run

Python 3.10 or later is required. From this directory:

```text
python subnet_calc.py 192.0.2.0/24
```

```text
Network:       192.0.2.0/24
Subnet mask:   255.255.255.0
Wildcard mask: 0.0.0.255
Broadcast:     192.0.2.255
First usable:  192.0.2.1
Last usable:   192.0.2.254
Usable count:  254
```

An input such as `192.0.2.73/24` is normalized to `192.0.2.0/24` with a note. Supply a dotted IPv4 address and a decimal prefix from 0 through 32. IPv6, hostnames, dotted masks, leading-zero prefixes and malformed inputs are rejected with exit status 2. Successful calculations exit 0.

For a `/31`, both addresses are counted as usable under point-to-point semantics. A `/32` contains one host. The broadcast field is the computed range endpoint; `/31` and `/32` do not have an operational subnet broadcast destination. Counts describe address arithmetic, not whether addresses are globally routable or suitable for a particular deployment.

## Check

```text
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python -m bandit subnet_calc.py
```

Tests use hand-calculated examples, small-network boundaries, invalid inputs, CLI exit status and a bounded `/0` command. Bandit is an optional development scanner; it is not a runtime dependency. See `VALIDATION.md` for the results actually run.

## Scope and learning

The first version covers IPv4 calculations and terminal output. It does not inspect the local machine, change interfaces, scan hosts, plan VLSM allocations or verify live connectivity. `/0` uses the same constant-space arithmetic as a `/24`.

The project demonstrates CIDR normalization, network and wildcard masks, usable endpoint conventions, clear input errors and command-line testing. `LEARNING.md` records the implementation decisions.

## Attribution and assistance

Python's `ipaddress` module performs address parsing and network arithmetic; no third-party source was vendored. A bounded public/synthetic draft was produced through OmniRoute using OpenRouter's North Mini Code free route. Codex reviewed it, corrected the CIDR validation and exception handling, implemented the final CLI and wrote the boundary tests. The raw draft and sanitized receipt are retained in local development records and are excluded from this public repository.

Original project contributions are offered under the [MIT license](LICENSE). Python and development tools retain their own licenses. [GitHub Actions](https://github.com/jfrance167/ipv4-subnet-calculator/actions) runs the test matrix, Bandit and CodeQL; see the latest run results before relying on a revision.
