import spydrnet as sdn
import networkx as nx
import json
import argparse

def build_dag(netlist):
    dag = nx.DiGraph()
    instance_map = {}
    top_def = netlist.top_instance.reference

    # Add all instances in top definition
    for instance in top_def.children:
        inst_name = instance.name or instance.reference.name
        dag.add_node(inst_name)
        instance_map[instance] = inst_name

    # Create edges based on output to input wires
    for src_inst, src_name in instance_map.items():
        for pin in src_inst.pins:
            if pin.inner_pin and pin.inner_pin.port.direction in (sdn.OUT, sdn.INOUT):
                wire = pin.wire
                if wire:
                    for connected_pin in wire.pins:
                        if isinstance(connected_pin, sdn.OuterPin):
                            dst_inst = connected_pin.instance
                            if dst_inst in instance_map and dst_inst != src_inst:
                                dag.add_edge(src_name, instance_map[dst_inst])

    return dag

def main():
    parser = argparse.ArgumentParser(description="Generate DAG from flattened netlist")
    parser.add_argument("input", help="Input flattened Verilog netlist (.v)")
    parser.add_argument("output", help="Output DAG in JSON format")
    args = parser.parse_args()

    netlist = sdn.parse(args.input)
    dag = build_dag(netlist)

    dag_json = nx.readwrite.json_graph.adjacency_data(dag)

    with open(args.output, "w") as f:
        json.dump(dag_json, f, indent=2)

    print(f"DAG written to {args.output}")
    print(f"Nodes: {dag.number_of_nodes()}, Edges: {dag.number_of_edges()}")

if __name__ == "__main__":
    main()
