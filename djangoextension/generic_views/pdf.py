# Create your views here.
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from StringIO import StringIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch  
from django.template import Template, Context
from django.conf import settings
import os.path
from django.core.files.base import File
import time


def pdf_list(filepath):
    path =  os.path.join(settings.MEDIA_ROOT,'pdfs',filepath)
    listing = os.listdir(path)
    return listing

def pdf_feed(path,filename,request):
    fullpath = os.path.join(settings.MEDIA_ROOT,'pdfs',path,filename)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment;'
    
    f = open(fullpath,'rb')  # notice 'rb' mode is key to the problems
    #time.sleep(5)
    response.write(f.read())
    '''
    buff = StringIO()
    file = open(fullpath,'r')
    f = File(file)
    #f.name = fullpath

    for chunk in f.chunks():
        buff.write(chunk)

    response.write(buff.getvalue())
    '''
    '''
    buff = StringIO()
    #buff.readlines
    buff.readlines(fullpath)
    response.write(buff.getvalue())
    #response = HttpResponse(file(fullpath).read())
    buff.close()
    '''
    return response


class pdf_response():
    def __init__(self,fielname):
        self.response = HttpResponse(mimetype='application/pdf')
        pdf_name = fielname #"pdf-%s" % str('pdf1')
        self.response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pdf_name
        self.buff = StringIO()
        self.serve_pdf = SimpleDocTemplate(self.buff, rightMargin=72,
                            leftMargin=72, topMargin=0, bottomMargin=18)
        # add style
        
        self.styles=getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        
        # add logo
        self.elements = []
        logo = "media/images/card.png"
        im = Image(logo, 8.3*inch, 2.1*inch)
        self.elements.append(im)
        self.add_spacer(width=10,height=10)
        
    def add_spacer(self,height=10,width=10):
        # add spacer
        s = Spacer(width=width, height=height)
        self.elements.append(s)
    
    def add_render_list(self,template_list,obj):
        for i in range(0,len(template_list)):
            self.add_render(template_list[i],obj)
        
    def add_render(self,template,obj):
        t = Template(template)
        ptext = t.render(Context({"obj": obj}))
        self.add_para(ptext)
    
    def add_para(self,text):
        ptext = '<font size=12>' + text + '</font>'
        self.elements.append(Paragraph(ptext, self.styles["Justify"]))
        self.add_spacer(10)
        
    def add_title(self,text):
        ptext = '<font size=16>' + text + '</font>'
        self.elements.append(Paragraph(ptext, self.styles["Normal"]))        
        self.add_spacer(20)
        
    def build_to_response(self):
        self.serve_pdf.build(self.elements)
        self.response.write(self.buff.getvalue())
        self.buff.close()
        return self.response

'''
def pdf_serve(request):
        # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    pdf_name = "pdf-%s" % str('pdf1')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pdf_name
    
    buff = StringIO()
    serve_pdf = SimpleDocTemplate(buff, rightMargin=72,
                            leftMargin=72, topMargin=0, bottomMargin=18)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    elements = []
    logo = "media/images/card.png"
    im = Image(logo, 8.3*inch, 2.1*inch)
    elements.append(im)
    
    s = Spacer(width=10, height=10)
    elements.append(s)

    # Create the PDF object, using the response object as its "file."
    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    elements.append(Paragraph(ptext, styles["Justify"]))
    

    
    serve_pdf.build(elements)
    
    # Close the PDF object cleanly, and we're done.
    response.write(buff.getvalue())
    buff.close()

    return response
'''