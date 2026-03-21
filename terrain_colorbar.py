import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

def terrain_colorbar(origvals, colors, display_min, display_max, label=None, *,
                     ax=None, cax=None, location="right", size="3%", pad=0.2):
    """
    Create a non-uniform colormap from (origvals, colors) and add a colorbar
    that displays only [display_min, display_max] without changing the scaling.

    Parameters
    ----------
    origvals : (N,) array-like
        Data values (not necessarily evenly spaced).
    colors : (N,3) array-like
        RGB colors in [0,1] corresponding to origvals.
    display_min, display_max : float
        Subrange (in data units) to show on the colorbar (visual clip only).
    label : str, optional
        Label for the colorbar.
    ax : matplotlib Axes, optional
        Axes the colorbar should be associated with (host axes).
        If None, uses current axes (plt.gca()).
    cax : matplotlib Axes, optional
        Axes to draw the colorbar into. If None, a side axes is created on `ax`
        using make_axes_locatable(location/size/pad).
    location : {"right","left","top","bottom"}, optional
        Where to append the colorbar relative to `ax` when `cax` is None.
    size : str or float, optional
        Size of the colorbar axes (e.g., "3%").
    pad : float, optional
        Padding between the plot and the colorbar.

    Returns
    -------
    cb : matplotlib.colorbar.Colorbar
    cmap : matplotlib.colors.Colormap
    norm : matplotlib.colors.Normalize
    """
    origvals = np.asarray(origvals, dtype=float)
    colors = np.asarray(colors, dtype=float)

    order = np.argsort(origvals)
    v = origvals[order]
    c = colors[order]
    vmin, vmax = float(v[0]), float(v[-1])

    # Normalize positions for non-uniform spacing
    pos = (v - vmin) / (vmax - vmin)
    cmap = LinearSegmentedColormap.from_list("custom_nonuniform",
                                             list(zip(pos, c)), N=256)

    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)

    # Figure/axes plumbing
    if ax is None:
        ax = plt.gca()
    fig = ax.figure

    if cax is None:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(location, size=size, pad=pad)

    cb = fig.colorbar(mappable, cax=cax)

    # Visual clip to the displayed subrange (does NOT rescale the norm)
    dmin = float(np.clip(display_min, vmin, vmax))
    dmax = float(np.clip(display_max, vmin, vmax))
    if dmin > dmax:
        dmin, dmax = dmax, dmin

    cb.ax.set_ylim(dmin, dmax)

    if label is not None:
        cb.set_label(label)

    return cb, cmap, norm