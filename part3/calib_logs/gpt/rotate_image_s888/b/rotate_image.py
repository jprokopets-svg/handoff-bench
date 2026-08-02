def rotate(matrix: list[list[int]]) -> None:
    """Rotate n x n matrix 90 degrees clockwise in place.

    Modifies the input matrix and returns None.

    Behavior:
    - If matrix is an empty list ([]) or has empty first row (e.g. [[]]), do nothing and return None.
    - If matrix is not square (rows lengths differ from number of rows), raises ValueError.
    """
    # Handle empty matrix or empty rows: no-op
    if not matrix:
        return None
    if not matrix[0]:
        # treat as no-op for empty-row matrix
        return None

    n = len(matrix)
    # Validate square
    for row in matrix:
        if len(row) != n:
            raise ValueError("matrix must be square")

    # Transpose in-place
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for row in matrix:
        row.reverse()

    return None
