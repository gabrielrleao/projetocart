from PIL import Image, ImageDraw, ImageFont
import io
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1H5f8GwR8ny11D02nMeVw9gowHibjE-3836YBLyDALFM'
SAMPLE_RANGE_NAME = 'NOVATOS!B2:L'  # Faixa que inclui as colunas de interesse

def download_image_from_drive(service, file_id, image_path):
    try:
        request = service.files().get_media(fileId=file_id)
        img_content = io.BytesIO(request.execute())
        with open(image_path, 'wb') as file:
            file.write(img_content.getvalue())
        return True
    except HttpError as error:
        print(f'Erro ao baixar a imagem: {error}')
        return False


def get_sheet_values(service):
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result['values']
        return values
    except HttpError as err:
        print(f'Erro ao obter os valores da planilha: {err}')
        return []


def main():
    # Carregar a imagem "cart"
    cart = Image.open('cart.png')

    # Configurar credenciais do Google Drive e Sheets
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    sheet_service = build('sheets', 'v4', credentials=creds)

    # Definir a fonte do texto
    fonte = ImageFont.truetype('arial.ttf', size=36)

    # Criar um objeto ImageDraw para desenhar na imagem
    draw = ImageDraw.Draw(cart)

    # Obter os valores dos campos de texto e das imagens da planilha
    valores_e_imagens = get_sheet_values(sheet_service)

    # Definir as posições iniciais dos campos de texto individualmente
    posicao_nome = (210, 700)
    posicao_inst = (300, 845)
    posicao_rota = (110, 980)
    posicao_turno = (550, 980)

    # Iterar sobre os valores e imagens obtidos
    for linha in valores_e_imagens:
        if len(linha) >= 5:
            # Obter os valores da linha atual
            nome = linha[0]
            inst = linha[1]
            rota = linha[2]
            turno = linha[3]
            imagem_id = linha[4]

            # Baixar a nova imagem do Google Drive
            image_path = f'{imagem_id}.jpg'  # Nome do arquivo baseado no ID da imagem
            download_image_from_drive(drive_service, imagem_id, image_path)

            # Carregar a nova imagem
            pessoa = Image.open(image_path)

            # Definir as dimensões desejadas para a imagem "pessoa"
            largura_desejada = 400
            altura_desejada = 380

            # Redimensionar a imagem "pessoa" para as dimensões desejadas
            pessoa = pessoa.resize((largura_desejada, altura_desejada))
            # Posicionar a imagem "pessoa" no canto superior esquerdo da imagem "cart"
            posicao_imagem = (200, 190)
            cart.paste(pessoa, posicao_imagem)

            # Desenhar os campos de texto na imagem
            draw.text(posicao_nome, nome, font=fonte, fill=(0, 0, 0))
            draw.text(posicao_inst, inst, font=fonte, fill=(0, 0, 0))
            draw.text(posicao_rota, rota, font=fonte, fill=(0, 0, 0))
            draw.text(posicao_turno, turno, font=fonte, fill=(0, 0, 0))

            cart.show()

# Remover as imagens temporárias baixadas
for linha in valores_e_imagens:
    if len(linha) >= 5:
        imagem_id = linha[4]
        image_path = f'{imagem_id}.jpg'
        if os.path.exists(image_path):
            os.remove(image_path)

        if name == 'main':
            main()
