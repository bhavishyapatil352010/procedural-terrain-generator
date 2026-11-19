import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import plotly.graph_objects as go

terrain = np.random.randint(0, 100, (10, 10))


neighbors = [
    terrain[0, 0], terrain[0, 1], terrain[0, 2],
    terrain[1, 0],                 terrain[1, 2],
    terrain[2, 0], terrain[2, 1], terrain[2, 2]
]

neighbor_avg = np.mean(neighbors)

alpha = 0.2

old_height = terrain[1, 1]

new_height = (1 - alpha) * old_height + alpha * neighbor_avg


new_terrain = terrain.astype(float)

new_terrain[1, 1] = new_height

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),            (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

rows, cols = terrain.shape

new_terrain = terrain.astype(float)

iterations = 3

for iteration in range(iterations):

    new_terrain = terrain.astype(float)

    for row in range(rows):
        for col in range(cols):
            neighbors = []

            for dr, dc in directions:
                r = row + dr
                c = col + dc

                if 0 <= r < rows and 0 <= c < cols:
                    neighbors.append(terrain[r, c])

            neighbor_avg = np.mean(neighbors)
            old_height = terrain[row, col]

            new_height = (1 - alpha) * old_height + alpha * neighbor_avg

            new_terrain[row, col] = new_height

    terrain = new_terrain
# Mountain generation

peak_row = 5
peak_col = 5

max_height = 100
sigma = 2

mountain = np.zeros((rows, cols), dtype=float)

for row in range(rows):
    for col in range(cols):

        distance = np.sqrt(
            (row - peak_row)**2 +
            (col - peak_col)**2
        )

        height = max_height * np.exp(
            -(distance**2) / (2 * sigma**2)
        )

        mountain[row, col] = height

final_terrain = terrain + mountain

fig = go.Figure(data=[
    go.Surface(
        z=final_terrain,
        colorscale="Earth",
        colorbar=dict(title="Elevation")
    )
])

fig.update_layout(
    title="Interactive 3D Terrain",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Elevation",
        aspectratio=dict(x=1, y=1, z=0.5)
    )
)

fig.write_html(
    "/storage/emulated/0/Download/terrain_3d.html"
)

print("Interactive 3D terrain saved!")