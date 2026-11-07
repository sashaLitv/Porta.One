import argparse
from DFS import DFS
from MMAS import MMAS

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip()]

def evaluate(nums, seq):
    if not seq:
        return 0, ""

    first_num = nums[seq[0]]
    overlap = first_num[-2:]
    glued = first_num[:-2] + overlap
    glued_for_print = first_num[:-2]
    for i in seq[1:]:
        if nums[i][:2] != overlap:
            raise ValueError("Invalid sequence: string connection does not match")
            # break

        glued_for_print += f"({overlap})" + nums[i][2:]
        glued += nums[i][2:]
        overlap = nums[i][-2:]

    return glued, glued_for_print

def main(args):
    nums = load(args.input_path)

    if args.algo == "DFS":
        if len(nums) < 145:
            dfs = DFS(nums)
            best_length, best_path = dfs.run()
            glued, glued_for_print = evaluate(nums, best_path)
        else:
            args.algo = "DFS"
            print("WARNING] DFS is computationally prohibitive for datasets with >= 145 elements")

    if args.algo == "MMAS":
        aco = MMAS(nums=nums, num_iterations=200, num_ants=100, rho=0.1, alpha=1.0, beta=1.5)
        best_length, best_path = aco.run()
        glued, glued_for_print = evaluate(nums, best_path)

    print(f"Length    : {best_length}")
    print(f"Formatted chain    : {glued_for_print}")
    print(f"Raw glued string   : {glued}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle-quiz using two method (DFS and MMAS-ACO")
    parser.add_argument("--input_path", type=str, default="source.txt", help="Path to source file with puzzles (default: source.txt)")
    parser.add_argument("--algo", type=str, default="MMAS", choices=["MMAS", "DFS"], help="Name of algorithm, you can choose between two method: MMAS(heuristic) and DFS(brute)")
    args = parser.parse_args()
    main(args)