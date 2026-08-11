import numpy as np

def generate_line(start_point, heading, num_points, spacing, orthogonal=0, degrees=False):
    """
    Generates a sequence of 2D points along a specified heading or orthogonal to it.

    Parameters:
    -----------
    start_point : array-like of shape (2,)
        The starting (x, y) coordinates.
    heading : float
        The heading angle. By default interpreted in degrees (0 = +X axis, 90 = +Y axis).
    num_points : int
        Number of points to generate.
    spacing : float
        Distance between consecutive points.
    orthogonal : int, optional (default=0)
        -  0: Generate along the heading.
        - -1: Generate orthogonal to the left (+90° / counter-clockwise).
        -  1: Generate orthogonal to the right (-90° / clockwise).
    degrees : bool, optional (default=True)
        Set to False if `heading` is passed in radians.

    Returns:
    --------
    np.ndarray of shape (num_points, 2)
        Array of (x, y) point coordinates.
    """
    if orthogonal not in (-1, 0, 1):
        raise ValueError("orthogonal flag must be -1 (left), 0 (along heading), or 1 (right).")

    # Convert angle to radians if in degrees
    angle = np.radians(heading) if degrees else heading

    # Adjust angle for orthogonal direction
    # -1 (Left)  -> +90 degrees (+pi/2 rad)
    #  1 (Right) -> -90 degrees (-pi/2 rad)
    if orthogonal == -1:
        angle += np.pi / 2
    elif orthogonal == 1:
        angle -= np.pi / 2

    # Unit direction vector [cos(angle), sin(angle)]
    direction = np.array([np.cos(angle), np.sin(angle)])

    # Compute scalar distances for each point: [0, spacing, 2*spacing, ...]
    distances = np.arange(num_points) * spacing

    # Broadcast multiplication to calculate point positions
    points = np.asarray(start_point) + distances[:, np.newaxis] * direction

    return points