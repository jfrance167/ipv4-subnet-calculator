"""Native offline desktop window for the existing IPv4 calculator."""

import tkinter as tk
from tkinter import ttk

from subnet_calc import calculate_subnet


class SubnetCalculator:
    """Keep input, validation feedback and readonly results in one window."""

    def __init__(self, root: tk.Tk):
        root.title("IPv4 Subnet Calculator")
        root.geometry("620x570")
        root.minsize(560, 530)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame = ttk.Frame(root, padding=24)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="IPv4 Subnet Calculator",
                  font="TkHeadingFont").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(frame, text="Enter an address and prefix. All calculations stay offline.").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(6, 20))
        self.address = tk.StringVar(root, value="192.168.1.73")
        self.prefix = tk.StringVar(root, value="24")
        ttk.Label(frame, text="IPv4 address").grid(row=2, column=0, sticky="w", padx=(0, 16))
        self.address_entry = ttk.Entry(frame, textvariable=self.address)
        self.address_entry.grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Label(frame, text="Prefix (0–32)").grid(row=3, column=0, sticky="w")
        self.prefix_entry = ttk.Entry(frame, textvariable=self.prefix, width=8)
        self.prefix_entry.grid(row=3, column=1, sticky="w", pady=4)
        self.calculate_button = ttk.Button(frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=4, column=1, sticky="w", pady=(10, 16))
        self.status = tk.StringVar(root, value="Ready. Press Calculate or Enter.")
        self.status_label = ttk.Label(frame, textvariable=self.status, wraplength=510)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self.results = {}
        labels = (("Network", "network"), ("Subnet mask", "subnet_mask"),
                  ("Wildcard mask", "wildcard_mask"), ("Broadcast / range end", "broadcast"),
                  ("First usable", "first_usable"), ("Last usable", "last_usable"),
                  ("Usable addresses", "usable_count"))
        for row, (label, key) in enumerate(labels, start=6):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 16))
            value = tk.StringVar(root)
            self.results[key] = value
            ttk.Entry(frame, textvariable=value, state="readonly").grid(
                row=row, column=1, sticky="ew", pady=3)
        self.note = tk.StringVar(root)
        ttk.Label(frame, textvariable=self.note, wraplength=510).grid(
            row=13, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        self.address.trace_add("write", self.input_changed)
        self.prefix.trace_add("write", self.input_changed)
        root.bind("<Return>", self.calculate)
        self.address_entry.focus_set()

    def clear_results(self):
        for value in self.results.values():
            value.set("")
        self.note.set("")

    def input_changed(self, *_args):
        self.clear_results()
        self.status.set("Input changed. Press Calculate or Enter.")

    def calculate(self, _event=None):
        self.clear_results()
        try:
            # Reuse the CLI's bounded, strict validation; never convert arbitrary input to int.
            data = calculate_subnet(f"{self.address.get().strip()}/{self.prefix.get().strip()}")
        except ValueError:
            self.status.set("Invalid input. Enter an IPv4 address and a prefix from 0 to 32 (for example, 24).")
            return
        for key, value in self.results.items():
            value.set(f"{data['network']}/{data['prefix_length']}" if key == "network" else str(data[key]))
        notes = []
        if data["normalized"]:
            notes.append("Host bits were normalized to the network address.")
        if data["prefix_length"] == 31:
            notes.append("/31 assumes a point-to-point link: both addresses are usable. The range end is not a broadcast destination.")
        elif data["prefix_length"] == 32:
            notes.append("/32 represents one host. There is no subnet broadcast destination.")
        self.note.set(" ".join(notes))
        self.status.set("Calculated. Select a result to copy it.")


def main():
    root = tk.Tk()
    SubnetCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
