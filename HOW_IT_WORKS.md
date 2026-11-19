How My Procedural Terrain Generator Works

1. What did I build?

I built a small procedural terrain generator using Python and NumPy.

The basic idea was to generate a random 2D grid, treat its values as elevations, smooth the rough terrain, add a mountain using mathematics, and finally convert the result into an interactive 3D visualization using Plotly.

Instead of manually designing a mountain, I used mathematical operations to generate it.

Let's understand how I did that.

---

2. First, I created a terrain

I started with:

terrain = np.random.randint(0, 100, (10, 10))

This generates a 10 × 10 array containing random numbers between 0 and 99.

But why a 2D array?

Because I wanted every position in the grid to represent a point on the ground, and its value to represent its elevation.

For example:

10  20  30
20  80  40
10  30  20

Here, 80 represents a higher point compared to the surrounding values.

So basically:

- Rows represent Y positions.
- Columns represent X positions.
- Values represent Z or elevation.

Now we have a basic heightmap.

But there is a problem: the terrain is too random and has sudden changes in elevation.

I wanted to make it smoother.

---

3. How did I smooth the terrain?

First, I needed to understand the neighbours of every cell.

For each position, I considered its eight surrounding neighbours.

A  B  C
D  X  E
F  G  H

Here, X is the current cell, and the other eight positions are its neighbours.

I used these directions in Python:

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),            (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

I also added boundary checking because cells at the edges don't have all eight neighbours.

Finding the average

After collecting the neighbours, I calculated their average.

The formula is:

[
\text{Average} =
\frac{\text{Sum of neighbour heights}}
{\text{Number of neighbours}}
]

I used NumPy's "np.mean()" for this.

But why not just replace the old height with the average?

Because I didn't want to completely remove the original terrain.

I wanted to preserve some of its original elevation while making it smoother.

So I used a weighted average:

[
H_{\text{new}} =
(1-\alpha)H_{\text{old}}+
\alpha H_{\text{average}}
]

I selected:

[
\alpha=0.2
]

Which gives:

[
H_{\text{new}} =
0.8H_{\text{old}}+0.2H_{\text{average}}
]

In simple words, 80% of the old height is preserved, and 20% comes from the neighbours' average.

This makes higher points gradually decrease and lower points surrounded by higher neighbours gradually increase.

That's how the sudden differences in elevation start becoming smoother.

Why did I repeat it?

I didn't want to perform smoothing just once.

I used:

iterations = 3

This means the entire grid goes through the smoothing process three times.

Every iteration uses the result of the previous iteration.

Mathematically:

[
H^{(t+1)}=S(H^{(t)})
]

Here, S represents one complete smoothing operation.

One important thing: I calculate all the new heights from the previous grid before replacing it. This prevents one cell's updated value from affecting another cell during the same iteration.

---

4. Now I wanted to generate a mountain

After smoothing, I had a smoother terrain, but I wanted to add a mountain.

Instead of manually assigning heights to different positions, I used a Gaussian function.

What is a Gaussian function?

A Gaussian function produces a bell-shaped curve.

When we extend this idea into two dimensions, it can produce a rounded hill or mountain.

The equation I used is:

[
M(x,y)=A\exp\left(
-\frac{(x-x_0)^2+(y-y_0)^2}
{2\sigma^2}
\right)
]

Let's understand the variables.

- A is the maximum additional height.
- x₀ is the mountain's centre along X.
- y₀ is the mountain's centre along Y.
- σ controls how wide the mountain is.
- exp represents the exponential function.

I selected these values:

peak_row = 5
peak_col = 5
max_height = 100
sigma = 2

So my mountain is centred at (5, 5), with a maximum additional height of 100.

How does this equation actually create a mountain?

First, I calculate the distance of every cell from the mountain's centre.

[
d=\sqrt{(x-x_0)^2+(y-y_0)^2}
]

Then I use that distance in the Gaussian equation:

[
M=A\exp\left(-\frac{d^2}{2\sigma^2}\right)
]

At the centre, the distance is zero.

So:

[
M=A\exp(0)=A
]

That means the centre receives the maximum additional height.

As we move away from the centre, the distance increases, and the exponential value decreases.

Therefore, the mountain gradually becomes shorter as we move away from its peak.

What does sigma do?

Sigma controls the spread of the mountain.

- Smaller sigma means a narrower mountain.
- Larger sigma means a wider mountain.

This is how I generated a mountain using mathematics instead of manually creating its shape.

---

5. Combining the mountain with the terrain

Now I had two separate arrays:

1. My smoothed random terrain.
2. My mathematically generated mountain.

I combined them:

final_terrain = terrain + mountain

Mathematically:

[
H_{\text{final}}=H_{\text{smooth}}+M
]

This simply adds the mountain's height to the existing terrain at every position.

Now I have my final heightmap.

---

6. How did I turn it into 3D?

Until this point, everything was just numerical data stored in a 2D array.

I wanted to actually see the terrain and rotate it.

For that, I used Plotly.

The basic concept is:

[
(x,y)\rightarrow z
]

The X and Y positions come from the grid, while Z comes from the elevation values.

I used:

go.Surface(
    z=final_terrain,
    colorscale="Earth",
    colorbar=dict(title="Elevation")
)

"go.Surface()" takes my elevation array and creates a 3D surface.

I selected the Earth colorscale to give the terrain different colours according to elevation.

I also configured the axes and aspect ratio to control how the terrain appears.

The best part is that Plotly makes it interactive.

I can rotate the terrain, zoom in, zoom out and inspect it from different angles.

---

7. Saving the result

Finally, I used:

fig.write_html(
    "/storage/emulated/0/Download/terrain_3d.html"
)

This saves the visualization as an HTML file.

I can open that file in my browser and interact with the 3D terrain.

One important distinction: this is an interactive 3D visualization, not an exported 3D model like OBJ or GLB.

---

8. The complete mathematics in one place

These are the main mathematical operations behind my project.

1. Random heightmap

[
H(i,j)\sim\text{UniformInteger}(0,99)
]

2. Neighbour averaging

[
\bar H_{i,j}=
\frac{1}{n}\sum H_{\text{neighbours}}
]

3. Smoothing

[
H^{(t+1)}{i,j}=
0.8H^{(t)}{i,j}+0.2\bar H^{(t)}_{i,j}
]

Repeated three times.

4. Gaussian mountain

[
M(x,y)=100\exp\left(
-\frac{(x-5)^2+(y-5)^2}{8}
\right)
]

5. Final terrain

[
\boxed{H_{\text{final}}=H_{\text{smooth}}+M}
]

6. 3D representation

[
z=H_{\text{final}}(x,y)
]

---

9. Current limitations

This is my first procedural terrain generator, so it has some limitations:

- The grid size is fixed at 10 × 10.
- The initial terrain is randomly generated.
- It generates one Gaussian mountain.
- Smoothing runs for three iterations.
- Mountain position and spread are manually configured.
- The output is an interactive HTML visualization, not a standalone 3D model.

These are limitations of my current implementation, not of procedural terrain generation itself.

---

10. What I learned

While building this project, I worked with:

- 2D numerical arrays.
- Neighbour indexing and boundary checking.
- Mean and weighted averaging.
- Iterative algorithms.
- Gaussian functions and exponential mathematics.
- Euclidean distance.
- 3D surface visualization.

My main takeaway:

I didn't manually draw a mountain or design every elevation.

I created mathematical rules, applied them to numerical data, and let the computer generate the terrain.

That's the basic idea behind my procedural terrain generator.

