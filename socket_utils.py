
import numpy as np

size = (1920, 1080, 3)

mat = np.random.randint(0, 255, size, dtype=np.uint8)
mv_mat = memoryview(mat) # buffer_like
nbytes = mv_mat.nbytes
