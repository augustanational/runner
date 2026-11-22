import sys
import fontforge
import psMat

def scale_font(input_path, output_path, scale_factor):
    font = fontforge.open(input_path)

    # 3. Select all glyphs and scale both outlines and horizontal advance widths
    font.selection.all()
    font.transform(psMat.scale(scale_factor))

    # 4. Round coordinates to integers (best practice for TrueType .ttf fonts)
    font.round()

    # 5. Export the scaled font
    font.generate(output_path)
    font.close()
    print(f"Successfully scaled '{input_path}' by {scale_factor}x -> '{output_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: fontforge -script scale_font.py <input.ttf> <output.ttf> <scale_factor>")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    factor = float(sys.argv[3])

    scale_font(in_file, out_file, factor)
