from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.image("static/logo_download_shopping_cart.png", 10, 1, 33)
        self.add_font(fname='static/DejaVuSansMono.ttf')
        self.set_font('DejaVuSansMono', size=20)
        self.cell(40)
        self.cell(50, 10, "Список покупок", "B", align="L")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVuSansMono", size=12)
        self.set_text_color(128)
        self.cell(0, 10, f"Варя Бандуро стр. {self.page_no()}", align="R")


def cart_list(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("DejaVuSansMono", size=15)
    count = 1
    for i in data:
        pdf.cell(40, 10, '{}) {}({}) - {}'.format(count, *i.values()))
        count += 1
        pdf.ln(9)
    return pdf
