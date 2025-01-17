import pypdf as pdf
from os import sep, remove

separator = sep

def QRArxiv(filename,dir='.',sep=separator,deleteQR=True,id_arxiv=None,shortname=''):
    """Takes a pdf file from Arxiv.org and creates an exact copy with a QR embedded in the first page that links back to the corresponding paper on Arxiv.org."""


    # Open pdf, create the object PdfFileReader, extract a page from it, extract text and get the id


    pdf_file = open(filename,'rb')
    pdf_doc = pdf.PdfReader(pdf_file)
    pdf_page = pdf_doc.get_page(0)
    if id_arxiv==None:
        pdf_text = pdf_page.extract_text()
        id_arxiv = pdf_text[pdf_text.find(":")+1:pdf_text.find(" ")]
    if shortname == '':
        shortname = filename
    elif shortname.endswith('.pdf'):
        shortname = shortname[:-4]
    else:
        pass # shortname = shortname


    # Create link to arxiv.org


    http = "https://arxiv.org/pdf"
    link = '/'.join([http,id_arxiv])

    print(id_arxiv)

    # import all reportlab's necessary tools


    from reportlab.pdfgen import canvas
    from reportlab.graphics.barcode import qr
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics import renderPDF
    from reportlab.lib.pagesizes import letter


    # Creates a temporary folder to store a temporal pdf with a qr


    # with tempfile.TemporaryDirectory() as path:
    c = canvas.Canvas(separator.join([dir,"QRtempfile_{}.pdf".format(shortname)]), pagesize=letter)
    qr_code = qr.QrCodeWidget(link)
    bounds = qr_code.getBounds()
    widthqr = bounds[2] - bounds[0]
    heightqr = bounds[3] - bounds[1]
    d = Drawing(45, 45, transform=[90./widthqr,0,0,90./heightqr,0,0])
    d.add(qr_code)
    renderPDF.draw(d, c, 15, 686)

    c.save()

    # The previous qr file is merged with the desired arxiv paper

    qr_file = open(separator.join([dir,"QRtempfile_{}.pdf".format(shortname)]),'rb')
    qr_doc = pdf.PdfReader(qr_file)
    qr_page = qr_doc.get_page(0)
    pdf_page.merge_page(qr_page)


    # The result is put out and the files are closed (except the canvas c)

    output = pdf.PdfWriter()
    for n in range(pdf_doc.get_num_pages()):
        output.add_page(pdf_doc.get_page(n))
    outputStream = open(sep.join([dir,shortname+'-qr.pdf']),'wb')
    output.write(outputStream)
    outputStream.close()
    qr_file.close()
    pdf_file.close()
    if deleteQR == True:
        remove(separator.join([dir,"QRtempfile_{}.pdf".format(shortname)]))


if __name__ == '__main__':
    from sys import argv
    if len(argv)  == 1:
        print("Please, provide a pdf to QR-ify.")
    elif len(argv) == 2:
        filename = argv[1]
        QRArxiv(filename)
    else:
        print("Too many arguments were given.")
