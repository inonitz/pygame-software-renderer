[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT][license-shield]][license-url]

<!-- PROJECT LOGO -->
<div align="center">
<h3 align="center">pygame-software-renderer</h3>
  <p align="center">
    A from-scratch software 3D renderer in numpy + pygame, across five rewrites (2019-2020)
  </p>
</div>

> **Archive notice:** This is a high-school-era learning archive, published as-is and marked read-only.
> The rewrite generations are preserved deliberately - the point of this repo *is* the progression.
> A few surgical fixes were applied at publication time (2026) so the flagship entry points run on
> modern Python/numpy - every such change is marked with an `archive fix (2026)` comment.

## About The Project

Before I knew what a graphics API was, I tried to build 3D rendering myself: projection matrices,
rotation, cameras, .obj parsing and triangle rasterization - all in numpy, drawn with pygame.
This repo preserves that journey, including the dead ends:

- **`early-experiments/`** - the first attempts. Rotating cubes, perspective projection one script at
  a time, plus `DIRT/` - the first structured attempt with a Camera/Vertex/Cube class hierarchy.
- **`renderer/`** - the main line, in the order it actually happened:
  `failed_attempts/` → `second_attempt/` → `rework/` → `rework2/` (first .obj mesh loading) →
  `rework3/` (camera + gui + renderer split, numba-accelerated math, the most complete iteration).
  `mesh_objects/` holds the .obj test meshes (yes, including the teapot).

## Project Structure

```
early-experiments/      single-file 3D experiments + DIRT/ (first class-based attempt)
renderer/
  ├── failed_attempts/  exactly what it says
  ├── second_attempt/
  ├── rework/
  ├── rework2/          .obj parsing appears
  ├── rework3/          most complete: python -m rework3.app
  ├── tests/            half-space triangle filling experiment
  └── mesh_objects/     teapot, cow, cube... test meshes
```

## Getting Started

### Prerequisites

- Python 3.10+ (verified on 3.12)
- `pip install -r requirements.txt` (numpy, pygame, numba; pyglet only for one early script)

### Downloading the Source

```
git clone https://github.com/inonitz/pygame-software-renderer.git
cd pygame-software-renderer
```

## Usage

**The classic** (spinning wireframe cube):

```
cd early-experiments
python rotating_cube_nice.py
```

**The most complete renderer** (rework3 - loads a filtered teapot mesh, WASD/mouse camera,
ESC pauses):

```
cd renderer
python -m rework3.app
```

Both verified working at publication time (2026) on Python 3.12 / pygame 2.6.

## Notes & Known Limitations

- Only the two entry points above are maintained-enough to run; the older generations are preserved
  as-is and some were already broken when they were abandoned (that's why the next rework exists).
- `renderer/rework2/main.py` references a `rework2/mesh_objects/` path that never existed in this
  layout - period-authentic breakage, left untouched.
- rework3 imports from rework2 (`parseFile`) - the generations were never fully independent.
- Expect runtime warnings from the projection math (divisions by ~0 at certain camera angles).

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/inonitz/pygame-software-renderer?style=for-the-badge&color=blue
[contributors-url]: https://github.com/inonitz/pygame-software-renderer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/inonitz/pygame-software-renderer?style=for-the-badge&color=blue
[forks-url]: https://github.com/inonitz/pygame-software-renderer/network/members
[stars-shield]: https://img.shields.io/github/stars/inonitz/pygame-software-renderer?style=for-the-badge&color=blue
[stars-url]: https://github.com/inonitz/pygame-software-renderer/stargazers
[license-shield]: https://img.shields.io/github/license/inonitz/pygame-software-renderer?style=for-the-badge
[license-url]: https://github.com/inonitz/pygame-software-renderer/blob/main/LICENSE
