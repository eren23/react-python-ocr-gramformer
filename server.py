
from flask import Flask, request, Response
from threading import Thread
from flask_cors import CORS
from grfor import gf
import uuid

from fpdf import FPDF
  


app = Flask('')
CORS(app)

@app.route('/graformer', methods=["GET", "POST"])
def home():
    to_return = ""
    ocr = request.json["ocr"]
    corrected = gf.correct(ocr)
    for cor in corrected:
        to_return = to_return+cor
    

    # variable pdf
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
    
    # create a cell
    pdf.cell(200, 10, txt = "OCR Date is Here", 
             ln = 1, align = 'C')
    
    n=60

    line_array = [to_return[i:i+n] for i in range(0, len(to_return), n)]
    # add another cell
    for index, line in enumerate(line_array):

        pdf.cell(200, 10, txt = line,
             ln = index+2, align = 'C')
    
    # save the pdf with name .pdf
    pdf.output(f"pdfgen{uuid.uuid1()}.pdf")   

    response = Response(to_return,status=200)

    return response

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()