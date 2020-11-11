import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        Consider the case we know for sure they are all mines:
        if {E,F,G} == 3, they must all be mines for example. So return this set.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        Consider the case we KNOW for sure they are all safe:
        if {E,F,F} == 0 for example, they must all be safe! return this set.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            # count represents number of cells that are mines.
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        Update Sentence so cell no longer in this?
        """
        if cell in self.cells:
            # remove but do not update count as we do not know anything else.
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def nearby_cells(self, cell):

        neighbours = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        return neighbours

    def add_knowledge(self, cell, count):

       # Mark cell as a move that has been made
        self.moves_made.add(cell)

        # Mark cell as safe
        self.mark_safe(cell)

        # New sentence
        neighbours = self.nearby_cells(cell)
        # Remove safes and moves that have been made from neighbours set.
        neighbours -= self.safes | self.moves_made
        new_sentence = Sentence(neighbours, count)
        self.knowledge.append(new_sentence)

        # 4) If new cells can be marked as safe or as mines, then the function should do so.
        new_safes = set()
        new_mines = set()

        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                new_mines.add(cell)
            for cell in sentence.known_safes():
                new_safes.add(cell)

        for cell in new_mines:
            self.mark_mine(cell)
        for cell in new_safes:
            self.mark_safe(cell)

       # Remove empty sentences from KB.
        for sentence in self.knowledge:
            if sentence == Sentence(set(), 0):
                self.knowledge.remove(sentence)

      # 5) subset method - add new sentences if they can be inferred from existing knowledge
        new_knowledge = []
        for set1 in range(len(self.knowledge)):
            for set2 in range(len(self.knowledge)):

                set_1 = self.knowledge[set1]
                set_2 = self.knowledge[set2]

                # set1 is a subset of set2
                if set_1.cells.issubset(set_2.cells):
                    new_cells = set_2.cells - set_1.cells
                    new_count = set_2.count - set_1.count
                    new_sentence = Sentence(new_cells, new_count)
                    new_knowledge.append(new_sentence)

                # set2 is a subset of set1
                elif set_2.cells.issubset(set_1.cells):
                    new_cells = set_1.cells - set_2.cells
                    new_count = set_1.count - set_2.count
                    new_sentence = Sentence(new_cells, new_count)
                    new_knowledge.append(new_sentence)

                else:
                    return None

        # add our new_knowledge to KB.
        for sentence in new_knowledge:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safes_left = self.safes - self.moves_made

        if safes_left:
            return safes_left.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_cell = (random.randrange(self.height),
                       random.randrange(self.width))

        random_set = self.mines | self.moves_made

        for i in range(0, self.height):
            for j in range(0, self.width):
                cell = i, j
                if cell not in random_set:
                    return random_cell
                else:
                    return None
