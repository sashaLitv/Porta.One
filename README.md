# Puzzle matching
<img width="1101" height="726" alt="Screenshot 2026-11-08 at 00 53 30" src="https://github.com/user-attachments/assets/115ce511-549d-4d9c-a66f-58dc1afad7a8" />

This project contains a Python solution for the puzzle matching problem. It includes two different algorithms to find the longest chain of connected fragments based on matching prefixes and endings.

---
## About the solution 

I consciously decided to implement **two different algorithms** because this solution needs to be flexible for any future input files where I don't know the size of the data in advance.

1. **Exact method (DFS - depth-first search):**
* Finds the absolute best result by exploring all paths.
* Perfect for small datasets, but it will freeze or take too long on large amounts of data.

2. **Heuristic method (MMAS - max-min ant system):**
* Created to solve large datasets quickly without freezing.
* I chose the **MMAS** modification instead of Marco Dorigo's base Ant System to actively prevent strong stagnation. MMAS sets strict lower and upper bounds on pheromone levels and restricts updates, which helps the ants avoid getting stuck in local loops and continually explores better paths.
---

## Installation & dependencies
To run this project, you need Python installed on your system along with a few libraries:
- **NumPy**: used for fast matrix computations and handling probability distributions.
- **tqdm**: used for dynamic progress bars in the terminal.

You can install all required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt

```

---

## 🚀 How to Run

The main entry point of the project is **`main.py`**. You can run it from your terminal with optional arguments.

### Available parameters:
* `--input_path` *(optional)*: Path to the input file with fragments. By default, it looks for **`source.txt`** in the current directory.
* `--algo` *(optional)*: Chooses the algorithm to run. By default, it uses the MMAS.
* `--iterations` *(optional)*: Number of MMAS iterations (default: `200`).
* `--ants` *(optional)*: Number of ants per iteration in MMAS (default: `100`).
* `--rho` *(optional)*: Pheromone evaporation rate ($\rho$) in MMAS (default: `0.1`).
* `--alpha` *(optional)*: Pheromone weight ($\alpha$) in MMAS (default: `1.0`).
* `--beta` *(optional)*: Heuristic weight ($\beta$) in MMAS (default: `1.5`).

> ⚠️ **Important note on DFS:** The exact method is not a heuristic — it checks all possible paths to find the absolute optimum. However, if the input file contains **145 or more entries**, the exact method will hang or freeze due to exponential complexity. Therefore, it is recommended to use DFS only for smaller datasets (under 145 records).

---

## Results 
Exact solution (DFS): → 67 fragments (absolute maximum, guaranteed optimal path found by exploring all branches on source.txt).

Heuristic solution (MMAS): → 64–67 fragments (typically hits 65–66 consistently on source.txt, with occasional runs reaching the 67 optimum depending on randomness and hyperparameters).

---
```
