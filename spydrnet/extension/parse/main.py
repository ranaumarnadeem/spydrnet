import spydrnet as sdn
import networkx as nx
from pathlib import Path

# Check if given instance is a black box
def is_black_box(instance):
    definition = instance.reference
    if len(definition.cables) != 0 or len(definition.children) != 0:
        return False
    return True

# Creates a copy of an instance
def copy_instance(parent_instance, instance, new_instance):
    for key, value in instance.data.items():
        new_instance[key] = value
    new_instance.name = f"{parent_instance.name}_{instance.name}"
    new_instance.reference = instance.reference

# Removes a newly created cable in favor of outside cable
def use_outside_cable(new_cable, old_cable, instance):
    wire = None
    for pin in old_cable.wires[0].pins:
        if pin in instance.pins:
            wire = instance.pins[pin].wire
            break
    if wire:
        for new_wire in new_cable.wires:
            for pin in new_wire.pins:
                new_wire.disconnect_pin(pin)
                wire.connect_pin(pin)
        new_cable.definition.remove_cable(new_cable)

# Remove instances that have been flattened
def clean_up(instance):
    for pin in instance.pins.values():
        if pin.wire:
            pin.wire.disconnect_pin(pin)
    instance.parent.remove_child(instance)

# Recursively flatten a given definition
def flatten_definition(definition, top_definition=False):
    children = definition.children.copy()
    created = []
    for child in children:
        leaf_grandchildren = []
        child_reference = child.reference
        grandchildren = child_reference.children.copy()
        instance_map = {}
        
        for grandchild in grandchildren:
            if not is_black_box(grandchild):
                leaf_grandchildren.extend(flatten_definition(child.reference))
            else:
                leaf_grandchildren.append(grandchild)
                
        for grandchild in leaf_grandchildren:
            new_instance = definition.create_child()
            copy_instance(child, grandchild, new_instance)
            instance_map[grandchild] = new_instance
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
                    if pin.instance in instance_map:
                        new_wire.connect_pin(instance_map[pin.instance].pins[pin.inner_pin])
            
            if name_cable:
                new_cable.name = f"{child.name}_{cable.name}"
            else:
                use_outside_cable(new_cable, cable, child)
                
        if not is_black_box(child):
            clean_up(child)
            
    return created

# Create graph representation from flattened netlist
def create_netlist_graph(netlist):
    G = nx.MultiDiGraph()
    top = netlist.top_instance.reference
    
    # Add all instances as nodes
    for instance in top.get_instances():
        G.add_node(instance.name, 
                   type="instance",
                   ref=instance,
                   primitive=is_black_box(instance))
    
    # Add primary ports
    for port in top.get_ports():
        port_name = port.name
        if port.direction == sdn.IN:
            G.add_node(f"INPUT:{port_name}", type="input_port")
        elif port.direction == sdn.OUT:
            G.add_node(f"OUTPUT:{port_name}", type="output_port")
        elif port.direction == sdn.INOUT:
            G.add_node(f"INOUT:{port_name}", type="inout_port")
    
    # Process all nets
    for net in top.get_pins():
        drivers = []
        receivers = []
        
        for pin in net.get_pins():
            # Handle both InnerPin (top-level ports) and OuterPin (instance pins)
            if isinstance(pin, sdn.InnerPin):
                # Top-level port
                port = pin.port
                if port.direction in {sdn.OUT, sdn.INOUT}:
                    drivers.append(f"INPUT:{port.name}" if port.direction == sdn.IN 
                                  else f"INOUT:{port.name}")
                if port.direction in {sdn.IN, sdn.INOUT}:
                    receivers.append(f"OUTPUT:{port.name}" if port.direction == sdn.OUT 
                                    else f"INOUT:{port.name}")
            else:  # OuterPin
                instance = pin.instance
                port = pin.inner_pin.port
                
                if port.direction in {sdn.OUT, sdn.INOUT}:
                    drivers.append(instance.name)
                if port.direction in {sdn.IN, sdn.INOUT}:
                    receivers.append(instance.name)
        
        # Add edges for all driver-receiver pairs
        for driver in drivers:
            for receiver in receivers:
                if driver != receiver:  # Avoid self-loops unless intentional
                    G.add_edge(driver, receiver, net=net.name)

    return G
# Main workflow
def process_netlist(input_file, output_file=None):
    # 1. Parse the netlist
    netlist = sdn.parse(input_file)
    
    # 2. Flatten the hierarchy
    top_def = netlist.top_instance.reference
    flatten_definition(top_def, top_definition=True)
    
    # 3. Create graph representation
    graph = create_netlist_graph(netlist)
    
    # 4. Optionally compose to output file
    if output_file:
        netlist.compose(output_file)
    
    return graph, netlist

# Usage
input_file = "serial_ALU.v"
output_file = "flattened_serial_ALU.v"

graph, flattened_netlist = process_netlist(input_file, output_file)
print(f"Created graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")