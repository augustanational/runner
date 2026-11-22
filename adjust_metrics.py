import sys
import fontforge
import psMat

# Nhận tham số từ dòng lệnh
input_font = sys.argv[1]
output_font = sys.argv[2]
shift_y = int(sys.argv[3]) # Nhập số âm để hạ xuống (ví dụ: -100)

font = fontforge.open(input_font)

# Chọn tất cả ký tự và dịch chuyển theo trục Y
font.selection.all()
font.transform(psMat.translate(0, shift_y))

# (Tùy chọn) Cập nhật lại thông số Ascent và Descent nếu cần
font.ascent += shift_y
font.descent -= shift_y

# Xuất ra file mới
font.generate(output_font)
font.close()
