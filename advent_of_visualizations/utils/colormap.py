import seaborn as sns
from matplotlib.colors import Colormap
import numpy as np

def get_color(rgba) -> np.ndarray:
    """Returns a numpy array of uint8 of rgb values in (0-255) given a colormap and a t value in (0.0, 1.0)"""
    r, g, b, _ = rgba
    return np.array([r * 255, g * 255, b * 255], dtype=np.uint8)

def get_plotly_color(rgba):
    """Convert RGBA to rgb string for Plotly"""
    r, g, b, _ = rgba
    return f'rgb({int(r*255)},{int(g*255)},{int(b*255)})'

def get_cmap(name) -> Colormap:
    """Returns the Seaborn colormap with the given name"""
    return sns.color_palette(name, as_cmap=True)