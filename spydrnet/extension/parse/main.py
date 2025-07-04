import spydrnet as sdn
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="SpyDrNet Genus Netlist Parser")
    parser.add_argument("-i", "--input", required=True, help="Input Verilog netlist file")
    parser.add_argument("-o", "--output", required=True, help="Output Verilog file")
    return parser.parse_args()

def print_hierarchy(instance, indent=""):
    print(indent + instance.name)
    for child in instance.reference.children:
        print_hierarchy(child, indent + "   ")

def main():
    args = parse_args()

    # Parse Genus netlist (Verilog)
    netlist = sdn.parse(args.input)

    print("\n📦 Top-Level Module:", netlist.top_instance.name)
    print("\n📂 Hierarchy:")
    print_hierarchy(netlist.top_instance)

    # Compose output Verilog netlist
    sdn.compose(netlist, args.output)
    print(f"\n✅ Netlist written to: {args.output}")

if __name__ == "__main__":
    main()
