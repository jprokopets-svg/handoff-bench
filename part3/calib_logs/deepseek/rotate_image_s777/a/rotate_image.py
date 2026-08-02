def rotate(matrix):
    """
    Rotate an n x n matrix 90 degrees clockwise in place.
    
    Args:
        matrix: List[List[int]] - The matrix to rotate (modified in place)
    
    Returns:
        None
    """
    n = len(matrix)
    
    # Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()