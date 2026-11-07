from tqdm import tqdm

class DFS():
    def __init__(self, nums):
        '''
        '''
        self.nums = nums
        self.adjacency_dict = self._create_adjacency_dict(nums)

        self.best_len = 0
        self.best_path = []

    def _create_adjacency_dict(self, nums):
        '''
        '''
        dictonary = {}

        for i, num in enumerate(nums):
            prefix = num[:2]
            if prefix not in dictonary:
                dictonary[prefix] = []

            dictonary[prefix].append(i)

        return dictonary

    def dfs(self, current_point, used, current_path):
        '''
        '''
        if len(current_path) > self.best_len:
            self.best_len = len(current_path)
            self.best_path = list(current_path)

        if current_point in self.adjacency_dict:
            for candidate in self.adjacency_dict[current_point]:
                if not used[candidate]:
                    # step forward
                    used[candidate] = True
                    current_path.append(candidate)
                    next_point = self.nums[candidate][-2:]
                    self.dfs(next_point, used, current_path)

                    # back step 
                    used[candidate] = False
                    current_path.pop()
                    
    
    def run_without_start_point(self):
        '''
        '''

        n = len(self.nums)
        self.best_len = 0
        self.best_path = []

        for i, num in enumerate(tqdm(self.nums, desc="Running DFS...")):
            used = [False] * n
            used[i] = True  

            start_point = num[-2:]
            self.dfs(start_point, used, [i])

        return self.best_len, self.best_path