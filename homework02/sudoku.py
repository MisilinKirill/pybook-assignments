import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    c1 = []
    qw = []
    r = 0
    for i in values:
        r += 1
        qw += [i]
        if r % n == 0 or r == len(values):
            c1 += [qw]
            qw = []
    return c1

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    c1 = []
    for i in grid:
        c1 += [i[pos[1]]]
    return c1


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    if pos[0] < 3:
        x = 0
    elif 3 <= pos[0] < 6:
        x = 3
    else:
        x = 6
    if pos[1] < 3:
        y = 0
    elif 3 <= pos[1] < 6:
        y = 3
    else:
        y = 6
    return grid[x][y:y + 3] + grid[x + 1][y:y + 3] + grid[x + 2][y:y + 3]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    x = -1
    for i in range(len(grid)):
        if '.' in grid[i]:
            x = i
            break
    for i in range(len(grid[x])):
        if grid[x][i] == '.':
            y = i
            break
    if x == -1:
        return(False)
    else:
        return (x, y)



def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    v = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    x = set(get_row(grid, pos))
    x.update(set(get_col(grid, pos)))
    x.update(set(get_block(grid, pos)))
    return (v - x)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    q = find_empty_positions(grid)
    if q:
        v = find_possible_values(grid, q)
        if len(v) != 0:
            for i in v:
                grid[q[0]][q[1]] = i
                x = solve(grid)
                if x:
                    return x
                else:
                    grid[q[0]][q[1]] = '.'

        else:
            return False
    else:
        return grid



def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    if find_empty_positions(solution):
        return False
    for i in range(9):
        x = get_row(solution, (i, 0))
        y = get_col(solution, (0, i))
        z = get_block(solution, ((i // 3 * 3), (i % 3 * 3)))
        if len(x) == len(set(x)) and len(y) == len(set(y)) and len(z) == len(set(z)):
            ...
        else:
            return False
    return True

import random

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    c = [['1', '2', '3', '4', '5', '6', '7', '8', '9'],
         ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
         ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
         ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
         ['5', '6', '7', '8', '9', '1', '2', '3', '4'],
         ['8', '9', '1', '2', '3', '4', '5', '6', '7'],
         ['3', '4', '5', '6', '7', '8', '9', '1', '2'],
         ['6', '7', '8', '9', '1', '2', '3', '4', '5'],
         ['9', '1', '2', '3', '4', '5', '6', '7', '8']]
    if N >= 81:
        N = 81
    b = 81 - N
    while b > 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if c[y][x] != '.':
            c[y][x] = '.'
            b -= 1
    return c


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
