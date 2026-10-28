# IPv4 Subnet Calculator

A small offline IPv4 calculator with a desktop window and a command-line interface. It uses Python's standard library and never connects to a network or enumerates host addresses.

## Run

Python 3.10 or later is required. The desktop window also requires Tkinter, included with the standard Windows Python installer.

### Desktop window

On Windows, double-click **subnet_gui.pyw** after downloading or cloning the whole repository. Keep it beside subnet_gui.py and subnet_calc.py. If Windows asks which program to use, choose Python's windowed launcher; Python must have its .pyw association installed.

Enter an IPv4 address, such as **192.168.1.73**, and a prefix, such as **24**, then click **Calculate** or press **Enter**. Results are selectable for copying. Editing either input clears the old results. Invalid inputs show an explanation in the window.

You can also launch the same window from a terminal:

```text
python subnet_gui.py
```

On Linux, Tkinter may need to be installed separately through the operating system's package manager, and a graphical display is required. No additional Python packages are needed to run the calculator.

### Command line

From this directory:

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
python -m bandit subnet_calc.py subnet_gui.py subnet_gui.pyw
```

Tests use hand-calculated examples, small-network boundaries, invalid inputs, CLI exit status and a bounded `/0` command. Widget tests check the Calculate button, normalization, validation errors, clearing stale results and special-prefix notes. Local widget tests explicitly skip when no graphical display is available; CI requires them to run and uses Xvfb on Ubuntu. Bandit is an optional development scanner; it is not a runtime dependency. See `VALIDATION.md` for the results actually run.

## Scope and learning

The calculator covers IPv4 calculations through a desktop window and terminal output. It does not inspect the local machine, change interfaces, scan hosts, plan VLSM allocations or verify live connectivity. `/0` uses the same constant-space arithmetic as a `/24`.

The project demonstrates CIDR normalization, network and wildcard masks, usable endpoint conventions, clear input errors and command-line testing. `LEARNING.md` records the implementation decisions.

## Attribution and assistance

Python's `ipaddress` module performs address parsing and network arithmetic; no third-party source was vendored. A bounded public/synthetic draft was produced through OmniRoute using OpenRouter's North Mini Code free route. Codex reviewed it, corrected the CIDR validation and exception handling, implemented the final CLI and wrote the boundary tests. The raw draft and sanitized receipt are retained in local development records and are excluded from this public repository.

Original project contributions are offered under the [MIT license](LICENSE). Python and development tools retain their own licenses. [GitHub Actions](https://github.com/jfrance167/ipv4-subnet-calculator/actions) runs the test matrix, Bandit and CodeQL; see the latest run results before relying on a revision.
