'''
    The heuristic algorithm for the Maximum Matching in a Sequence (MMAS) problem, based on Ant Colony Optimization (ACO)
'''
import numpy as np
from tqdm import tqdm

class MMAS:
    def __init__(self, nums, num_iterations, num_ants, rho, alpha, beta):
        self.nums = nums
        self.num_iterations = num_iterations
        self.num_ants = num_ants
        self.rho = rho                          # how fast the pheromone disappears (evaporation rate)
        self.alpha = alpha                      # pheromone weight
        self.beta = beta                        # heuristic weight

        unique_nodes = sorted({int(n[:2]) for n in nums} | {int(n[-2:]) for n in nums})
        self.uniq_L = len(unique_nodes)
        self.L = len(nums)

        self.pheromone_max = None
        self.pheromone_min = None 
        self.p_best = 0.05
        self.p_dec = self.p_best ** (1.0 / (self.L - 1))

        # bidirectional mapping between real state values (e.g., 00-99) and compact matrix indices (0 to K-1)
        # to save memory and ensure O(1)
        self.node_to_idx = {node: idx for idx, node in enumerate(unique_nodes)}
        self.idx_to_node = {idx: node for idx, node in enumerate(unique_nodes)}

        self.capacity, self.transition_pool = self._initialize_graph_and_pools(nums)

        self.pheromones = np.ones((self.uniq_L, self.uniq_L))

        self.eta = self._build_lookahead_heuristic()

        self.best_solution = (0, [])

    def _initialize_graph_and_pools(self, nums):
        '''Initializes the graph representation and transition pools based on the input nums'''
        # matrix to store the capacity for each state transition (u_idx -> v_idx)
        capacity = np.zeros((self.uniq_L, self.uniq_L), dtype=int)
        # maps a pair of states (u_idx, v_idx) to a list of original
        transition_pool = {}
    
        for idx, num in enumerate(nums):
            u_real = int(num[:2])
            v_real = int(num[-2:])
        
            u_idx = self.node_to_idx[u_real]
            v_idx = self.node_to_idx[v_real]
        
            capacity[u_idx, v_idx] += 1
            
            if (u_idx, v_idx) not in transition_pool:
                transition_pool[(u_idx, v_idx)] = []
                        
            transition_pool[(u_idx, v_idx)].append(idx)

        return capacity, transition_pool

    def _build_lookahead_heuristic(self, local_weight=1.0, lookahead_weight = 0.6):
        '''Builds the 2-step lookahead heuristic matrix (eta) based on the graph's capacity'''
        eta = np.zeros((self.uniq_L, self.uniq_L))

        for u in range(self.uniq_L):
            for v in range(self.uniq_L):
                if self.capacity[u, v] == 0:
                    eta[u, v] = 0.0
                    continue

                level_1 = [w for w in range(self.uniq_L) if self.capacity[v, w] > 0]
                score_1 = len(level_1)

                score_2 = 0
                for w in level_1:
                    level_2 = [z for z in range(self.uniq_L) if self.capacity[w, z] > 0]
                    score_2 += len(level_2)

                eta[u, v] = local_weight * score_1 + lookahead_weight * score_2

        max_val = np.max(eta)
        if max_val > 0:
            eta /= max_val

        return eta

    def construct_solution(self, start_idx=None):
        '''Constructs a solution path starting from a given idx or selecting a starting idx if none is provided'''
        edge_counts = {}
        if start_idx is None: start_idx = self.select_next_idx(edge_counts, current_idx=None)
        if start_idx is None: return []

        current_idx = start_idx
        path = [start_idx]

        while True:
            next_idx = self.select_next_idx(edge_counts, current_idx)
            if next_idx is None:
                break
            next_idx = int(next_idx)
            path.append(next_idx)
            edge_counts[(current_idx, next_idx)] = edge_counts.get((current_idx, next_idx), 0) + 1
            current_idx = next_idx

        return path
    
    def select_next_idx(self, edge_counts, current_idx):
        '''
            Selects the next idx or a starting idx using the probabilistic ACO rule.
            If current_idx is None, it selects a starting idx from all valid idxs in the graph.
        '''
        # select start idx based on calculated node potential
        if current_idx is None:
            available_idxs = [u for u in range(self.uniq_L) if np.sum(self.capacity[u, :]) > 0]
            if not available_idxs:
                return None

            probabilities = np.zeros(self.uniq_L)
            for u in available_idxs:
                strength = 0.0
                for v in range (self.uniq_L):
                    if self.capacity[u, v] > 0:
                        strength += (self.pheromones[u, v] ** self.alpha) * (self.eta[u, v] ** self.beta)

                probabilities[u] = max(strength, 0.001)

            total_prob = np.sum(probabilities)
            probabilities /= total_prob

            return np.random.choice(self.uniq_L, p=probabilities)

        # gather all valid successor idxs with remaining edge capacity 
        unvisited_idxs = []
        for idx in range(self.uniq_L):
            max_cap = self.capacity[current_idx, idx]
            if max_cap > 0:
                used_count = edge_counts.get((current_idx, idx), 0)
                if used_count < max_cap:
                    unvisited_idxs.append(idx)

        if not unvisited_idxs:
            return None
            
        # calculate transition probabilities using pheromone and heuristic weights
        probabilities = np.zeros(self.uniq_L)
        total_prob = 0.0

        for idx in unvisited_idxs:
            pheromone = self.pheromones[current_idx, idx] ** self.alpha
            eta = self.eta[current_idx, idx] ** self.beta

            probabilities[idx] = pheromone * eta
            total_prob += probabilities[idx]

        if total_prob == 0.0:
            return np.random.choice(unvisited_idxs)

        probabilities /= total_prob

        return np.random.choice(self.uniq_L, p = probabilities)
    

    def _check_pheromone_limits(self):
        '''Checks and updates the pheromone limits based on the best solution found on this iteration'''
        if self.best_solution[1] == []:
            return
        
        self.pheromone_max = 1.0 / (self.rho * (self.L - self.best_solution[0]))
        self.pheromone_min = (self.pheromone_max * (1 - self.p_dec)) / (0.5 * self.p_dec)

    def update_pheromones(self, iter_best):
        '''Updates the pheromone levels based on the best solution found in the current iteration'''
        if self.best_solution[0] == 0:
            return
        
        self.pheromones *= (1.0 - self.rho)
        delta_pheromone = 1.0 / (self.L - iter_best[0])

        for i in range(iter_best[0] - 1):
            u, v = iter_best[1][i], iter_best[1][i+1]

            self.pheromones[u, v] += delta_pheromone

        self._check_pheromone_limits()
        np.clip(self.pheromones, self.pheromone_min, self.pheromone_max, out=self.pheromones)


    def _get_full_number_path(self, path_indices):
        '''Converts a path of node indices into a sequence of full 6-digit strings from nums'''
        if not path_indices or len(path_indices) < 2:
            return []
            
        full_seq = []
        for i in range(len(path_indices) - 1):
            u_idx = path_indices[i]
            v_idx = path_indices[i+1]
            
            frag_idx = self.transition_pool[(u_idx, v_idx)][0]
            full_seq.append(frag_idx)
            
        return full_seq

    
    def run(self, start_node=None):
        '''Executes the Max-Min Ant System (MMAS) optimization loop. Args: start_node (int, optional): An optional starting node for the construction phase'''
        start_idx = None
        if start_node is not None:
            try:
                target_val = int(start_node)
            except ValueError:
                raise ValueError(f"Invalid start_node format: '{start_node}'. Expected a valid node identifier.")

            if target_val not in self.node_to_idx:
                available_examples = list(self.node_to_idx.keys())[:5]
                raise ValueError(
                    f"Start node '{start_node}' does not exist in the input data. "
                    f"Available nodes include: {available_examples}..."
                )
            
            start_idx = self.node_to_idx[target_val]

        for _ in tqdm(range(self.num_iterations), desc="Running ACO...") :
            iter_best = (0, [])

            for _ in range(self.num_ants):
                path = self.construct_solution(start_idx=start_idx)
                if not path: continue

                path_length = len(path)

                if path_length > iter_best[0]:
                    iter_best = path_length, path

                if path_length > self.best_solution[0]:
                    self.best_solution = (path_length, path)
                    print(f"\nNew best solution found with length: {path_length}")

            self.update_pheromones(iter_best) 

        self.best_solution = (self.best_solution[0], self._get_full_number_path(self.best_solution[1]))
        return self.best_solution

    