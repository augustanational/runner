import sys
import fontforge
import psMat

def adjust_font(input_path, output_path, shift):
    font = fontforge.open(input_path)

# 1. Cập nhật thông số cơ bản (EM metrics)
font.ascent += shift
font.descent -= shift

# 2. Cập nhật bảng hhea (dùng cho macOS / iOS)
font.hhea_ascent += shift
font.hhea_descent -= shift

# 3. Cập nhật bảng OS/2 (dùng cho Windows / Web)
font.os2_typoascent += shift
font.os2_typodescent -= shift
font.os2_winascent += shift
font.os2_windescent += shift  # Lưu ý: giá trị winDescent luôn là số dương


    # 4. Round coordinates to integers (best practice for TrueType .ttf fonts)
    font.round()

    # 5. Export the scaled font
    font.generate(output_path)
    font.close()
    print(f"Successfully adjust '{input_path}' by {shift} -> '{output_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: fontforge -script adjust_metrics.py <input.ttf> <output.ttf> <shift>")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    shift = float(sys.argv[3])

    adjust_font(in_file, out_file, shift)
