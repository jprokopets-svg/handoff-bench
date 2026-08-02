def rotate(matrix: list[list[int]]) -> None:
    """Rotate the n x n matrix 90 degrees clockwise in place.

    The function modifies the input matrix and returns None.
    """
    # Handle empty matrix or empty rows: nothing to do
    if not matrix or not matrix[0]:
        return None

    n = len(matrix)
    # Transpose in place
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for row in matrix:
        row.reverse()

    return None
