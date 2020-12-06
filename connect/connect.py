#!/usr/bin/env python3
# coding=utf-8
"""
The main executable file
"""


class Cell:
    """
    The size one cell on the field
    """
    width = 4
    height = 1

    def __init__(self, width=4, height=1):
        self.width = width
        self.height = height


class Game:
    """
    Main class
    """
    sequence_depth = 4  # for win
    empty_field = 0
    player_first = 1
    _player_first_mark = '  X '
    player_second = 2
    _player_second_mark = '  O '

    def __init__(self, count_lines=6, count_columns=7, cell=None):
        self._count_lines = count_lines
        self._count_columns = count_columns

        # empty field
        self._game_field_state = [[Game.empty_field for _ in range(self._count_columns)]
                                  for _ in range(self._count_lines)]

        # printed logic
        self._cell = cell or Cell()
        self._vertical_separator = '_' * self._cell.width  # The separator between showed cell
        self._horizontal_separator = '|' * self._cell.height  # The separator between showed cell
        self._blank = ' ' * self._cell.width

    def show_game_field(self):
        """
        Field is printed in console.
        """
        for line_states in self._game_field_state:
            print(self._vertical_separator * self._count_columns)
            print(self._horizontal_view(line_states))

        print(self._vertical_separator * self._count_columns)
        print('  ' + self._blank.join(str(i) for i in range(1, self._count_columns + 1)))

    def _horizontal_view(self, line_states: list):

        view = f'{self._horizontal_separator}'
        for cell_val in line_states:
            if cell_val == self.player_first:
                view = f'{view}{self._player_first_mark}{self._horizontal_separator}'
            elif cell_val == self.player_second:
                view = f'{view}{self._player_second_mark}{self._horizontal_separator}'
            else:
                view = f'{view}{self._blank}{self._horizontal_separator}'
        return view

    def player_choice(self):
        choice = int(input("Please select an empty space between 1 and 7: ")) - 1
        while self._game_field_state[0][choice] != Game.empty_field:
            choice = int(input("This column is marked. Please choose another one: "))
        return choice

    def marker(self, player):
        if player == self.player_first:
            return self._player_first_mark
        return self._player_second_mark

    def _is_cell_available(self, column: list):
        column = list(reversed(column))
        for i, item in enumerate(column):
            if item == self.empty_field:
                return len(column) - i - 1
        return False

    def _single_column(self, column):
        """
        :return: single column states
        """
        return [self._game_field_state[line][column] for line in range(self._count_lines)]

    def is_empty_cells_in_field(self):
        """
        Does the field contain empty cell
        """
        top_line = self._game_field_state[0]
        for i, col in enumerate(top_line):
            if col == self.empty_field:
                return True
        return False

    def check_winner(self, marker):
        """
        Check all columns and line
        """
        for line in self._game_field_state:
            if self._check_four_connect(line, marker):
                return True

        for i in range(self._count_lines):
            col = self._single_column(i)
            if self._check_four_connect(col, marker):
                return True

        return False

    @staticmethod
    def _check_four_connect(line, marker):
        """
        Check one line
        """
        string = ''.join(str(i) for i in line)
        substring = str(marker) * 4
        if substring in string:
            return True

    def step(self, player, column):
        """
        One move in game
        """
        single_col = self._single_column(column)
        line_index = self._is_cell_available(single_col)
        if line_index is not False:
            self._game_field_state[line_index][column] = player
            return True
        return False


if __name__ == '__main__':
    game = Game()

    current_player = game.player_first
    print('Player 1 will be X. Player 2 will be O.')

    while not game.check_winner(current_player):
        game.show_game_field()

        choice = game.player_choice()
        game.step(current_player, choice)

        if not game.is_empty_cells_in_field():
            print('Nobody wins. The board is filled up.')
            break

        current_player = game.player_second if current_player == game.player_first else game.player_first
    else:
        print(f'The player {current_player} wins.')
        game.show_game_field()
