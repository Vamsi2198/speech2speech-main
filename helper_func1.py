

def find_common_strings(matrix):
    """
    Given a matrix of arrays containing strings, return a set of the common strings.
    """
    if not matrix:
        return set()
    
    common_strings = set(matrix[0])
    for i in range(1, len(matrix)):
        common_strings &= set(matrix[i])
    
    return common_strings

if '__name__'=='__main__':
    find_common_strings(matrix)