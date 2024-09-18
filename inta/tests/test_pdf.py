from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER

# Configuración del PDF
pagesize = A4
margins = (10*mm, 10*mm, 10*mm, 10*mm)

# Estilos de texto
style = ParagraphStyle(
    name = 'BodyText',
    fontSize = 12,
    leading = 14,
    alignment = TA_CENTER
)

# Encabezado
encabezado = Paragraph("TEST RESULTS", style = ParagraphStyle(
    name = 'Header',
    fontSize = 18,
    leading = 20,
    alignment = TA_CENTER
))

# Datos de la tabla
data = [
    ['', 'mx (mA·m²)', 'my (mA·m²)', 'mz (mA·m²)', '|m| (mA·m²)', 'Expected Value'],
    ['Initial', '2.8 ± 1.1', '-1.7 ± 1.7', '1.1 ± 1.5', '3.5 ± 2.0', '< 50'],
    ['After Deperm', '3.1 ± 1.7', '-2.6 ± 1.3', '0.6 ± 1.1', '4.1 ± 2.0', '< 50'],
    ['After Perm', '3.4 ± 1.7', '-1.3 ± 1.6', '0.9 ± 1.3', '3.7 ± 2.0', '< 50']
]

# Creación de la tabla
table = Table(data, style = TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER')
]))

# Creación del PDF
doc = SimpleDocTemplate('output.pdf', pagesize = pagesize, margins = margins)
story = [encabezado, Spacer(1, 20), table]
doc.build(story)