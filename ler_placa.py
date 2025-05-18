import cv2
import easyocr
import matplotlib.pyplot as plt

# Carregar a imagem
image_path = 'carros/Fiat-Argo.jpg'
img = cv2.imread(image_path)

# Inicializar o EasyOCR
reader = easyocr.Reader(['pt', 'en'])  # Português e Inglês

# Detectar texto na imagem
resultados = reader.readtext(img)

# Mostrar os resultados e anotar
for (bbox, texto, conf) in resultados:
    if len(texto) >= 6:  # Filtrar possíveis placas
        print(f"Placa detectada: {texto} (confiança: {conf:.2f})")

        # Desenhar a caixa na imagem
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, texto, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Mostrar a imagem com anotações
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
