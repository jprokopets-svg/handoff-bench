
def find_duplicate(nums: list[int]) -> int:
    # Floyd's Cycle Finding algorithm
    # Phase 1: Find the intersection point of the two runners.
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find the "entrance" to the cycle.
    # The distance from the start to the entrance of the cycle is the same
    # as the distance from the intersection point to the entrance of the cycle.
    ptr1 = nums[0]
    ptr2 = slow

    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1
