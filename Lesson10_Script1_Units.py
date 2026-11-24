import numpy as np

# Read the 3-component velocity (u, v, w) in m/s from the input dataset
inp = inputs[0]
vel = inp.PointData['velocity'] # shape (N, 3), units: m/s

# Latitude of every point, in degrees.
# getattr(inp, 'Points', None) returns the point coordinates if the grid stores them
# (e.g. a structured grid after the Transform filter), or None if it does not (plain image data).
pts = getattr(inp, 'Points', None)
if pts is not None:
    lat = np.asarray(pts)[:, 1]            # column 1 = y = latitude of every point
else:
    # Image data stores only origin and spacing, so rebuild the latitude from the point numbering.
    # Points are stored x-fastest, then y, then z:
    # 1) np.arange(...) numbers every point from 0 to nx*ny*nz - 1
    # 2) // nx gives a row counter that grows by 1 every nx points (one row of longitudes)
    # 3) % ny wraps the counter back to 0 at each new depth level -> latitude index 0 ... ny-1
    nx, ny, nz = inp.GetDimensions()
    row = (np.arange(nx * ny * nz) // nx) % ny
    lat = inp.GetOrigin()[1] + row * inp.GetSpacing()[1]

R   = 6371000.0   # mean Earth radius in metres
day = 86400.0     # seconds per day

# Convert horizontal velocities from m/s to degrees per day:
# - u (east-west): 1 degree of longitude gets shorter away from the equator
#   (length = R * cos(lat) * pi/180), so we divide by cos(lat)
# - v (north-south): 1 degree of latitude is always R * pi/180 = 111 km
u = vel[:, 0] * day / (R * np.cos(np.radians(lat))) * 180.0 / np.pi   # degrees of longitude per day
v = vel[:, 1] * day / R * 180.0 / np.pi                               # degrees of latitude per day

# w = 0: this lesson traces particles on ONE depth level, so vertical motion is switched off.
# (w is in m/s, not degrees/day; a 3-D version would only need w * day -> m/day, because z is in metres.)
w = np.zeros_like(u)

# Stack u, v, w as three columns (N x 3) and store them as a new point array 'velocity_deg'
output.PointData.append(np.column_stack((u, v, w)), 'velocity_deg')
