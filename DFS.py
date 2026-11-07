'''
'''

from tqdm import tqdm

class DFS():
    def __init__(self, nums):
        '''
            Initializes the DFS solver with a list of string fragments.
            Builds the adjacency dictionary and sets up tracking for the best solution
        '''
        self.nums = nums
        self.n = len(nums)

        self.head, self.tail, self.adj = self._create_adjacency_structures(nums)

    def _create_adjacency_structures(self, nums):
        '''
            Helper method that maps string prefixes/suffixes to integer IDs and builds 
            the adjacency list and tail arrays
        '''
        unique_nodes = sorted({n[:2] for n in nums} | {n[-2:] for n in nums})
        index = {node: i for i, node in enumerate(unique_nodes)}

        head = [index[n[:2]] for n in nums]
        tail = [index[n[-2:]] for n in nums]

        adj = [[] for _ in unique_nodes]
        # Build the adjacency list: map each starting node (prefix) 
        # to the list of fragment indices (edges) that begin at that node
        for edge, node in enumerate(head):
            adj[node].append(edge)

        return head, tail, adj

    def _run_one_step_with_node(self, start_node):
        '''Runs a depth-first search starting from a specific node, tracking the longest path found'''
        adj, tail = self.adj, self.tail
        best_depth = 0
        best_path_local = []
        path = []

        def _dfs(cur, used, depth):
            '''
                Recursive depth-first search method to explore valid fragment chains and 
                return depth, best path whenever a longer sequence is found
            '''
            nonlocal best_depth, best_path_local
            
            if depth > best_depth:
                best_depth = depth
                best_path_local = list(path)

            for edge in adj[cur]:
                if not used[edge]:
                    used[edge] = True
                    path.append(edge)
                    
                    _dfs(tail[edge], used, depth + 1)
                    
                    path.pop()
                    used[edge] = False

        used = [False] * self.n
        used[start_node] = True
        path.append(start_node)
        
        _dfs(tail[start_node], used, 1)
        
        return best_depth, best_path_local

    def run(self, start_node=None):
        '''
            Iterates through every fragment as a potential starting point, displaying a 
            progress bar, and returns the maximum length and path found
        '''
        if start_node is not None:
            try:
                start_node = int(start_node)
            except ValueError:
                raise ValueError(f"Invalid start_node format: '{start_node}'. Expected a valid node identifier.")
        
        best_len, best_path = 0, []

        if start_node is not None:
            best_len, best_path = self._run_one_step_with_node(start)
        else:
            for start in tqdm(range(self.n), desc="Running DFS..."):
                length, path = self._run_one_step_with_node(start)
                if length > best_len:
                    best_len, best_path = length, list(path)

        return best_len, best_path


