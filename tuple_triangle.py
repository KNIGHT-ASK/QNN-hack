# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 03:34:28 2025

@author: Lydia_Blackwell_Esslami
"""
def generate_inner_list(z):
    inner_list = []
    
    # Block for ODD z
    if z % 2 == 1:
        # Since z is odd, the largest odd number <= z is simply z itself.
        max_start = z
        # i goes 1, 3, 5, ...
        for i in range(1, max_start + 1, 2):
            inner_list.append((i, i + 1))
    
    # Block for EVEN z
    elif z % 2 == 0:
        # Since z is even, the largest even number <= z is simply z itself.
        max_start = z
        # i goes 2, 4, 6, ...
        for i in range(2, max_start + 1, 2):
            inner_list.append((i, i + 1))
            
    return inner_list


def inverted_pyramid(n):
    """Gets tuples with the inverted pyramid entanglement algorythm"""
    output_list = []
    for x in range(1,n):
        inner_list = generate_inner_list(x)
        output_list.append(inner_list)
    for y in range(n-2,0, -1):
        inner_list = generate_inner_list(y)
        output_list.append(inner_list)
    
    return output_list

#print(inverted_pyramid(10))

def pyramid(n):
    """Gets tuples with the pyramid entanglement algorithm
    
    Builds from top-down: starts with highest qubit pairs and works down
    PARAMETERIZED VERSION - works for any number of qubits
    
    Args:
        n: number of qubits (will create pairs up to (n-1, n))
    """
    output_list = []
    
    def generate_pyramid_list_ascending(z, max_qubit):
        """Generate pyramid pattern for ascending phase (includes lowest pair)"""
        inner_list = []
        
        if z % 2 == 1:
            # Odd z: Start from highest odd pair and work down
            # Highest odd pair is (max_qubit-1, max_qubit) if max_qubit is even
            start_i = max_qubit - 1 if max_qubit % 2 == 0 else max_qubit - 2
            
            # Work down by 2s: (9,10), (7,8), (5,6), (3,4), (1,2)
            for i in range(start_i, 0, -2):
                # Include pair if z is large enough
                # Each step down requires z to be 2 larger
                steps_from_top = (start_i - i) // 2
                if z >= 1 + (steps_from_top * 2):
                    inner_list.append((i, i + 1))
        
        elif z % 2 == 0:
            # Even z: Start from highest even pair and work down
            # Highest even pair is (max_qubit-1, max_qubit) if max_qubit is odd
            start_i = max_qubit - 1 if max_qubit % 2 == 1 else max_qubit - 2
            
            # Work down by 2s: (8,9), (6,7), (4,5), (2,3)
            for i in range(start_i, 1, -2):
                # Include pair if z is large enough
                steps_from_top = (start_i - i) // 2
                if z >= 2 + (steps_from_top * 2):
                    inner_list.append((i, i + 1))
        
        return inner_list
    
    def generate_pyramid_list_descending(z, max_qubit):
        """Generate pyramid pattern for descending phase (excludes lowest pair)"""
        inner_list = []
        
        if z % 2 == 1:
            # Odd z: Start from highest odd pair, exclude (1,2)
            start_i = max_qubit - 1 if max_qubit % 2 == 0 else max_qubit - 2
            
            for i in range(start_i, 2, -2):  # Stop at 2 to exclude (1,2)
                steps_from_top = (start_i - i) // 2
                if z >= 1 + (steps_from_top * 2):
                    inner_list.append((i, i + 1))
        
        elif z % 2 == 0:
            # Even z: Same as ascending for even
            start_i = max_qubit - 1 if max_qubit % 2 == 1 else max_qubit - 2
            
            for i in range(start_i, 1, -2):
                steps_from_top = (start_i - i) // 2
                if z >= 2 + (steps_from_top * 2):
                    inner_list.append((i, i + 1))
        
        return inner_list
    
    # Ascending phase: x = 1 to n-1
    for x in range(1, n):
        output_list.append(generate_pyramid_list_ascending(x, n))
    
    # Descending phase: y = n down to 1
    for y in range(n, 0, -1):
        output_list.append(generate_pyramid_list_descending(y, n))
    
    return output_list

    
        
print(pyramid(10))



