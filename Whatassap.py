import pywhatkit
import keyboard
from datetime import datetime
import time
import os

# diretorio = ''  # Substitua pelo caminho da sua pasta
#
# for arquivo in os.listdir(diretorio):
#     caminho_completo = os.path.join(diretorio, arquivo)
#     if os.path.isfile(caminho_completo):
#         print(arquivo)


numero = ['+5511982593295']
mensagem = "Olá sou bot ,Vinicius Seu capacete esta sendo roubado"
#imagem = [r'C:\Users\fabfe\PycharmProjects\OpenCVScript_4\pythonProject1\Fotos\frame128.jpg']
imagem = [r'C:\Users\fabfe\PycharmProjects\OpenCVScript_4\pythonProject1\imagem\capacete\Image_1.jpg']

# Espera 1 minuto antes de começar
time.sleep(60)

# Envia a mensagem e espera 2 minutos antes de enviar a imagem
for num in numero:
    pywhatkit.sendwhatmsg(num, mensagem, datetime.now().hour, datetime.now().minute + 2)
    time.sleep(15)  # Espera 4 segundos antes de pressionar enter
    keyboard.press_and_release('enter')
    time.sleep(5)  # Espera 10 segundos após enviar a mensagem

    # Envia a imagem
while True:
    pywhatkit.sendwhats_image(num, imagem[0], "Imagem1")
    time.sleep(10)  # Espera 15 segundos antes de pressionar enter
    keyboard.press_and_release('enter')
    time.sleep(60)  # Espera 1 minuto após enviar a imagem
    keyboard.press_and_release('ctrl + w')  # Fecha a janela do navegador do WhatsApp
    break