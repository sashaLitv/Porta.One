import argparse
from DFS import DFS

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
    dfs = DFS(nums)
    best_length, best_path = dfs.run_without_start_point()
    glued, glued_for_print = evaluate(nums, best_path)

    print(f"Length    : {best_length}")
    print(f"Formatted chain    : {glued_for_print}")
    print(f"Raw glued string   : {glued}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle-quiz using two method (DFS and MMAS modification)")
    parser.add_argument("--input_path", type=str, default="source.txt", help="Path to source file with puzzles (default: source.txt)")
    parser.add_argument(
        "--name_of_algorithm", 
        type=str, 
        default="MMAS", 
        choices=["MMAS", "DFS"],
        help="Name of algorithm: MMAS - heuristic, DFS - exhaustive chain enumeration (default: MMAS)"
    )

    args = parser.parse_args()
    main(args)