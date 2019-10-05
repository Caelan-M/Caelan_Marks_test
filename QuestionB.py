# The goal of this question is to write a software library that accepts 2 version string
# as input and returns whether one is greater than, equal, or less than the other.
# As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of.


def version(version1, version2):
    if version1 == version2:
        return version1 + ' is equal to ' + version2

    v1 = version1.split('.')
    v2 = version2.split('.')

    for i in range(len(v1)):
        if v1[i] > v2[i]:
            return version1 + ' is greater than ' + version2
        elif v2[i] > v1[i]:
            return version1 + ' is less than ' + version2

    return print('Something has gone wrong, shouldn\'t be here.')


test_cases = [['1.0', '1.1', '1.0 is less than 1.1'],
              ['1.1', '1.0', '1.1 is greater than 1.0'],
              ['1.0', '1.0', '1.0 is equal to 1.0'],
              ['1.0', '2.0', '1.0 is less than 2.0'],
              ['2.0', '1.0', '2.0 is greater than 1.0'],
              ['2.0', '1.1', '2.0 is greater than 1.1'],
              ['1.0.0', '1.1.0', '1.0.0 is less than 1.1.0'],
              ['1.1.1', '1.1.0', '1.1.1 is greater than 1.1.0'],
              ['1.0.0', '1.0.0', '1.0.0 is equal to 1.0.0'],
              ['1.0.2', '1.0.1', '1.0.2 is greater than 1.0.1'],
              ['2.0.2', '1.1.3', '2.0.2 is greater than 1.1.3'],
              ['2.0.2', '2.22.0', '2.0.2 is less than 2.22.0']]

test_pass = True
for test in test_cases:
    if version(test[0], test[1]) != test[2]:
        print('Test fail, case: ' + str(test))
        test_pass = False
        break

if test_pass:
    print('All tests pass!')
