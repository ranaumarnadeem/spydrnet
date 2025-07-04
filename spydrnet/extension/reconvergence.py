import json
import argparse
from collections import defaultdict

def dfs_traverse(graph, start_node, visited=None, depth=0):
    """
    Depth-first traversal starting from start_node.
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
    Load DAG from JSON file and return adjacency list and node metadata.
    """
    try:
        with open(filepath, "r") as f:
            dag_data = json.load(f)

        graph = {}
        node_dict = {}
        for node, neighbors in zip(dag_data["nodes"], dag_data["adjacency"]):
            node_id = node["id"]
            graph[node_id] = [edge["id"] for edge in neighbors]
            node_dict[node_id] = node

        print(f"[INFO] Loaded DAG with {len(graph)} nodes.")
        return graph, list(node_dict.keys()), node_dict

    except FileNotFoundError:
        print(f"[ERROR] File '{filepath}' not found.")
        return {}, [], {}

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {str(e)}")
        return {}, [], {}

    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return {}, [], {}


def save_list_to_file(node_list, filename, label):
    """
    Write list of node names to file.
    """
    try:
        with open(filename, "w") as f:
            for node in sorted(node_list):
                f.write(node + "\n")
        print(f"[INFO] {label} written to '{filename}'.")

    except Exception as e:
        print(f"[ERROR] Could not write {label} file: {str(e)}")


def save_node_structures(node_list, node_dict, filename, label):
    """
    Write full structure of specified nodes to JSON.
    """
    try:
        node_structs = [node_dict[node] for node in node_list if node in node_dict]
        with open(filename, "w") as f:
            json.dump(node_structs, f, indent=2)
        print(f"[INFO] {label} structure written to '{filename}'.")

    except Exception as e:
        print(f"[ERROR] Failed to write {label} structure: {str(e)}")


def find_reconvergent_nodes(graph):
    """
    Identify reconvergent nodes: those reached by multiple unique DFS paths.
    """
    path_count = defaultdict(set)

    def dfs(node, path_id):
        if path_id in path_count[node]:
            return
        path_count[node].add(path_id)
        for neighbor in graph.get(node, []):
            dfs(neighbor, path_id)

    for idx, node in enumerate(graph.keys()):
        dfs(node, path_id=f"path_from_{node}")

    reconvergent = [node for node, paths in path_count.items() if len(paths) > 1]
    return reconvergent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DFS and reconvergence analysis of a DAG")
    parser.add_argument("-i", "--input", required=True, help="Path to DAG JSON file")
    parser.add_argument("-s", "--start", required=True, help="Start node for DFS")
    parser.add_argument("--dfs_out", default="dfs_output.txt", help="Visited node names")
    parser.add_argument("--unvisited_out", default="unvisited_nodes.txt", help="Unvisited node names")
    parser.add_argument("--reconverge_out", default="reconvergent_nodes.txt", help="Reconvergent node names")

    parser.add_argument("--dfs_detail", default="visited_nodes_detail.json", help="Visited node structure")
    parser.add_argument("--unvisited_detail", default="unvisited_nodes_detail.json", help="Unvisited node structure")
    parser.add_argument("--reconverge_detail", default="reconvergent_nodes_detail.json", help="Reconvergent node structure")

    args = parser.parse_args()

    graph, all_nodes, node_dict = load_dag_from_json(args.input)
    if not graph or args.start not in graph:
        print(f"[ERROR] Invalid input or start node '{args.start}' not found.")
        exit(1)

    # === DFS Traversal ===
    visited_nodes = dfs_traverse(graph, args.start)
    unvisited_nodes = set(all_nodes) - visited_nodes

    save_list_to_file(visited_nodes, args.dfs_out, "DFS visited nodes")
    save_list_to_file(unvisited_nodes, args.unvisited_out, "Unvisited nodes")
    save_node_structures(visited_nodes, node_dict, args.dfs_detail, "Visited nodes")
    save_node_structures(unvisited_nodes, node_dict, args.unvisited_detail, "Unvisited nodes")

    # === Reconvergence Detection ===
    reconvergent_nodes = find_reconvergent_nodes(graph)
    print(f"[INFO] Found {len(reconvergent_nodes)} reconvergent node(s).")
    save_list_to_file(reconvergent_nodes, args.reconverge_out, "Reconvergent nodes")
    save_node_structures(reconvergent_nodes, node_dict, args.reconverge_detail, "Reconvergent nodes")
