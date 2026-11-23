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
        # 1. Shift anchor points (mark-to-base, mark-to-mark, etc.)
        # Anchors belong to individual glyphs and do not inherit reference shifts,
        # so we shift them on ALL glyphs.
        if glyph.anchorPoints:
            new_anchors = []
            for ap in glyph.anchorPoints:
                # Tuple format: (anchor_class_name, type, x, y[, ligature_index])
                ap_list = list(ap)
                ap_list[3] += dy
                new_anchors.append(tuple(ap_list))
            glyph.anchorPoints = tuple(new_anchors)

        # 2. Shift glyph outlines (skip pure references to avoid double-shifting)
        if not glyph.references:
            glyph.transform(matrix)

    # 3. Shift vertical metrics to keep total em-size and line-height identical
    font.ascent += dy
    font.descent -= dy
    font.hhea_ascent += dy
    font.hhea_descent += dy
    font.os2_typoascent += dy
    font.os2_typodescent += dy
    font.os2_winascent += dy
    font.os2_windescent -= dy

    # 4. Generate the updated font
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
