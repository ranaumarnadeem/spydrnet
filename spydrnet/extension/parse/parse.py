import spydrnet as sdn
import argparse
from pathlib import Path

def is_black_box(instance):
    definition = instance.reference
    return not (definition.cables or definition.children)

def copy_instance(parent_instance, instance, new_instance):
    for key, value in instance.data.items():
        new_instance[key] = value

    new_instance['EDIF.identifier'] = parent_instance['EDIF.identifier'] + '_' + new_instance['EDIF.identifier']

    if '.NAME' in parent_instance:
        parent_name = parent_instance['.NAME']
    else:
        parent_name = parent_instance['EDIF.identifier']

    if '.NAME' in instance:
        child_name = instance['.NAME']
    else:
        child_name = instance['EDIF.identifier']

    new_instance['.NAME'] = f"{parent_name}/{child_name}"
    new_instance.reference = instance.reference

def use_outside_cable(new_cable, old_cable, instance):
    wire = None
    for pin in old_cable.wires[0].pins:
        if pin in instance.pins:
            wire = instance.pins[pin].wire
            break

    for new_wire in new_cable.wires:
        for pin in new_wire.pins:
            new_wire.disconnect_pin(pin)
            wire.connect_pin(pin)

    new_cable.definition.remove_cable(new_cable)

def clean_up(instance):
    for pin in instance.pins.values():
        pin.wire.disconnect_pin(pin)
    instance.parent.remove_child(instance)

def flatten_definition(definition, top_definition=False):
    children = definition.children.copy()
    created = []
    for child in children:
        leaf_grandchildren = []
        child_reference = child.reference
        grandchildren = child_reference.children.copy()
        map = {}

        if top_definition and not is_black_box(child):
            print("Flattening:", child['EDIF.identifier'])

        for grandchild in grandchildren:
            if not is_black_box(grandchild):
                leaf_grandchildren.extend(flatten_definition(child.reference))
            else:
                leaf_grandchildren.append(grandchild)

        for grandchild in leaf_grandchildren:
            new_instance = definition.create_child()
            copy_instance(child, grandchild, new_instance)
            map[grandchild] = new_instance
            created.append(new_instance)

        cables = child_reference.cables.copy()
        for cable in cables:
            name_cable = True
            new_cable = definition.create_cable()
            for wire in cable.wires:
                new_wire = new_cable.create_wire()
                for pin in wire.pins:
                    if isinstance(pin, sdn.InnerPin):
                        name_cable = False
                        continue
                    new_wire.connect_pin(map[pin.instance].pins[pin.inner_pin])

            if name_cable:
                new_cable['EDIF.identifier'] = child['EDIF.identifier'] + '_' + cable['EDIF.identifier']
                new_cable.name = new_cable['EDIF.identifier']
            else:
                use_outside_cable(new_cable, cable, child)

        if not is_black_box(child):
            clean_up(child)

        if top_definition and not is_black_box(child):
            print("Done flattening:", child['EDIF.identifier'])
    return created

def print_hierarchy(instance, indent=""):
    print(indent + instance.name)
    for child in instance.reference.children:
        print_hierarchy(child, indent + "   ")

def main():
    parser = argparse.ArgumentParser(description="SpyDrNet Netlist Flattener")
    parser.add_argument("-i", "--input", required=True, help="Input Verilog netlist file")
    parser.add_argument("-o", "--output", required=True, help="Output Verilog netlist file")
    args = parser.parse_args()

    netlist = sdn.parse(args.input)
    top_def = netlist.top_instance.reference

    print("\n📂 Hierarchy BEFORE Flattening:")
    print_hierarchy(netlist.top_instance)

    flatten_definition(top_def, top_definition=True)

    print("\n📂 Hierarchy AFTER Flattening:")
    print_hierarchy(netlist.top_instance)

    sdn.compose(netlist, args.output)
    print(f"\n✅ Flattened netlist saved to: {args.output}")

if __name__ == "__main__":
    main()
