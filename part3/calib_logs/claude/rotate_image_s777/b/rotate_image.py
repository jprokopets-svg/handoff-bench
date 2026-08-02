def rotate(matrix: list[list[int]]) -> None:
    """
    Rotates an n x n matrix 90 degrees clockwise in-place.
    
    Algorithm:
    1. Transpose the matrix (swap elements across the main diagonal)
    2. Reverse each row
    
    This achieves a 90-degree clockwise rotation.
    
    Example:
        [[1,2,3],       [[7,4,1],
         [4,5,6],  -->   [8,5,2],
         [7,8,9]]        [9,6,3]]
    """
    n = len(matrix)
    
    # Step 1: Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
