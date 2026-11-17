# Graph Routing & Pathfinding Visualizer

An interactive graph routing engine and Flask web visualizer implementing blind and heuristic shortest-path algorithms (`A*`, Uniform Cost Search, Greedy Search, and Depth-First Search) in object-oriented Python.

## Repository Structure

```text
graph-routing-pathfinder/
├── README.md
├── app.py                # Flask web server and route controller
├── Backend.py            # Graph representation (My_Map, Node) and search algorithms (Algorithms)
├── MapaLigacoes.csv      # Weighted bidirectional adjacency list of Portuguese cities (km)
├── DistanceToFaro.csv    # Straight-line heuristic distances to target node
├── requirements.txt      # Python dependencies
└── templates/            # HTML frontend with interactive path rendering and debug tables
```

## Key Engineering Highlights

- **Object-Oriented Graph Engine (`Backend.py`):** Decouples graph topology (`My_Map`), search state (`Node`), and traversal logic (`Algorithms`) so any weighted network CSV can be loaded dynamically.
- **Blind & Heuristic Search Implementations:**
  - **Uniform Cost Search (UCS):** Priority-queue-driven optimal shortest-path traversal by cumulative edge cost.
  - **A\* Search:** Combines cumulative path cost $g(n)$ with straight-line heuristic distance $h(n)$ for optimal guided routing.
  - **Greedy Best-First Search:** Supports both cycle-checked and pure memoryless modes.
  - **Depth-First Search (DFS):** LIFO stack traversal with closed-set cycle prevention.
- **Interactive Canvas UI & Step-by-Step Debugger:** Renders computed routes directly onto an HTML5 Canvas map and exposes frontier expansion logs (`Levels` and `Iterations` tables) for algorithm inspection.

## Tech Stack

- **Backend & Algorithms:** Python, Flask, `queue.PriorityQueue`
- **Frontend:** HTML5 Canvas, CSS, Jinja2 Templates

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Flask application
python app.py

# 3. Open in your browser
# [http://127.0.0.1:5000](http://127.0.0.1:5000)
```
