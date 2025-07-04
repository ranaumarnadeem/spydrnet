import spydrnet as sdn
import networkx as nx
import json
import argparse

def dfs_traverse(graph, start_node, visited=None, depth=0):
    """
    Perform depth-first traversal on the graph starting from start_node.
    """
    if visited is None:
        visited = set()

    try:
        if start_node in visited:
            return visited

        print("  " * depth + f"Visiting: {start_node}")
        visited.add(start_node)

        for neighbor in graph.get(start_node, []):
            dfs_traverse(graph, neighbor, visited, depth + 1)

    except Exception as e:
        print(f"[ERROR] DFS failed at node '{start_node}': {str(e)}")

    return visited


def load_dag_from_json(filepath):
    """
    Load DAG from JSON and return an adjacency dictionary.
    """
    try:
        with open(filepath, "r") as f:
            dag_data = json.load(f)

        graph = {}
        for node, neighbors in zip(dag_data["nodes"], dag_data["adjacency"]):
            node_id = node["id"]
            graph[node_id] = [edge["id"] for edge in neighbors]

        print(f"[INFO] Loaded DAG with {len(graph)} nodes.")
        return graph

    except FileNotFoundError:
        print(f"[ERROR] File '{filepath}' not found.")
        return {}

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {str(e)}")
        return {}

    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return {}


def save_output(visited_nodes, filename="dfs_output.txt"):
    """
    Save the list of visited nodes to a file.
    """
    try:
        with open(filename, "w") as f:
            for node in sorted(visited_nodes):  # Optional: sorted order
                f.write(node + "\n")
        print(f"[INFO] DFS result written to '{filename}'.")

    except Exception as e:
        print(f"[ERROR] Could not write output file: {str(e)}")


if __name__ == "__main__":
    # === Configuration ===
    json_file = "dag.json"       # Change to your DAG file
    start_node = "zero_reg"      # Change to your desired root

    # === Run DFS ===
    graph = load_dag_from_json(json_file)

    if graph and start_node in graph:
        visited = dfs_traverse(graph, start_node)
        save_output(visited)
    else:
        print(f"[ERROR] Start node '{start_node}' not found in the graph.")