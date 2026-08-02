def rotate(matrix: list[list[int]]) -> None:
    """
    Rotate an n x n matrix 90 degrees clockwise in-place.
    
    Algorithm:
    1. Transpose the matrix (swap elements across the main diagonal)
    2. Reverse each row
    
    Time Complexity: O(n²) where n is the dimension of the matrix
    Space Complexity: O(1) - only swaps, no extra space allocated
    
    Args:
        matrix: An n x n matrix represented as a list of lists
        
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
