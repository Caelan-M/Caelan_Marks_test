# Your goal for this question is to write a program that accepts two lines (x1,x2) and
# (x3,x4) on the x-axis and returns whether they overlap. As an example, (1,5) and
# (2,6) overlaps but not (1,5) and (6,8).


# Assumes input points are tuples (x1, x2) and (x3, x4) where x2 > x1 and x4 > x3
# Also assumes that when lines are touching (ex: (0, 1), (1, 2)) that they are not overlapping
def overlap(line1, line2):
    if line1[0] < line2[0]:
        if line1[1] > line2[0]:
            return True
    elif line2[1] > line1[0]:
        return True

    return False


test_cases = [[(0, 2), (1, 3), True],  # Partial overlap, True
              [(1, 3), (0, 2), True],  # Partial overlap, True
              [(-1, 0), (1, 2), False],  # No overlap not touching, False
              [(1, 2), (-1, 0), False],  # No overlap not touching, False
              [(0, 1), (1, 2), False],  # No overlap touching, False
              [(1, 2), (0, 1), False],  # No overlap touching, False
              [(0, 1), (-1, 2), True],  # Complete overlap, True
              [(-1, 2), (0, 1), True]]  # Complete overlap, True

test_pass = True
for test in test_cases:
    if overlap(test[0], test[1]) != test[2]:
        print('Test fail, case: ' + str(test))
        test_pass = False
        break

if test_pass:
    print('All tests pass!')
