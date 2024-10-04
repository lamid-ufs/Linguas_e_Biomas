import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageOps
import io
from urllib.parse import urlparse
import requests

def is_valid_url(url):
  try:
    result = urlparse(url)
    return True
  except ValueError:
    return False

def create_qr_code(url, logo=None):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white", image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img = img.convert("RGBA")

    if logo is not None:
        # Redimensionar o logo
        logo_size = int(img.size[0] * 0.25)  # O logo ocupará 25% do tamanho do QR code
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # Calcular a posição para colocar o logo no centro
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        
        # Criar uma máscara circular
        mask = Image.new("L", logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
        
        # Aplicar a máscara ao logo
        output = ImageOps.fit(logo, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        
        # Criar uma nova imagem para o resultado final
        final_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
        
        # Colar o QR code na imagem final
        final_img.paste(img, (0, 0))
        
        # Colar o logo na imagem final
        final_img.paste(output, pos, output)
        
        return final_img
    else:
        return img
    
def autor():
   st.divider()
   st.markdown("<small>Desenvolvido por [Túlio Gois](github.com/tuliosg)</small>", unsafe_allow_html=True)