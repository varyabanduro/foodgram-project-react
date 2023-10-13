from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("static/logo_download_shopping_cart.png", 10, 1, 33)
        # Setting font: helvetica bold 15
        self.add_font(fname='static/DejaVuSansMono.ttf')
        self.set_font('DejaVuSansMono', size=20)
        # Moving cursor to the right:
        self.cell(40)
        # Printing title:
        self.cell(50, 10, "Список покупок", "B", align="L")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("DejaVuSansMono", size=12)
        self.set_text_color(128)
        # Printing page number:
        # self.cell(0, 10, f"Страница {self.page_no()}/{{nb}}", align="C")
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
