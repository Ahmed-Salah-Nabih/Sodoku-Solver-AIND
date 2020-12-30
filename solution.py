
#encode the board
rows ='ABCDEFGHI'
cols ='123456789'
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

#we must define the diagonal units 
diagonal_units= [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
assignments =[]
def cross(A,B):
    return [s+t for s in A for t in B]

boxes = cross(rows , cols)

row_units    =[cross(r ,cols)  for r in  rows]
cols_units   =[cross(rows,c) for c in cols]
square_units =[cross(rs , cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units +cols_units + square_units+diagonal_units
unitlist = unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#-----------------------------------------------------------------------------------
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

#-----------------------------------------------------------------------------------
def grid_value(grid):
    values =[]
    all_digits='123456789'

    for c in grid:
        if c =='.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)

    assert len(grid)== 81
    return dict(zip(boxes, values))

display(grid_value(grid))

#eliminate  solved values from peers
#-----------------------------------------------------------------------------------
def eliminate(values):

     solved_values = [box for box in values.keys() if len(values[box]) == 1]
     for box in solved_values:
         digit = values[box]
         for peer in peers[box]:
             values[peer]=values [peer].replace(digit,'')

     return values


#following function assign a value to boxes with only one number
#-----------------------------------------------------------------------------------
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len (dplaces)== 1:
                values[dplaces[0]] = digit
        return values
#-----------------------------------------------------------------------------------


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
#-----------------------------------------------------------------------------------


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

    # -----------------------------------------------------------------------------------
        # the following function is to update the values dictionary
        # it assigns value to a given box
        def assign_values(values, box, value):


            values[box] == value
            if len(value) == 1:
                assignments.append(values.copy())
            return values

    # -----------------------------------------------------------------------------------

    def naked_twin (values):
        #create a unit_counter to search every unit in unitlist including the diagonals
        
        for unit_counter in unitlist:
        
        #this will be created for the four elements in the unitlist 
        
            twins=[]
        #create to counters box and secondary_box
            for box in unit_counter:
                for secondary_box in unit_counter:
        #now we check for every box that has two values and with its values present in another box
                        if (len(values[box])==2) and secondary_box != box and (values[box]==values[secondary_box]):
                            twins.append(secondary_box)
                #by now we have stored the secondary_box value in twins=[]
            if(twins):
                       # For each of the values in any twin...
              for digit in values[twins[0]]:
                           # Check every box in the unit
                  for box in unit_counter:
                               # Get the value for every box in the unit
                      val = values[box]
                                # Check if the values of that box contain twin numbers
                      if digit in val and box not in twins:
                                # If they do, remove them from the box
                                  assign_value(values, box, values[box].replace(digit, ''))
                                  # Return the values after the twins have been removed
            return values
                    
          
  # -----------------------------------------------------------------------------------

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_value(grid)
    solved_sodoku = search(values)
    return solved_sodoku



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

        