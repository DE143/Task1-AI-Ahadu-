import numpy as np 
#create addition 
A= np.array([[1,2],[3,4]])
# B= np.array([[5,6],[7,8]])
# print("Addition of A and B is: \n", A+B)
# #Create subtraction
# print("Subtraction of A and B is: \n", A-B)
# #Create multiplication
# print("Multiplication of A and B is: \n", A*B)

# perform vector addition
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
vector_addition = v1 + v2
# print("Vector Addition:", vector_addition) 

# special matrix operations
# # Transpose of a matrix
# print("Transpose of A is: \n", A.T)
# # Inverse of a matrix
# print("Inverse of A is: \n", np.linalg.inv(A))
# # Determinant of a matrix
# print("Determinant of A is: ", np.linalg.det(A))


# Eigenvalues and Eigenvectors
# eigenvalues, eigenvectors = np.linalg.eig(A)
# print("Eigenvalues of A are: ", eigenvalues)
# print("Eigenvectors of A are: \n", eigenvectors)

# Matrix Decomposition
# Singular Value Decomposition (SVD)
# U, S, V = np.linalg.svd(A)
# print("U matrix from SVD: \n", U)
# print("S matrix from SVD: \n", S)
# print("V matrix from SVD: \n", V)



Ma= np.array([[1,2,3],[4,5,6],[7,10,9]])

print("Determinant of the Matrix Ma is: \n", np.linalg.det(Ma))
print("Inverse of the Matrix Ma is: \n", np.linalg.inv(Ma))
vector= np.array([1, 0, 1])
print("Shape of the vector is: ", vector.shape)

# Matrix-Vector Multiplication
result = np.dot(Ma, vector)
print("Result of Matrix-Vector Multiplication: \n", result)
# # Matrix-Matrix Multiplication
Mb= np.array([[1,0,2],[0,1,3],[4,5,6]])
matrix_multiplication = np.dot(Ma, Mb)
print("Result of Matrix-Matrix Multiplication: \n", matrix_multiplication)
# # Eigenvalues and Eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(Ma)
print("Eigenvalues of Ma are: ", eigenvalues)
print("Eigenvectors of Ma are: \n", eigenvectors)
# Matrix devision
# To perform matrix division, we can use the concept of multiplying by the inverse of a matrix. For example, if we want to divide matrix A by matrix B, we can calculate the inverse of B and then multiply it with A:
A = np.array([[1, 2], [3, 4]])
B = np.array([[1, 0], [0, 1]])
result = np.dot(A, np.linalg.inv(B))  
print("Result of Matrix Division (A divided by B): \n", result)
# # Matrix Decomposition
U, S, Vt = np.linalg.svd(Ma)
print("U matrix from SVD: \n", U)
print("S matrix from SVD: \n", S)
print("V transpose matrix from SVD: \n", Vt )


