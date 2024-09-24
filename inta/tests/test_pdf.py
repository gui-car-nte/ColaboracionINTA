import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

# Crear la tabla original
data = {
    'Condition': ['Initial', 'After Deperm', 'After Perm'],
    'mx (mA·m2)': ['2.8 ± 1.1', '3.1 ± 1.7', '3.4 ± 1.7'],
    'my (mA·m2)': ['-1.7 ± 1.7', '-2.6 ± 1.3', '-1.3 ± 1.6'],
    'mz (mA·m2)': ['1.1 ± 1.5', '0.6 ± 1.1', '0.9 ± 1.3'],
    '|m| (mA·m2)': ['3.5 ± 2.0', '4.1 ± 2.0', '3.7 ± 2.0'],
    'Expected Value (mA·m2)': ['< 50', '< 50', '< 50']
}

df = pd.DataFrame(data)

# Función para modificar la tabla
def modify_table(df, condition, column, new_value):
    if condition in df['Condition'].values and column in df.columns:
        df.loc[df['Condition'] == condition, column] = new_value
        print(f"Valor modificado para {condition} en {column}: {new_value}")
    else:
        print("Condición o columna no encontrada.")

# Modificar algunos valores
modify_table(df, 'Initial', 'mx (mA·m2)', '3.0 ± 1.2')
modify_table(df, 'After Deperm', 'my (mA·m2)', '-2.8 ± 1.4')

# Crear el PDF
pdf_filename = "tabla_modificada.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
elements = []

# Añadir título
styles = getSampleStyleSheet()
title = Paragraph("Tabla 1. SMILE DPA Magnetic moment values (Modificada)", styles['Title'])
elements.append(title)

# Convertir DataFrame a lista para ReportLab
data = [df.columns.tolist()] + df.values.tolist()

# Crear la tabla
table = Table(data)

# Estilo de la tabla
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('TOPPADDING', (0, 1), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])
table.setStyle(style)

# Añadir la tabla al documento
elements.append(table)

# Generar el PDF
doc.build(elements)

print(f"Se ha generado el PDF: {pdf_filename}")

# Mostrar la tabla modificada en la consola
print("\nTabla modificada:")
print(df.to_string(index=False))