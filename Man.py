import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🌀 Explore Mandelbrot Set with +256712427799")

# Initialize session state for center and zoom
if "x_center" not in st.session_state:
    st.session_state.x_center = -0.5
if "y_center" not in st.session_state:
    st.session_state.y_center = 0.0
if "zoom" not in st.session_state:
    st.session_state.zoom = 1.0

# Controls
max_iter = st.slider("Max iterations", 10, 300, 100, 10)
zoom = st.slider("Zoom (scale)", 1.0, 100.0, st.session_state.zoom, 0.1)
x_center = st.slider("X center", -2.0, 1.0, st.session_state.x_center, 0.01)
y_center = st.slider("Y center", -1.5, 1.5, st.session_state.y_center, 0.01)
cmap = st.selectbox("Color map", ['Viridis','Cividis','Inferno','Magma','Plasma','Turbo','Electric','Rainbow','Greys','Blues'])

# Update session state
st.session_state.zoom = zoom
st.session_state.x_center = x_center
st.session_state.y_center = y_center

# Vectorized Mandelbrot set calculation
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width).reshape((1, width))
    y = np.linspace(ymin, ymax, height).reshape((height, 1))
    c = x + 1j * y
    z = np.zeros_like(c, dtype=np.complex128)
    div_time = np.zeros(c.shape, dtype=int)
    mask = np.full(c.shape, True, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c[mask]
        mask, old_mask = np.abs(z) <= 2, mask
        div_time += old_mask & (~mask) * i

    div_time[div_time == 0] = max_iter
    return div_time

# Calculate bounds based on zoom and center
scale = 1 / zoom
xmin, xmax = x_center - 1.5 * scale, x_center + 1.5 * scale
ymin, ymax = y_center - 1.5 * scale, y_center + 1.5 * scale
width, height = 600, 600

# Compute fractal data
mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

# Plot using Plotly heatmap
fig = go.Figure(data=go.Heatmap(
    z=mandelbrot_image.T,
    colorscale=cmap,
    zsmooth='best',
    x=np.linspace(xmin, xmax, width),
    y=np.linspace(ymin, ymax, height),
    colorbar=dict(title='Iterations')
))

fig.update_layout(
    title="Mandelbrot Set",
    xaxis_title="Re",
    yaxis_title="Im",
    yaxis=dict(scaleanchor="x", scaleratio=1),
    dragmode='zoom',
    hovermode='closest',
    height=700,
    width=700
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
*Use the plot's zoom, pan, and box select tools for interactive exploration.*

*Adjust the sliders above to change iteration depth, zoom, and center.*
""")
