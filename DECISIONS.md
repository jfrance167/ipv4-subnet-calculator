# Decisions

- Hold the approved IPv4-only, offline CLI scope; no services or third-party runtime dependencies.
- Use ipaddress for parsing and fixed-size integer arithmetic for endpoints/counts.
- Require explicit decimal CIDR prefixes, accept and explain host-bit normalization, and reject IPv6/hostnames/dotted masks.
- Use point-to-point `/31` and single-host `/32` conventions, with clear broadcast-field limitations.
- Keep the worker's draft as reviewed input. Correct its missing strict prefix validation, broad exception catch and stray language marker before use.
