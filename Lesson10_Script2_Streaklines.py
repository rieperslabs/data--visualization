import numpy as np
from vtkmodules.vtkCommonDataModel import vtkCellArray

# Particle Tracer output: points only, no cells, plus one value per particle in these arrays
seed = inputs[0].PointData['InjectedPointId']   # which seed point released the particle (0, 1, ...)
age  = inputs[0].PointData['ParticleAge']       # how long the particle has travelled (days)

# vtkCellArray holds the connectivity: which point ids make up each cell (here: each line)
lines = vtkCellArray()

# np.unique(seed) gives each seed id once, e.g. [0, 1, 2, 3], so we build one streakline per seed point
for s in np.unique(seed):
    ids = np.where(seed == s)[0]           # point ids of all particles from this seed point ...
    ids = ids[np.argsort(age[ids])]        # ... sorted from youngest (at the seed) to oldest
    lines.InsertNextCell(len(ids))         # start a new line cell that will have len(ids) points
    # add the point ids to this line in sorted order; VTK expects plain Python int, not numpy int
    for i in ids:
        lines.InsertCellPoint(int(i))

output.ShallowCopy(inputs[0].VTKObject)    # keep the particles and their arrays (no data copy)
output.SetLines(lines)                     # and add one line per seed point
