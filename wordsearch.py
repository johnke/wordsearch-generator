#!/usr/bin/env python3
"""
Word Search Generator - Creates an SVG word search puzzle from a list of words in a text file.
"""

import random
import argparse
import string
from typing import List, Tuple


class WordSearchGenerator:
    def __init__(self, size: int = 15, max_attempts: int = 100):
        """
        Initialize the word search generator.

        Args:
            size: Size of the grid (square)
            max_attempts: Maximum attempts to place a word before giving up
        """
        self.size = size
        self.max_attempts = max_attempts
        self.grid = [[" " for _ in range(size)] for _ in range(size)]
        self.placed_words = []
        self.word_positions = {}  # Maps words to lists of positions

    def read_words_from_file(self, filename: str) -> List[str]:
        """Read words from a text file, one word per line."""
        words = []
        with open(filename, "r") as f:
            for line in f:
                word = line.strip().upper()
                if word and len(word) <= self.size:
                    words.append(word)
        return words

    def can_place_word(
        self, word: str, row: int, col: int, direction: Tuple[int, int]
    ) -> bool:
        """Check if a word can be placed at the given position and direction."""
        dr, dc = direction

        # Check if the word fits on the grid and doesn't clash with existing letters
        for i, char in enumerate(word):
            r, c = row + i * dr, col + i * dc

            # Check if position is out of bounds
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False

            # Check if cell is empty or has the same character
            if self.grid[r][c] != " " and self.grid[r][c] != char:
                return False

        return True

    def place_word(self, word: str) -> bool:
        """Try to place a word on the grid. Return True if successful."""
        word = word.upper()

        # Possible directions: horizontal, vertical, diagonal
        directions = [
            (0, 1),  # right
            (1, 0),  # down
            (1, 1),  # down-right
            # (1, -1),  # down-left
            # (0, -1),  # left
            # (-1, 0),  # up
            # (-1, -1), # up-left
            (-1, 1),  # up-right
        ]

        # Shuffle directions to ensure we don't bias toward any direction
        random.shuffle(directions)

        # Count successful placements in each direction to monitor distribution
        _ = {(dr, dc): 0 for dr, dc in directions}

        # Try random positions and directions
        for attempt in range(self.max_attempts):
            # Cycle through directions
            direction_index = attempt % len(directions)
            direction = directions[direction_index]
            dr, dc = direction

            # Adjust starting position based on direction to ensure the word fits
            max_row = self.size - 1 if dr == 0 else self.size - len(word) * abs(dr)
            max_col = self.size - 1 if dc == 0 else self.size - len(word) * abs(dc)
            min_row = 0 if dr >= 0 else len(word) - 1
            min_col = 0 if dc >= 0 else len(word) - 1

            if max_row < min_row or max_col < min_col:
                continue

            row = random.randint(min_row, max_row)
            col = random.randint(min_col, max_col)

            # Check if the word can be placed
            if self.can_place_word(word, row, col, direction):
                # Place the word
                positions = []
                for i, char in enumerate(word):
                    r, c = row + i * dr, col + i * dc
                    self.grid[r][c] = char
                    positions.append((r, c))

                self.placed_words.append(word)
                self.word_positions[word] = positions
                return True

        return False

    def fill_empty_cells(self):
        """Fill empty cells with random letters."""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == " ":
                    self.grid[row][col] = random.choice(string.ascii_uppercase)

    def generate_svg(self, output_file: str, cell_size: int = 40):
        """Generate an SVG file of the word search puzzle."""
        width = self.size * cell_size
        height = self.size * cell_size + 100  # Extra space for word list

        with open(output_file, "w") as f:
            # SVG header
            f.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
            )

            # Background
            f.write(f'  <rect width="{width}" height="{height}" fill="white"/>\n')

            # Grid lines
            for i in range(self.size + 1):
                # Horizontal lines
                f.write(
                    f'  <line x1="0" y1="{i * cell_size}" x2="{width}" y2="{i * cell_size}" stroke="black" stroke-width="1"/>\n'
                )
                # Vertical lines
                f.write(
                    f'  <line x1="{i * cell_size}" y1="0" x2="{i * cell_size}" y2="{self.size * cell_size}" stroke="black" stroke-width="1"/>\n'
                )

            # Grid letters
            for row in range(self.size):
                for col in range(self.size):
                    x = col * cell_size + cell_size // 2
                    y = (
                        row * cell_size + cell_size // 2 + 5
                    )  # +5 for vertical alignment
                    f.write(
                        f'  <text x="{x}" y="{y}" font-family="Arial" font-size="{cell_size // 2}" text-anchor="middle">{self.grid[row][col]}</text>\n'
                    )

            # Word list
            f.write(
                f'  <text x="10" y="{self.size * cell_size + 30}" font-family="Arial" font-size="16" font-weight="bold">Words to find:</text>\n'
            )

            # Arrange words in columns
            words_per_column = 5
            column_width = width // ((len(self.placed_words) // words_per_column) + 1)

            for i, word in enumerate(sorted(self.placed_words)):
                column = i // words_per_column
                row = i % words_per_column
                x = 10 + column * column_width
                y = self.size * cell_size + 50 + row * 20
                f.write(
                    f'  <text x="{x}" y="{y}" font-family="Arial" font-size="14">{word}</text>\n'
                )

            # SVG footer
            f.write("</svg>\n")

    def generate_solution_svg(self, output_file: str, cell_size: int = 40):
        """Generate an SVG file showing the solution to the word search puzzle."""
        width = self.size * cell_size
        height = self.size * cell_size + 100  # Extra space for word list

        with open(output_file, "w") as f:
            # SVG header
            f.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
            )

            # Background
            f.write(f'  <rect width="{width}" height="{height}" fill="white"/>\n')

            # Grid lines
            for i in range(self.size + 1):
                # Horizontal lines
                f.write(
                    f'  <line x1="0" y1="{i * cell_size}" x2="{width}" y2="{i * cell_size}" stroke="black" stroke-width="1"/>\n'
                )
                # Vertical lines
                f.write(
                    f'  <line x1="{i * cell_size}" y1="0" x2="{i * cell_size}" y2="{self.size * cell_size}" stroke="black" stroke-width="1"/>\n'
                )

            # Grid letters (faded)
            for row in range(self.size):
                for col in range(self.size):
                    x = col * cell_size + cell_size // 2
                    y = (
                        row * cell_size + cell_size // 2 + 5
                    )  # +5 for vertical alignment
                    f.write(
                        f'  <text x="{x}" y="{y}" font-family="Arial" font-size="{cell_size // 2}" text-anchor="middle" fill="#CCCCCC">{self.grid[row][col]}</text>\n'
                    )

            # Words with highlighted paths
            colors = [
                "#FF0000",
                "#00AA00",
                "#0000FF",
                "#FF6600",
                "#9900CC",
                "#009999",
                "#FF00FF",
                "#666600",
                "#663300",
                "#003366",
            ]

            # Draw word paths
            for i, word in enumerate(self.placed_words):
                color = colors[i % len(colors)]
                positions = self.word_positions[word]

                # Draw a line for the word path
                start_pos = positions[0]
                end_pos = positions[-1]
                start_x = start_pos[1] * cell_size + cell_size // 2
                start_y = start_pos[0] * cell_size + cell_size // 2
                end_x = end_pos[1] * cell_size + cell_size // 2
                end_y = end_pos[0] * cell_size + cell_size // 2

                # Draw a transparent background for the line
                f.write(
                    f'  <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="{color}" stroke-width="{cell_size * 0.8}" stroke-opacity="0.3" stroke-linecap="round"/>\n'
                )

                # Draw the actual line
                f.write(
                    f'  <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>\n'
                )

                # Highlight the word's letters
                for row, col in positions:
                    x = col * cell_size + cell_size // 2
                    y = row * cell_size + cell_size // 2 + 5
                    letter = self.grid[row][col]
                    f.write(
                        f'  <text x="{x}" y="{y}" font-family="Arial" font-size="{cell_size // 2}" text-anchor="middle" font-weight="bold" fill="{color}">{letter}</text>\n'
                    )

            # Word list
            f.write(
                f'  <text x="10" y="{self.size * cell_size + 30}" font-family="Arial" font-size="16" font-weight="bold">Solution:</text>\n'
            )

            # Arrange words in columns with matching colors
            words_per_column = 5
            column_width = width // ((len(self.placed_words) // words_per_column) + 1)

            for i, word in enumerate(sorted(self.placed_words)):
                column = i // words_per_column
                row = i % words_per_column
                x = 10 + column * column_width
                y = self.size * cell_size + 50 + row * 20
                color = colors[i % len(colors)]
                f.write(
                    f'  <text x="{x}" y="{y}" font-family="Arial" font-size="14" fill="{color}">{word}</text>\n'
                )

            # SVG footer
            f.write("</svg>\n")

    def generate(self, word_file: str, output_file: str):
        """Generate a complete word search puzzle."""
        words = self.read_words_from_file(word_file)

        if not words:
            print("No valid words found in the input file.")
            return False

        # Sort words by length (longer words first)
        words.sort(key=len, reverse=True)

        # Place words
        for word in words:
            if not self.place_word(word):
                print(f"Warning: Could not place word '{word}'")

        if not self.placed_words:
            print(
                "Could not place any words. Try reducing word length or increasing grid size."
            )
            return False

        # Fill remaining cells
        self.fill_empty_cells()

        # Generate puzzle SVG
        self.generate_svg(output_file)

        # Generate solution SVG
        solution_file = output_file.replace(".svg", "_solution.svg")
        self.generate_solution_svg(solution_file)

        print(f"Word search generated with {len(self.placed_words)} words")
        print(f"Placed words: {', '.join(self.placed_words)}")
        print(f"Puzzle saved to {output_file}")
        print(f"Solution saved to {solution_file}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate a word search puzzle as SVG."
    )
    parser.add_argument("word_file", help="Text file containing words, one per line")
    parser.add_argument(
        "-o",
        "--output",
        default="wordsearch.svg",
        help="Output SVG file (default: wordsearch.svg)",
    )
    parser.add_argument(
        "-s", "--size", type=int, default=15, help="Grid size (default: 15)"
    )
    parser.add_argument(
        "-a",
        "--attempts",
        type=int,
        default=100,
        help="Max attempts to place each word (default: 100)",
    )

    args = parser.parse_args()

    generator = WordSearchGenerator(size=args.size, max_attempts=args.attempts)
    generator.generate(args.word_file, args.output)


if __name__ == "__main__":
    main()
