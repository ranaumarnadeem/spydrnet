import spydrnet as sdn
import networkx as nx
import json
import argparse
from collections import defaultdict, deque

def dfs_traverse(graph, start_node, visited=None, depth=0, all_paths=None, current_path=None):
    if visited is None:
        visited = set()
    if all_paths is None:
        all_paths = defaultdict(list)
    if current_path is None:
        current_path = []

    try:
        if start_node in visited:
            return visited, all_paths

        print("  " * depth + f"Visiting: {start_node}")
        visited.add(start_node)
        current_path.append(start_node)

        all_paths[start_node].append(list(current_path))

        for neighbor in graph.get(start_node, []):
            dfs_traverse(graph, neighbor, visited, depth + 1, all_paths, current_path[:])

    except Exception as e:
        print(f"[ERROR] DFS failed at node '{start_node}': {str(e)}")

    return visited, all_paths

def load_dag_from_json(filepath):
    try:
        with open(filepath, "r") as f:
            dag_data = json.load(f)

        graph = {}
        all_nodes = []
        for node, neighbors in zip(dag_data["nodes"], dag_data["adjacency"]):
            node_id = node["id"]
            graph[node_id] = [edge["id"] for edge in neighbors]
            all_nodes.append(node_id)

        print(f"[INFO] Loaded DAG with {len(graph)} nodes.")
        return graph, all_nodes

    except FileNotFoundError:
        print(f"[ERROR] File '{filepath}' not found.")
        return {}, []

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {str(e)}")
        return {}, []

    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return {}, []

def save_output(visited_nodes, filename="dfs_output.txt"):
    try:
        with open(filename, "w") as f:
            for node in sorted(visited_nodes):
                f.write(node + "\n")
        print(f"[INFO] DFS result written to '{filename}'.")
    except Exception as e:
        print(f"[ERROR] Could not write output file: {str(e)}")

def save_unvisited_nodes(all_nodes, visited_nodes, filename="unvisited_nodes.txt"):
    try:
        unvisited = set(all_nodes) - set(visited_nodes)
        with open(filename, "w") as f:
            for node in sorted(unvisited):
                f.write(node + "\n")
        print(f"[INFO] Unvisited nodes written to '{filename}'.")
    except Exception as e:
        print(f"[ERROR] Failed to write unvisited nodes: {str(e)}")

def find_reconvergent_paths(graph, all_paths, output_file="reconvergent_paths.json"):
    reconvergent_data = []
    try:
        for node, paths in all_paths.items():
            unique_starts = set(path[0] for path in paths)
            if len(unique_starts) > 1:
                reconvergent_data.append({
                    "reconvergent_node": node,
                    "paths": [
                        {
                            "source": path[0],
                            "path": path
                        } for path in paths
                    ]
                })

        with open(output_file, "w") as f:
            json.dump(reconvergent_data, f, indent=2)
        print(f"[INFO] Reconvergent path details written to '{output_file}'.")

    except Exception as e:
        print(f"[ERROR] Could not detect or write reconvergent paths: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DAG DFS and reconvergent fanout analyzer")
    parser.add_argument("--dag", required=True, help="Input DAG file (JSON format)")
    parser.add_argument("--start", required=True, help="Start node for DFS")
    args = parser.parse_args()

    graph, all_nodes = load_dag_from_json(args.dag)

    if graph and args.start in graph:
        visited, all_paths = dfs_traverse(graph, args.start)
        save_output(visited)
        save_unvisited_nodes(all_nodes, visited)
        find_reconvergent_paths(graph, all_paths)
    else:
        print(f"[ERROR] Start node '{args.start}' not found in the graph.")
