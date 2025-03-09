# Wordsearch-generator

## Background

My son is obsessed with word search puzzles. For his 7th birthday party, he asked if we could make a word search that we could include in the party bags. So I banged together this script to get that done.

This generates two SVG files, the puzzle and the solution to the puzzle.

## Usage

```bash
# install a venv using uv
uv venv
source .venv/bin/activate.fish  # I'm using fish, source the correct file for your shell!
python wordsearch.py words.txt
```

Additional arguments (like grid size) can be accessed with `python wordsearch.py --help`

## My workflow

1. Generate the SVGs
2. Convert the solution SVG to a PNG (I used [Permute](https://software.charliemonroe.net/permute/) but [ImageMagick](https://imagemagick.org/index.php) will work just as well)
3. Upload the solution PNG to Imgur
4. Copy the link to the solution PNG
5. Create a QR code to the Imgur link (I used [QR Code Generator](https://www.qr-code-generator.com/))
6. Put everything together using an image editor (I used [Pixelmator Pro](https://www.pixelmator.com/pro/))
7. Print!

![Pixelmator](./images/pixelmator.png)
