def rotate(matrix):
    """Rotate the n x n matrix 90 degrees clockwise in place.

    Modifies the input matrix and returns None.
    """
    if not matrix:
        return None
    n = len(matrix)
    # transpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # reverse each row
    for i in range(n):
        matrix[i].reverse()
    return None
