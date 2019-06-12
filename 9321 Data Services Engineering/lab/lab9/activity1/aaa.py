
from reportlab.pdfgen import canvas
#设置绘画开始的位置
def generate_pdf(c,data):
    c.drawString(1, 800, data)

file = 'file_r.pdf'
# 定义要生成的pdf的名称
total_data = 'sdasdasdasdadasdadsadas'
c = canvas.Canvas(file)
# 调用函数进行绘画，并将canvas对象作为参数传递
generate_pdf(c, total_data)
# showPage函数：保存当前页的canvas
c.showPage()
# save函数：保存文件并关闭canvas
c.save()