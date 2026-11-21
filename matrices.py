def multiply_matrix_by_vector(matrix, vector):
    result = [0, 0, 0, 0]

    for row in range(4):
        total = 0
        for i in range(4):
            total = total + matrix[row][i] * vector[i]
        result[row] = total

    return result
