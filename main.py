from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json()

    cliente = data.get('cliente', 'Cliente')
    tratamiento = data.get('tratamiento', 'Tratamiento').upper()
    pedido = data.get('pedido', '[Pedido #0000]')
    precio = data.get('precio', '0€')

    img = Image.open('valeregalo.png').convert("RGB")
    draw = ImageDraw.Draw(img)

    color = (76, 54, 18)
    font = ImageFont.truetype("arial.ttf", 72)

    draw.text((600, 500), cliente, font=font, fill=color)
    draw.text((600, 600), tratamiento, font=font, fill=color)
    draw.text((600, 700), pedido, font=font, fill=color)
    draw.text((600, 800), precio, font=font, fill=color)

    output_pdf = BytesIO()
    img.save(output_pdf, "PDF", resolution=300)
    output_pdf.seek(0)

    fecha = datetime.now().strftime("%Y%m%d")
    n_pedido = pedido.replace("[Pedido #", "").replace("]", "")
    filename = f"bono_{fecha}_pedido_{n_pedido}.pdf"

    return send_file(output_pdf, download_name=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
