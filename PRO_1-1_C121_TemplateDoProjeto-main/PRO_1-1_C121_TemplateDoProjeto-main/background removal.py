# importe o cv2 para capturar o feed de vídeo
import cv2

import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
# anexe a câmera indexada como 0
camera = cv2.VideoCapture(0)

# definindo a largura do quadro e a altura do quadro como 640 X 480
camera.set(3 , 640)
camera.set(4 , 480)

# carregando a imagem da montanha
mountain = cv2.imread('mount everest.jpg')

# redimensionando a imagem da montanha como 640 X 480
for i in range(60):
    ret, bg = camera.read()
bg = np.flip(bg, axis=1)


while True:

    # ler um quadro da câmera conectada
    status , frame = camera.read()

    # se obtivermos o quadro com sucesso
    if status:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # inverta-o
        frame = cv2.flip(frame , 1)

        # convertendo a imagem em RGB para facilitar o processamento
        frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

        # criando os limites
        lower_bound = np.array([100,100,100])
        upper_bound = np.array([255,255,255])

        # imagem dentro do limite
        mask_1 = cv2.inRange(hsv, lower_bound, upper_bound)

        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask_2 = cv2.inRange(hsv, lower_red, upper_red)

        # invertendo a máscara
        frame = np.flip(frame, axis=1)

        # bitwise_and - operação para extrair o primeiro plano / pessoa
        res_1 = cv2.bitwise_and(frame, frame, mask = mask_2)
        res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

        final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)

        # imagem final
        output_file.write(final_output)
        # exiba-a

        cv2.imshow('quadro' , frame)

        # espera de 1ms antes de exibir outro quadro
        code = cv2.waitKey(1)
        if code  ==  32:
            break

# libere a câmera e feche todas as janelas abertas
camera.release()
cv2.destroyAllWindows()
