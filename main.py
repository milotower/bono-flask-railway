from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime

app = Flask(__name__)


@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    data = request.json

    cliente = data.get('cliente', 'Cliente')
    tratamiento = data.get('tratamiento', 'Tratamiento')
    pedido = data.get('pedido', '[Pedido #0000]')
    precio = data.get('precio', '0€')

    # Cargar plantilla local (asegúrate de subirla al entorno)
    img = Image.open('valeregalo.png').convert("RGB")
    draw = ImageDraw.Draw(img)

    #try:
     #   font = ImageFont.truetype("alice.ttf", 100)
    #except:
     #   font = ImageFont.load_default()

    # Coordenadas ajustables según tu diseño
    # draw.text((100, 150), cliente, font=font, fill="black")

    #draw.text((100, 360), precio, font=font, fill="black")
    font_tratamiento = ImageFont.truetype("alice.ttf", 120)
    font_pedido = ImageFont.truetype("alice.ttf", 50)
    color_texto = (76, 54, 18)  # hexadecimal #4c3612

    draw.text((250, 480), tratamiento.upper(), font=font_tratamiento, fill=color_texto)
    draw.text((1560, 45), pedido, font=font_pedido, fill=color_texto)

    output_pdf = BytesIO()
    img.save(output_pdf, "PDF", resolution=300)
    output_pdf.seek(0)

    # Obtener fecha actual en formato YYYYMMDD
    fecha = datetime.now().strftime("%Y%m%d")

    # Limpiar número de pedido (extraer solo los dígitos)
    n_pedido = pedido.replace("[Pedido #", "").replace("]", "")

    # Crear nombre dinámico del archivo
    filename = f"bono_{fecha}_pedido_{n_pedido}.pdf"

    return send_file(output_pdf, download_name=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
