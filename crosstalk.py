import numpy as np
from numpy.linalg import inv

# you should measure your outputs and enter them here
K_F = np.array([[1.9633,0.0305,-0.0524],
                [-0.0618,2.0473,0.0339],
                [0.0421,-0.0828,2.105]])

F = 5

K = K_F/F

Kinv = inv(K)

print(Kinv)

print(np.matmul(Kinv,K)) # ? identity matrix