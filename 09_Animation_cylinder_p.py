import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

# Load your two .dat files
data1 = np.loadtxt('InitialData.dat')  # replace with your actual file names
data2 = np.loadtxt('shiftedRealData.dat')
data = np.vstack((data1, data2))

# Extract columns from the data (no header)
# 0: time, 1: R, 2: phi, 5: d
time = data[:, 0]
R = data[:, 1]
phi = data[:, 2]
d = data[:, 5]

# Set up figure
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect('equal')
ax.set_xlim(-5, 6)
ax.set_ylim(-2, 2)

# --- Create fixed cell structure ---
cell_radius = 1
cylinder_length = 4  # Short cylinder

# Hemisphere (convex to left)
theta = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
hemi_x = cell_radius * np.cos(theta)
hemi_y = cell_radius * np.sin(theta)
hemi_x += 0  # left edge is x = 0

light_green_c='#90ee90'
deep_green_c='#006400'

# Cylinder rectangle (starts from x=0 to x=cylinder_length)
cell_body = patches.Rectangle((0, -cell_radius), cylinder_length, 2 * cell_radius,
                              facecolor=light_green_c, edgecolor='black', alpha=0.4)
ax.add_patch(cell_body)

# Hemisphere patch
# Create a filled hemisphere patch to match the cylinder color
hemi_patch = patches.Polygon(np.column_stack((hemi_x, hemi_y)),
                             closed=True,
                             facecolor=light_green_c,
                             edgecolor='black',
                             alpha=0.4)
ax.add_patch(hemi_patch)

# Moving spore (initial position placeholder)
spore_patch = plt.Circle((-d[0], 0), R[0], color=deep_green_c, alpha=0.5)
ax.add_patch(spore_patch)

# --- Animation function ---
def animate(i):
    r = R[i]
    angle = phi[i]
    dist = d[i]

    # New corrected center: always on x-axis
    cx = -dist * np.cos(angle)
    cy = 0  # Fixed to keep on x-axis

    spore_patch.center = (cx, cy)
    spore_patch.set_radius(r)

    ax.set_title(f"Time: {time[i]:.0f} | R: {r:.2f} | d: {dist:.2f} | φ: {angle:.2f} rad")
    return spore_patch,

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(time), interval=30, blit=True)

# Save to MP4
ani.save("sporulation_short_cylinder_p.mp4", writer='ffmpeg', fps=300)

# Optional: uncomment to show interactively
# plt.show()

