assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins_type(i,values,peers):
        nakedtwins=[]
        value=values[i]
        unsolved_peers=[k for k in peers if len(values[k])!=1]
        for peer in unsolved_peers:
            if values[peer]==value:
               nakedtwins.append(peer)
        if len(nakedtwins)>0:
          twinvalue=values[nakedtwins[0]]
          for peer in unsolved_peers:
            if peer not in nakedtwins:
                for j in twinvalue:
                  values[peer]=values[peer].replace(j,'')
        return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    unsolved_values=[j for j in values.keys() if len(values[j])==2]
    for i in unsolved_values:
        naked_twins_type(i,values,rowpeers[i])
        naked_twins_type(i,values,colpeers[i])
        naked_twins_type(i,values,sqrpeers[i])
                

    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
rowunits = dict((s, [u for u in row_units if s in u]) for s in boxes)
rowpeers=dict((s, set(sum(rowunits[s],[]))-set([s])) for s in boxes)
rowunits = dict((s, [u for u in row_units if s in u]) for s in boxes)
rowpeers=dict((s, set(sum(rowunits[s],[]))-set([s])) for s in boxes)
colunits = dict((s, [u for u in column_units if s in u]) for s in boxes)
colpeers=dict((s, set(sum(colunits[s],[]))-set([s])) for s in boxes)
sqrunits = dict((s, [u for u in square_units if s in u]) for s in boxes)
sqrpeers=dict((s, set(sum(sqrunits[s],[]))-set([s])) for s in boxes)



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    updated=[]
    value='123456789'
    for i in grid:
     if i=='.':
         updated.append(value)
     else:
         updated.append(i)
    return dict((zip(boxes,updated)))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values=[j for j in values.keys() if len(values[j])==1]
    diapeers1=['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    diapeers2=['A9','B8','C7','D6','E5','F4','G3','H2','I1']
    for i in solved_values:
        value=values[i]
        if i in diapeers1:
            diapeers1.remove(i)
            updatedpeers=peers[i].union(diapeers1)
        elif i in diapeers2:
            diapeers2.remove(i)
            updatedpeers=peers[i].union(diapeers2)
        else:
            updatedpeers=peers[i]
        for peer in updatedpeers:
            values[peer]=values[peer].replace(value,'')
    return values
 
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
            
    for value in values[s]:
        new_sudoku = values.copy() 
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(grid_values(diag_sudoku_grid))
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
