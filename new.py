from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math
import os

# ---- Settings ----
INPUT_FILE = "lastly.png"   # change to your file name
OUTPUT_TEXT_FILE = "lastly.txt"
OUTPUT_IMAGE_FILE = "lastly.png"

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength / 256

scaleFactor = 0.09

oneCharWidth = 10
oneCharHeight = 18

FONT_SIZE = 15

# Cross-platform monospace font fallback list, tried in order.
FONT_CANDIDATES = [
    'C:\\Windows\\Fonts\\lucon.ttf',                                  # Windows (Lucida Console)
    '/System/Library/Fonts/Menlo.ttc',                                # macOS
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',            # Linux (common)
    '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf' # Linux (alternative)
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    # Last resort: PIL's built-in default bitmap font (not monospace-scalable, but always works)
    print("Warning: no monospace TTF found from the candidate list; using PIL's default font.")
    return ImageFont.load_default()


def getChar(inputInt):
    index = min(math.floor(inputInt * interval), charLength - 1)
    return charArray[index]


def main():
    fnt = load_font(FONT_SIZE)

    # Convert to RGB immediately so background-removed (RGBA) images don't crash
    # the r, g, b unpack below. Transparent areas become solid black.
    with Image.open(INPUT_FILE) as im:
        im = im.convert("RGB")
        # Brighten the image (1.0 = original, >1.0 = brighter, <1.0 = darker)
        enhancer = ImageEnhance.Brightness(im)
        im = enhancer.enhance(1.4)  # try 1.2–1.6 depending on how much brighter you want

        width, height = im.size
        im = im.resize(
            (int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))),
            Image.NEAREST
        )
        width, height = im.size
        pix = im.load()

        outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
        d = ImageDraw.Draw(outputImage)

        with open(OUTPUT_TEXT_FILE, "w") as text_file:
            for i in range(height):
                for j in range(width):
                    r, g, b = pix[j, i]
                    h = int(r / 3 + g / 3 + b / 3)
                    character = getChar(h)
                    text_file.write(character)
                    d.text((j * oneCharWidth, i * oneCharHeight), character, font=fnt, fill=(r, g, b))
                text_file.write('\n')

        outputImage.save(OUTPUT_IMAGE_FILE)
        print(f"Done. Wrote {OUTPUT_TEXT_FILE} and {OUTPUT_IMAGE_FILE}")


if __name__ == "__main__":
    main()