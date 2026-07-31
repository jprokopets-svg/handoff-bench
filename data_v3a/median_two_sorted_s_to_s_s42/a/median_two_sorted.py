def find_median_sorted_arrays(nums1, nums2):
    """
    Find the median of two sorted arrays in O(log(min(m, n))) time.

    Args:
        nums1: First sorted array
        nums2: Second sorted array

    Returns:
        The median value as a float
    """
    # Ensure nums1 is the smaller array for binary search efficiency
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2

    low, high = 0, m

    while low <= high:
        i = (low + high) // 2   # partition index for nums1
        j = half_len - i         # partition index for nums2

        if i < m and nums2[j - 1] > nums1[i]:
            # Move partition in nums1 to the right
            low = i + 1
        elif i > 0 and nums1[i - 1] > nums2[j]:
            # Move partition in nums1 to the left
            high = i - 1
        else:
            # Found the correct partition
            # Determine max of left side
            if i == 0:
                max_left = nums2[j - 1]
            elif j == 0:
                max_left = nums1[i - 1]
            else:
                max_left = max(nums1[i - 1], nums2[j - 1])

            # If total length is odd, median is max_left
            if (m + n) % 2 == 1:
                return float(max_left)

            # Determine min of right side
            if i == m:
                min_right = nums2[j]
            elif j == n:
                min_right = nums1[i]
            else:
                min_right = min(nums1[i], nums2[j])

            return (max_left + min_right) / 2.0

    raise ValueError("Input arrays are not sorted or are invalid.")
