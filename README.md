# Cellular Automata Caves (raylib + pyray)

A **procedural cave generation** demo built with Python, using **cellular automata smoothing** on seeded noise to generate infinite, chunked cave worlds — rendered in real time with **raylib** and **pyray**.

---

## ✨ Features

* **Procedural cave generation** using hash-based noise + cellular automata smoothing
* **Infinite chunk-based world** — chunks load and unload dynamically around the camera
* **Seamless chunk borders** — chunks are generated with configurable padding so smoothing at the edges blends correctly with neighbours, eliminating visible seams
* **Chunk render textures** — each chunk is pre-baked to a texture and only redrawn when dirty
* **Smooth camera movement** with arrow keys
* **Real-time tile editing** — place and destroy wall tiles with the mouse; the affected chunk is immediately marked dirty and re-rendered
* **Debug mode** — chunk borders, tile coordinate tooltips, and grid overlay
* Lightweight multi-file structure with clean separation of concerns

---

## 📦 Requirements

Make sure you have Python installed, then install dependencies:

```bash
pip install raylib numpy scipy
```

---

## 🚀 Running the Project

```bash
python main.py
```

---

## 🎮 Controls

| Key / Button        | Action                  |
| ------------------- | ----------------------- |
| Arrow Keys          | Move camera             |
| Left Mouse Button   | Place tile (wall)       |
| Right Mouse Button  | Destroy tile (empty)    |
| `F1`                | Toggle debug mode       |
| ESC / Close Window  | Exit program            |

---

## ⚙️ Configuration

All key parameters live in `settings.py`:

```python
SEED = 534543           # World generation seed
TILE_SIZE = 16          # Pixels per tile
CHUNK_WIDTH  = 64       # Tiles per chunk (X)
CHUNK_HEIGHT = 64       # Tiles per chunk (Y)
WALL_THRESHOLD = 0.50   # Noise density — higher = more walls
CHUNK_PADDING = 4       # Border padding for seamless chunk edges
SMOOTHING_AMOUNT = 8    # Cellular automata passes — higher = rounder caves
```

---

## 🖼️ Preview

![App Screenshot](screenshot.gif)
