import sys
import fontforge
import psMat

def scale_font(input_path, output_path, scale_factor):
    font = fontforge.open(input_path)

    # 1. Scale vertical boundaries (em = ascent + descent)
    # Scaling ascent and descent proportionally automatically updates font.em
    font.ascent = int(round(font.ascent * scale_factor))
    font.descent = int(round(font.descent * scale_factor))

    # 2. Scale OpenType OS/2 and HHEA vertical metrics to prevent clipping across all OS/engines
    # Note: os2_windescent and hhea_descent are typically negative values in FontForge
    font.os2_winascent = int(round(font.os2_winascent * scale_factor))
    font.os2_windescent = int(round(font.os2_windescent * scale_factor))
    font.os2_typoascent = int(round(font.os2_typoascent * scale_factor))
    font.os2_typodescent = int(round(font.os2_typodescent * scale_factor))
    font.hhea_ascent = int(round(font.hhea_ascent * scale_factor))
    font.hhea_descent = int(round(font.hhea_descent * scale_factor))

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
