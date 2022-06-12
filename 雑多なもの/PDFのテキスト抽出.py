from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

input_path = "03-yoshi.pdf"
output_path="result.txt"

rsrcmgr=PDFResourceManager()
codec="utf-8"
params=LAParams()

with open(output_path,'ab') as output:
    device=TextConverter(rsrcmgr,output,codec=codec,laparams=params)
    with open(input_path,"rb") as input:
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        for page in PDFPage.get_pages(input):
            interpreter.process_page(page)

    device.close()