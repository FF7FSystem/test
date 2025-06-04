"""ЗАДАЧА: Number of Islands
Дан 2D массив из '1' (суша) и '0' (вода).
Остров - это группа соседних (по горизонтали/вертикали) клеток суши.
Найти количество островов.
ТРЕБОВАНИЯ:
- Написать функцию numIslands(grid)
- Временная сложность: O(m*n)
- Пространственная сложность: O(min(m,n)) для BFS или O(m*n) для DFS
НУЖНО ПРЕДОСТАВИТЬ:
1. Рабочий код на Python/иной на выбор
2. Комментарии к ключевым местам
3. Тесты на примерах из задачи
4. Краткое объяснение выбранного подхода (2-3 предложения)
ОПЦИОНАЛЬНО:
5. Попробуйте реализовать как через DFS, так и через BFS"
6. Подумайте над модификацией: как найти размер самого большого острова?
Input: grid = [
["1","1","1","1","0"],
["1","1","0","1","0"],
["1","1","0","0","0"],
["0","0","0","0","0"]
]
Output: 1
Input: grid = [
["1","1","0","0","0"],
["1","1","0","0","0"],
["0","0","1","0","0"],
["0","0","0","1","1"]
]
"""

def numIslands_vers_1(grid: list) -> int:
    """
    All the pieces of the map are bypassed.
    Each piece is checked to see if its neighbors on the right or left are part of existing islands.
    If this happens, then the current piece is added to the set of this island.
    If its direct neighbors are in contact with two different islands, then these islands (their sets) are combined.
    :param grid: list
    :return: int
    """
    horizontal_size = len(grid)
    vertical_size = len(grid[0])
    islands = []
    LAND = "1"

    for horizontal in range(horizontal_size):
        for vertical in range(vertical_size):
            if grid[horizontal][vertical] != LAND:
                continue

            current_coordinates = (horizontal, vertical)
            horizontal_contact = (horizontal - 1, vertical)
            vertical_contact = (horizontal, vertical - 1)
            consists_of_islands = set()

            if not islands:
                islands.append({current_coordinates, })
                continue

            for contact in (horizontal_contact, vertical_contact):
                for island_index, island in enumerate(islands):

                    if contact in island and not consists_of_islands:
                        island.add((horizontal, vertical))
                        consists_of_islands.add(island_index)

                    elif contact in island and consists_of_islands:
                        consists_of_islands.add(island_index)

            if not consists_of_islands: #new island
                islands.append({current_coordinates, })

            elif len(consists_of_islands) > 1: # merge island
                islands_for_merge = [islands.pop(i) for i in sorted(consists_of_islands, reverse=True)] #do pop from the end
                islands.append(set.union(*islands_for_merge))

    return len(islands)


def numIslands_vers_2(grid: list) -> int:
    """
    The idea of the function is that it goes through the array and checks if this piece has contact with others.
    If there is no contact, it means it is new, We have found a new island, hooray (the island counter is increasing).
    If there is a contact, then this piece is part of another island, too, nothing
    ((the island counter does not change)). If this piece is in contact with the second section,
    it means that 2 islands connect at this point (the island counter decreases).

    This works because the map is processed sequentially, line by line, from index 0 to the largest

    :param grid: list
    :return: int
    """
    horizontal_size = len(grid)
    vertical_size = len(grid[0])
    islands_cnt = 0
    LAND = "1"
    WATER = "0"

    for horizontal in range(horizontal_size):
        for vertical in range(vertical_size):
            if grid[horizontal][vertical] == WATER:
                continue

            already_contacted_with_land = False
            horizontal_contact = grid[horizontal - 1][vertical] if horizontal - 1 >= 0 else None
            vertical_contact = grid[horizontal][vertical - 1] if vertical - 1 >= 0 else None

            for contact in (horizontal_contact, vertical_contact):
                if contact and contact == LAND:
                    if not already_contacted_with_land:
                        already_contacted_with_land = True
                    else:
                        islands_cnt -= 1

            # still not contacted with anyone
            if not already_contacted_with_land:
                islands_cnt += 1

    return islands_cnt


grid = [
    ["1", "0", "1", "1", "1"],
    ["1", "0", "1", "0", "1"],
    ["1", "0", "1", "0", "1"],
    ["1", "1", "1", "0", "1"]
]

print(f"func 1: Number of islands => {numIslands_vers_1(grid)}")
print(f"func 2: Number of islands => {numIslands_vers_2(grid)}")

grid = [
    ["1", "1", "0", "1", "1"],
    ["0", "1", "1", "1", "0"],
    ["0", "0", "1", "0", "0"],
    ["1", "0", "1", "1", "1"]
]

print(f"func 1: Number of islands => {numIslands_vers_1(grid)}")
print(f"func 2: Number of islands => {numIslands_vers_2(grid)}")
