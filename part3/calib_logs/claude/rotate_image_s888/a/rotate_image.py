def rotate(matrix):
    """
    Rotate an n x n matrix 90 degrees clockwise in-place.
    
    Args:
        matrix: A list of lists representing an n x n matrix
        
    Returns:
        None (modifies matrix in-place)
    """
    n = len(matrix)
    
    # Step 1: Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
