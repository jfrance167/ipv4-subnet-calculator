# Decisions

- Keep IPv4 calculations offline with both CLI and native Tkinter interfaces; no services or third-party runtime dependencies.
- Reuse calculate_subnet for both interfaces. Clear stale results when inputs change, and show validation errors beside the inputs.
- Publish a portable .pyw entry point; keep the machine-specific Windows shortcut local.
- Require a working Tk display in CI, using Xvfb on Ubuntu; preserve the existing required check names.
- Use ipaddress for parsing and fixed-size integer arithmetic for endpoints/counts.
- Require explicit decimal CIDR prefixes, accept and explain host-bit normalization, and reject IPv6/hostnames/dotted masks.
- Use point-to-point `/31` and single-host `/32` conventions, with clear broadcast-field limitations.
- Keep the worker's draft as reviewed input. Correct its missing strict prefix validation, broad exception catch and stray language marker before use.
