'''
pip install opencv-python #instalar cv2
pip install --upgrade opencv-python #Atualize para garantir a versão mais recente
pip install matplotlib
pip install easyocr
pip install sqlite3
'''

import sqlite3

import easyocr
import cv2
from  matplotlib import pyplot as plt


conn = sqlite3.connect('placa_veiculos.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS veiculo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL
    )
''')

conn.commit()

def inserir_placa(placa):
    cursor.execute('INSERT INTO veiculo (placa) VALUES (?)', (placa,))
    conn.commit()
    print('Placa inserido com sucesso!')


def listar_placa():
    cursor.execute('SELECT * FROM veiculo')
    veiculos = cursor.fetchall()
    for v in veiculos:
        print(f'ID: {v[0]}, Placa: {v[1]}')


def atualizar_placa(id, nova_placa):
    cursor.execute('UPDATE veiculo SET placa = ? WHERE id = ?', (nova_placa, id))
    conn.commit()
    print('Placa atualizado com sucesso!')

def deletar_placa(id):
    cursor.execute('DELETE FROM veiculo WHERE id = ?', (id,))
    conn.commit()
    print('Placa deletado com sucesso!')





img = cv2.imread('carros/Fiat-Argo.jpg')
cv2.imshow('img',img)

cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('cinza', cinza)


_, bin = cv2.threshold(cinza, 80, 255, cv2.THRESH_BINARY)


cv2.imshow('bin', bin)
desfoque = cv2.GaussianBlur(bin, (5, 5), 0)

cv2.imshow('des', desfoque)
cv2.imwrite('placa/desfoque.jpg', desfoque)




img = 'placa/desfoque.jpg'

# Inicializa o leitor do easyocr para português
reader = easyocr.Reader(['pt'])
result = reader.readtext('placa/desfoque.jpg')


img = cv2.imread(img)

for detection in result:

    #converter coordenadas para inteiros
    top_left = tuple(map(int, detection[0][0]))
    bottom_right = tuple(map(int,detection[0][2]))
    text = detection[1]

    #desenha o reângulo ao redor do texto detectado
    img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 3)

    img = cv2.putText(img, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,0,255), 2,cv2.LINE_AA)

    #converter a imagem para RGB para exibirção no Matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off') # Desativa os iexos para uma visualização mais limpa
plt.show()


lista_placa = reader.readtext('placa/desfoque.jpg', detail = 0)

print(lista_placa)
print(type(lista_placa))

inserir_placa(lista_placa[0])

listar_placa()




cv2.waitKey(0)
cv2.destroyWindow()
conn.close()