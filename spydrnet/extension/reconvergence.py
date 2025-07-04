import sys
import logging
import argparse
import networkx as nx
import spydrnet as sdn

# ------------------------- Flattening Utilities -------------------------

def is_black_box(instance):
    definition = instance.reference
    return len(definition.cables) == 0 and len(definition.children) == 0

def copy_instance(parent_instance, instance, new_instance):
    for key, value in instance.data.items():
        new_instance[key] = value
    new_instance['EDIF.identifier'] = parent_instance['EDIF.identifier'] + '_' + new_instance['EDIF.identifier']
    if '.NAME' in parent_instance:
        if '.NAME' in instance:
            new_instance['.NAME'] = parent_instance['.NAME'] + '/' + instance['.NAME']
        else:
            new_instance['.NAME'] = parent_instance['.NAME'] + '/' + instance['EDIF.identifier']
    else:
        if '.NAME' in instance:
            new_instance['.NAME'] = parent_instance['EDIF.identifier'] + '/' + instance['.NAME']
        else:
            new_instance['.NAME'] = parent_instance['EDIF.identifier'] + '/' + instance['EDIF.identifier']
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
    return created

# ------------------------- Reconvergence Logic -------------------------

def find_top_definition(netlist):
    defs = list(sdn.get_definitions(netlist))
    insts = list(sdn.get_instances(netlist, recursive=True))
    inst_defs = {inst.reference for inst in insts if inst.reference is not None}
    top_defs = [d for d in defs if d not in inst_defs]
    return top_defs[0] if top_defs else defs[0]

def detect_reconvergence(graph, labels):
    results = []
    for node in graph.nodes():
        succs = list(graph.successors(node))
        if len(succs) < 2:
            continue
        reachable_sets = [set(nx.descendants(graph, s)) for s in succs]
        node_count = {}
        for desc in reachable_sets:
            for n in desc:
                node_count[n] = node_count.get(n, 0) + 1
        reconv_nodes = [n for n, c in node_count.items() if c >= 2]
        if reconv_nodes:
            stem_label = labels.get(node, str(node))
            branch_labels = [labels.get(n, str(n)) for n in succs]
            reconv_labels = [labels.get(n, str(n)) for n in reconv_nodes]
            results.append((stem_label, branch_labels, reconv_labels))
    return results

# ------------------------- Main CLI Interface -------------------------

def main():
    parser = argparse.ArgumentParser(description="Detect reconvergent fanouts in Verilog netlist")
    parser.add_argument("input_netlist", help="Input Verilog file")
    parser.add_argument("output_file", help="Output .txt file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info(f"Parsing netlist: {args.input_netlist}")
    netlist = sdn.parse(args.input_netlist)
    top_def = find_top_definition(netlist)
    netlist.top_instance = sdn.instantiate(top_def)
    flatten_definition(top_def, top_definition=True)
    logging.info("Flattening completed.")

    G = top_def.get_connectivity_network()
    labels = nx.get_node_attributes(G, "label")
    logging.info(f"Graph has {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    results = detect_reconvergence(G, labels)
    logging.info(f"Detected {len(results)} reconvergent fanouts.")

    with open(args.output_file, "w") as f:
        for stem, branches, reconvs in results:
            f.write(f"Stem: {stem}\n")
            f.write(f"  Branches: {', '.join(branches)}\n")
            f.write(f"  Reconverges at: {', '.join(reconvs)}\n\n")

    logging.info(f"Results written to {args.output_file}")

if __name__ == "__main__":
    main()