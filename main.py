import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageOps
import io
from urllib.parse import urlparse
from components import *

if 'url' not in st.session_state:
    st.session_state.url = ""

st.set_page_config(page_title="Gerador de QR Code", page_icon="imgs/linguas_biomas_logo.png", layout="centered")

st.image("imgs/linguas_biomas_logo.png", width=100)
st.title("Gerador de QR Code")
st.markdown("Ferramenta para a criação dos QR Codes especiais para o Línguas e Biomas.")

tab1, tab2 = st.tabs(["📷 **Gerar QR Code**", "❓ **Como usar**"])

with tab1:
    st.markdown("#### Insira o link para gerar o QR Code")
    url = st.text_input("Copie e cole o link aqui:")

    if st.button('Gerar QR Code'):
        if is_valid_url(url):
            if url != st.session_state.url:
                st.session_state.url = url
                logo = Image.open("imgs/linguas_biomas.png").convert("RGBA")
                qr_image = create_qr_code(url, logo)

                img_byte_arr = io.BytesIO()
                qr_image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                with st.expander("QR Code gerado", expanded=True):
                    col1, col2, col3 = st.columns([1,2,1])
                    line1, line2, line3 = st.columns([1,2,1])

                    with col2:
                        st.image(qr_image, use_column_width=200)

                    with line3:
                        st.download_button(
                            label="Baixar QR Code",
                            data=img_byte_arr,
                            file_name=f"{urlparse(url).netloc}_qr_code.png",
                            mime="image/png"
                        )
            else:
                st.warning('O QR Code já foi gerado para este link. Insira um novo link para geração.')
        else:
            st.error('Por favor, insira um link válido.')
    
    autor()


with tab2:
    st.title("Tutorial")
    st.markdown(
        """
        **1. Procurando o seu link**
        - Acesse o site que você deseja compartilhar e copie o link da página no campo superior do navegador;
            > No exemplo abaixo, o link seria `instagram.com/gelinsufs/`
        """
        )
    st.image("imgs/gelins_instagram.png", use_column_width=True)
    st.markdown(
        """
        - Caso deseje compartilhar um vídeo do YouTube em um tempo específico, você deve acessar o vídeo e deixá-lo no tempo desejado. Em seguida, clique com o botão direito do mouse no vídeo e selecione a opção `Copiar URL do vídeo no momento atual`.
        """
        )
    st.image("imgs/youtube_ex.png", use_column_width=True)
    st.markdown(
        """
        **2. Gerando o QR Code**
        - Volte para a página do gerador de QR Code e cole o link no campo de texto;
        - Clique em "Gerar QR Code";
        - O QR Code será gerado e exibido na tela.
        """
        )
    st.markdown(
        """
        **3. Baixando o QR Code**
        - Para baixar o QR Code, clique no botão "Baixar QR Code";
        - O arquivo será salvo no seu computador. Você pode renomeá-lo e compartilhá-lo como preferir.
        """
        )
    
    autor()
    