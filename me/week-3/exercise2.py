import numpy as np


A= np.array([[1, 2], [3, 4]])

print("Determinant of A:", np.linalg.det(A))

print ("Inverse of A:\n", np.linalg.inv(A))
print("Eigenvalues of A:", np.linalg.eigvals(A))
print("Eigenvectors of A:\n", np.linalg.eig(A)[1])

U, S, V = np.linalg.svd(A)
print("Singular values of A: \n", S)
print("U (left singular vectors) : \n", U)
print("V (right singular vectors) : \n", V)