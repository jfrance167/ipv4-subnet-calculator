"""Offline IPv4 subnet summaries using only Python's standard library."""

from __future__ import annotations

import argparse
import ipaddress
import re
from collections.abc import Sequence


def calculate_subnet(cidr: str) -> dict[str, str | int | bool]:
    """Return a bounded IPv4 summary; accept host bits, reject non-CIDR masks."""
    error = "enter an IPv4 address with a decimal CIDR prefix from 0 through 32"
    if not isinstance(cidr, str) or len(cidr) > 64 or cidr.count("/") != 1:
        raise ValueError(error)
    address, prefix = cidr.split("/")
    if re.fullmatch(r"(?:[0-9]|[12][0-9]|3[0-2])", prefix) is None:
        raise ValueError(error)
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        original_address = ipaddress.IPv4Address(address)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as exc:
        raise ValueError(error) from exc

    start, end = int(network.network_address), int(network.broadcast_address)
    if network.prefixlen >= 31:
        first, last, count = start, end, network.num_addresses
    else:
        first, last, count = start + 1, end - 1, network.num_addresses - 2
    return {
        "network": str(network.network_address),
        "prefix_length": network.prefixlen,
        "subnet_mask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "broadcast": str(network.broadcast_address),
        "first_usable": str(ipaddress.IPv4Address(first)),
        "last_usable": str(ipaddress.IPv4Address(last)),
        "usable_count": count,
        "normalized": original_address != network.network_address,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cidr", help="IPv4 CIDR, for example 192.0.2.0/24")
    args = parser.parse_args(argv)
    try:
        data = calculate_subnet(args.cidr)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Network:       {data['network']}/{data['prefix_length']}")
    for label, key in (("Subnet mask", "subnet_mask"), ("Wildcard mask", "wildcard_mask"),
                       ("Broadcast", "broadcast"), ("First usable", "first_usable"),
                       ("Last usable", "last_usable"), ("Usable count", "usable_count")):
        print(f"{label + ':':<15}{data[key]}")
    if data["normalized"]:
        print("Note: host bits were normalized to the network address.")
    if data["prefix_length"] == 31:
        print("Note: /31 assumes a point-to-point link; both addresses are usable.")
        print("The displayed broadcast value is the range end, not a broadcast destination.")
    elif data["prefix_length"] == 32:
        print("Note: /32 represents one host; there is no subnet broadcast destination.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
