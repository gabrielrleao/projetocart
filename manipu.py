from PIL import Image, ImageDraw, ImageFont

cart = Image.open('cart.png')
pessoa = Image.open('pessoa.jpeg')

# Definir as dimensões desejadas para a imagem 'pessoa.jpeg'
largura_desejada = 400
altura_desejada = 380

# Redimensionar a imagem 'pessoa.jpeg' para as dimensões desejadas
pessoa = pessoa.resize((largura_desejada, altura_desejada))

# Posicionar a imagem 'pessoa.jpeg' no canto superior esquerdo da imagem 'cart.png'
posicao_imagem = (200, 190)
cart.paste(pessoa, posicao_imagem)

# Definir a fonte do texto
fonte = ImageFont.truetype('arial.ttf', size=36)

# Criar um objeto ImageDraw para desenhar na imagem
draw = ImageDraw.Draw(cart)

# Definir os valores dos campos de texto
nome = "Gabriel asdasd dasdasd"
inst = "UNINASSAU"
rota = "Rec. Centro"
turno = "Manhã"

# Definir as posições dos campos de texto individualmente
posicao_nome = (210, 700)
posicao_inst = (300, 845)
posicao_rota = (110, 980)
posicao_turno = (550, 980)

# Desenhar os campos de texto na imagem
draw.text(posicao_nome, nome, font=fonte, fill=(0, 0, 0))
draw.text(posicao_inst, inst, font=fonte, fill=(0, 0, 0))
draw.text(posicao_rota, rota, font=fonte, fill=(0, 0, 0))
draw.text(posicao_turno, turno, font=fonte, fill=(0, 0, 0))

cart.show()
