def rotate(matrix: list[list[int]]) -> None:
    """
    Rotate an n x n matrix 90 degrees clockwise in place.
    
    Args:
        matrix: A square matrix (list of lists) to be rotated in place.
    
    Returns:
        None (the matrix is modified in place)
    """
    n = len(matrix)
    
    # Step 1: Transpose the matrix (swap rows and columns)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()