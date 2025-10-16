from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate , Paragraph, Spacer
from io import BytesIO
from datetime import datetime

def pdf_generator(clusters, outlines , ideas):

    buffer = BytesIO()
    document = SimpleDocTemplate(buffer,pagesize = A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph('<b> Report</b>' , styles['Title']))
    content.append(Spacer(1,12))
    content.append(Paragraph(
        f"Timestamped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['BodyText']
    ))

    content.append(Spacer(1,20))
    content.append(Paragraph('Generated Ideas' , styles['Heading1']))
    content.append(Spacer(1,20))


    for name , outline in outlines.items():
        content.append(Paragraph(f"<b>Cluster:</b> {name}", styles['Heading2']))
        content.append(Spacer(1,10))
        
        for line in outline.split("\n"):
            if line.strip():
                content.append(Paragraph(line.strip(), styles['BodyText']))        
        content.append(Spacer(1,10))

        idea = ideas.get(name, 'No idea created')
        content.append(Paragraph(f'<b> Generated Idea</b>',styles['Heading3']))
        content.append(Paragraph(idea, styles["BodyText"]))
        content.append(Spacer(1,20))


    document.build(content)
    buffer.seek(0)
    return buffer

