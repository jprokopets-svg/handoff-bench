def findMedianSortedArrays(nums1, nums2):
    """
    Find the median of two sorted arrays in O(log(min(m,n))) time.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
    
    Returns:
        The median of the two sorted arrays
    """
    # Ensure nums1 is the smaller array to optimize binary search
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    
    # Binary search on the smaller array
    low, high = 0, m
    
    while low <= high:
        partition1 = (low + high) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases for partition boundaries
        left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        right1 = float('inf') if partition1 == m else nums1[partition1]
        
        left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if we found the correct partition
        if left1 <= right2 and left2 <= right1:
            # If total length is even
            if (m + n) % 2 == 0:
                return (max(left1, left2) + min(right1, right2)) / 2.0
            # If total length is odd
            else:
                return float(max(left1, left2))
        
        # Adjust binary search bounds
        elif left1 > right2:
            high = partition1 - 1
        else:
            low = partition1 + 1
    
    return -1.0
