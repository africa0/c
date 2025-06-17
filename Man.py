import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🌀 Mandelbrot Explorer with Interactive Zoom")

# Initial parameters and state
if 'x_center' not in st.session_state:
    st.session_state.x_center = -0.5
if 'y_center' not in st.session_state:
    st.session_state.y_center = 0.0
if 'zoom' not in st.session_state:
    st.session_state.zoom = 1.0

# Sliders for max iterations and colormap
max_iter = st.slider("Max iterations", 10, 300, 100, 10)
cmap = st.selectbox("Color map", ['twilight_shifted', 'inferno', 'magma', 'plasma', 'viridis'])

# Zoom slider (controlled externally)
zoom = st.slider("Zoom", 1.0, 100.0, st.session_state.zoom, 0.1)

# Mandelbrot calculation (same vectorized function)
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width).reshape((1, width))
    y = np.linspace(ymin, ymax, height).reshape((height, 1))
    c = x + 1j * y
    z = np.zeros_like(c, dtype=np.complex128)
    div_time = np.zeros(c.shape, dtype=int)
    mask = np.full(c.shape, True, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask]*z[mask] + c[mask]
        mask, old_mask = np.abs(z) <= 2, mask
        div_time += old_mask & (~mask) * i

    div_time[div_time == 0] = max_iter
    return div_time

# Calculate window based on center and zoom
scale = 1 / zoom
xmin, xmax = st.session_state.x_center - 1.5*scale, st.session_state.x_center + 1.5*scale
ymin, ymax = st.session_state.y_center - 1.5*scale, st.session_state.y_center + 1.5*scale
width, height = 600, 600

mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

# Create Plotly figure
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

# Capture click event to recenter zoom
clicked = st.plotly_chart(fig, use_container_width=True)

# NOTE: Streamlit currently does not provide direct click event data from Plotly charts.
# As a workaround, interactive zoom and pan are possible in Plotly itself.
# To implement click recenter, you'd need a more complex setup possibly outside Streamlit or using
# Streamlit callbacks or experimental components.

st.markdown("""
*Use Plotly’s zoom/pan tools to explore the fractal interactively.*

*To recenter or zoom further, use the sliders above.*
""")
