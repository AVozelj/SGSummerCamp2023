import numpy as np
from numpy.linalg import inv

# you should measure your outputs and enter them here
K_F = np.array([[0.29036,-0.02254,-0.05431],
                [0.06846,-0.33893,-0.39122],
                [0.41231,0.19171,-0.24230]])

F = np.array([909,-837,706])

K = K_F/F

Kinv = inv(K)

print(Kinv)

print(np.matmul(Kinv,K)) # ? identity matrix