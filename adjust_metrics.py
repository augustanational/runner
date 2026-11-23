import argparse
import sys
import fontforge
import psMat

def shift_font(input_path, output_path, dy):
    try:
        font = fontforge.open(input_path)
    except Exception as e:
        print(f"Error opening font: {e}", file=sys.stderr)
        sys.exit(1)

    matrix = psMat.translate(0, dy)
    font.selection.all()

    for glyph in font.selection.byGlyphs:
        if not glyph.references:
            # glyph.transform() automatically moves BOTH contours and anchorPoints
            glyph.transform(matrix)
        elif glyph.anchorPoints:
            # For composite glyphs (with references), shift their anchors individually
            old_anchors = glyph.anchorPoints
            glyph.anchorPoints = ()
            for ap in old_anchors:
                name = ap[0]
                ap_type = ap[1]
                x = ap[2]
                y = ap[3]
                if len(ap) == 5:
                    glyph.addAnchorPoint(name, ap_type, x, y + dy, ap[4])
                else:
                    glyph.addAnchorPoint(name, ap_type, x, y + dy)

    # Shift vertical metrics to keep total em-size and line-height identical
    font.ascent += dy
    font.descent -= dy
    font.hhea_ascent += dy
    font.hhea_descent += dy
    font.os2_typoascent += dy
    font.os2_typodescent += dy
    font.os2_winascent += dy
    font.os2_windescent -= dy

    font.generate(output_path)
    font.close()
    print(f"Success: Shifted glyphs, anchors, and metrics by {dy} units -> '{output_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shift all glyphs, anchor points, and vertical metrics while keeping font size unchanged."
    )
    parser.add_argument("input", help="Path to input font file (e.g., input.ttf)")
    parser.add_argument("output", help="Path to output font file (e.g., output.ttf)")
    parser.add_argument(
        "dy",
        type=int,
        help="Vertical shift in font units (negative = move down, positive = move up)"
    )

    args = parser.parse_args()
    shift_font(args.input, args.output, args.dy)
