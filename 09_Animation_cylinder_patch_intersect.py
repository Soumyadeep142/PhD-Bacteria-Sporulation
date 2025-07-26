import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from matplotlib.path import Path
from matplotlib.patches import PathPatch

# --- Load Data ---
data1 = np.loadtxt('InitialData.dat')
data2 = np.loadtxt('shiftedRealData.dat')
data = np.vstack((data1, data2))

# Extract columns (0: time, 1: R, 2: phi, 5: d)
time = data[:, 0]
R = data[:, 1]
phi = data[:, 2]
d = data[:, 5]

# --- Cell geometry ---
cell_radius = 1
cylinder_length = 4

def build_cell_polygon():
    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
    hemi_x = cell_radius * np.cos(theta)
    hemi_y = cell_radius * np.sin(theta)

    rect_x = [0, cylinder_length, cylinder_length, 0]
    rect_y = [-cell_radius, -cell_radius, cell_radius, cell_radius]

    full_x = np.concatenate([hemi_x, rect_x])
    full_y = np.concatenate([hemi_y, rect_y])
    return Polygon(zip(full_x, full_y))

cell_poly = build_cell_polygon()

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect('equal')
ax.set_xlim(-5, 6)
ax.set_ylim(-2, 2)

# --- Patch for intersection only ---
intersection_patch = PathPatch(Path.make_compound_path(), facecolor='blue', ec='black', alpha=0.6)
ax.add_patch(intersection_patch)

# --- Helper: shapely polygon to matplotlib path ---
def polygon_to_pathpatch(poly, **kwargs):
    if poly.is_empty:
        return PathPatch(Path.make_compound_path(), visible=False)
    if poly.geom_type == 'Polygon':
        x, y = poly.exterior.coords.xy
        path = Path(np.column_stack((x, y)))
        return PathPatch(path, **kwargs)
    elif poly.geom_type == 'MultiPolygon':
        paths = []
        for part in poly.geoms:
            x, y = part.exterior.coords.xy
            paths.append(Path(np.column_stack((x, y))))
        compound = Path.make_compound_path(*paths)
        return PathPatch(compound, **kwargs)
    else:
        return PathPatch(Path.make_compound_path(), visible=False)

# --- Animation function ---
def animate(i):
    r = R[i]
    angle = phi[i]
    dist = d[i]

    cx = -dist * np.cos(angle)
    cy = 0

    spore = Point(cx, cy).buffer(r, resolution=100)
    intersection = cell_poly.intersection(spore)

    new_patch = polygon_to_pathpatch(intersection, facecolor='blue', alpha=0.6, edgecolor='black')
    intersection_patch.set_path(new_patch.get_path())
    intersection_patch.set_visible(not intersection.is_empty)

    ax.set_title(f"Time: {time[i]:.0f} | R: {r:.2f} | d: {dist:.2f} | φ: {angle:.2f} rad")
    return intersection_patch,

# --- Animate and Save ---
ani = animation.FuncAnimation(fig, animate, frames=len(time), interval=30, blit=True)
ani.save("intersection_only.mp4", writer='ffmpeg', fps=300)

