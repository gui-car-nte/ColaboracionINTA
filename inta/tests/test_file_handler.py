from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def crear_pdf_con_graficos(momentos_magneticos):
    tipos = ['x', 'y', 'z']  # Los ejes correspondientes
    pdf_path = "momento_magnetico.pdf"
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Agregar título centrado
    c.setFont("Helvetica-Bold", 18)
    titulo = "Momento Magnético"
    c.drawCentredString(width / 2.0, height - 50, titulo)
    
    y_offset = 100  # Offset inicial para el primer gráfico
    
    for i, (eje, momento_magnetico) in enumerate(zip(tipos, momentos_magneticos)):
        # imagen = generar_grafico(eje)
        imagen = 'src/front/resource/imagen.png'
        
        # Agregar el eje correspondiente encima de cada gráfico
        c.setFont("Helvetica-Bold", 12)
        c.drawString(275, 660, f"Eje {eje}")
        
        # Agregar la imagen del gráfico
        c.drawImage(ImageReader(imagen), 100, 450, width=400, height=200)
        
        # Agregar el momento magnético debajo de cada gráfico
        c.setFont("Helvetica", 12)
        c.drawString(225, 425, f"Momento Magnético: {momento_magnetico}")
        
        y_offset += 300  # Incrementar el offset para el siguiente gráfico
        c.showPage()
    
    c.save()

# Ejemplo de lista de momentos magnéticos
momentos_magneticos = [1.0, 0.5, 2.0]

crear_pdf_con_graficos(momentos_magneticos)
