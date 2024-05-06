import numpy as np
import cv2
import time
from csv import DictWriter
import tkinter as tk
from tkinter import messagebox
import pygame

# Inicializando o pygame
pygame.mixer.init()

# Carregando arquivo com o nome dos objetos
with open('yoloDados/YoloNames.names') as f:
    labels = [line.strip() for line in f]

# Carregando os arquivos treinados pelo framework YOLO
network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
layers_names_all = network.getLayerNames()
layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]

# Definindo probabilidades mínimas e limite de filtragem
probability_minimum = 0.5
threshold = 0.3
colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

# Carregando classificador de faces
classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.LBPHFaceRecognizer_create()
reconhecedor.read('classificadorLBPH_V1.yml')

# Inicializando a câmera
camera = cv2.VideoCapture(0)

# Inicializando o arquivo CSV para salvar as detecções
with open('teste.csv', 'w') as arquivo:
    cabecalho = ['Detectado', 'Acuracia']
    escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
    escritor_csv.writeheader()

    # Variável para armazenar se uma garrafa foi detectada
    bottle_detected = False

    while True:
        _, frame = camera.read()
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        network.setInput(blob)
        start = time.time()
        output_from_network = network.forward(layers_names_output)
        end = time.time()

        bounding_boxes = []
        confidences = []
        class_numbers = []

        for result in output_from_network:
            for detected_objects in result:
                scores = detected_objects[5:]
                class_current = np.argmax(scores)
                confidence_current = scores[class_current]

                if confidence_current > probability_minimum:
                    box_current = detected_objects[0:4] * np.array([w, h, w, h])
                    x_center, y_center, box_width, box_height = box_current
                    x_min = int(x_center - (box_width / 2))
                    y_min = int(y_center - (box_height / 2))
                    bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                    confidences.append(float(confidence_current))
                    class_numbers.append(class_current)

        results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)

        if len(results) > 0:
            for i in results.flatten():
                x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                box_width, box_height = bounding_boxes[i][1], bounding_boxes[i][1]
                colour_box_current = colours[class_numbers[i]].tolist()
                cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)

                object_class = labels[int(class_numbers[i])]

                # Verificar se uma garrafa foi detectada
                if object_class == "bottle":
                    bottle_detected = True

                text_box_current = '{}: {:.4f}'.format(object_class, confidences[i])
                cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)

                escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
                print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])

        # Detecção de rostos e reconhecimento facial
        faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)

        for (x, y, l, a) in faceDetectadas:
            imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
            cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
            id, confianca = reconhecedor.predict(imagemFace)

            if id == 1:
                nome = "Fabio"
            elif id == 2:
                nome = "Luiz"

            cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))

            # Associando objetos detectados com rostos reconhecidos
            if bottle_detected and nome == "Fabio":
                # Disparar o alarme
                tk.Tk().withdraw()  # Esconder a janela principal
                messagebox.showinfo("Alerta", "Deixa Garrafa Quieta Porra!")
                pygame.mixer.music.load('alert_sound.wav')
                pygame.mixer.music.play()

        # Exibir o frame resultante
        cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
        cv2.imshow('YOLO v3 WebCamera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()



# import numpy as np
# import cv2
# import time
# from csv import DictWriter
# import tkinter as tk
# from tkinter import messagebox
# import pygame
#
# # Inicializando o pygame
# pygame.mixer.init()
#
# # Carregando arquivo com o nome dos objetos
# with open('yoloDados/YoloNames.names') as f:
#     labels = [line.strip() for line in f]
#
# # Carregando os arquivos treinados pelo framework YOLO
# network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
# layers_names_all = network.getLayerNames()
# layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]
#
# # Definindo probabilidades mínimas e limite de filtragem
# probability_minimum = 0.5
# threshold = 0.3
# colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
#
# # Carregando classificador de faces
# classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# reconhecedor = cv2.face.LBPHFaceRecognizer_create()
# reconhecedor.read('classificadorLBPH_V1.yml')
#
# # Inicializando a câmera
# camera = cv2.VideoCapture(0)
#
# # Inicializando o arquivo CSV para salvar as detecções
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         start = time.time()
#         output_from_network = network.forward(layers_names_output)
#         end = time.time()
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][1], bounding_boxes[i][1]
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#                 # Trigger alert if a bottle is detected
#                 if int(class_numbers[i]) == 1:
#                     # Add your alert logic here
#                     if 'Fabio' in [linha['Detectado'] for linha in escritor_csv]:
#                         tk.Tk().withdraw()  # Hide the main window
#                         messagebox.showinfo("Alert", "Bottle Detected while Fabio is present!")
#                         pygame.mixer.music.load('alert_sound.wav')
#                         pygame.mixer.music.play()
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#         for (x, y, l, a) in faceDetectadas:
#             imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
#             cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
#             id, confianca = reconhecedor.predict(imagemFace)
#
#             if id == 1:
#                 nome = "Fabio"
#                 # Trigger alert sound if "Fabio" is detected
#                 #pygame.mixer.music.load('alert_sound.wav')
#                 #pygame.mixer.music.play()
#             elif id == 2:
#                 nome = "Luiz"
#
#             cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
#
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()


#
#
# import numpy as np
# import cv2
# import time
# from csv import DictWriter
# import tkinter as tk
# from tkinter import messagebox
# import pygame
#
# # Inicializando o pygame
# pygame.mixer.init()
#
# # Carregando arquivo com o nome dos objetos
# with open('yoloDados/YoloNames.names') as f:
#     labels = [line.strip() for line in f]
#
# # Carregando os arquivos treinados pelo framework YOLO
# network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
# layers_names_all = network.getLayerNames()
# layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]
#
# # Definindo probabilidades mínimas e limite de filtragem
# probability_minimum = 0.5
# threshold = 0.3
# colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
#
# # Carregando classificador de faces
# classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# reconhecedor = cv2.face.LBPHFaceRecognizer_create()
# reconhecedor.read('classificadorLBPH_V1.yml')
#
# # Inicializando a câmera
# camera = cv2.VideoCapture(0)
#
# # Inicializando o arquivo CSV para salvar as detecções
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         start = time.time()
#         output_from_network = network.forward(layers_names_output)
#         end = time.time()
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][1], bounding_boxes[i][1]
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#                 # Trigger alert if a bottle is detected
#                 if int(class_numbers[i]) == 1:
#                     # Add your alert logic here
#                     tk.Tk().withdraw()  # Hide the main window
#                     messagebox.showinfo("Alert", "Bottle Detected!")
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#         for (x, y, l, a) in faceDetectadas:
#             imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
#             cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
#             id, confianca = reconhecedor.predict(imagemFace)
#
#             if id == 1:
#                 nome = "Fabio"
#                 # Trigger alert sound if "Fabio" is detected
#                 pygame.mixer.music.load('alert_sound.wav')
#                 pygame.mixer.music.play()
#             elif id == 2:
#                 nome = "Luiz"
#             #elif id == 3:
#             #   nome = "aleta"
#
#             cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
#
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()

#-------------------------------------------------------------------------------
# import numpy as np
# import cv2
# import time
# from csv import DictWriter
# import tkinter as tk
# from tkinter import messagebox
# import pygame
# # Carregando arquivo com o nome dos objetos
# with open('yoloDados/YoloNames.names') as f:
#     labels = [line.strip() for line in f]
#
# # Carregando os arquivos treinados pelo framework YOLO
# network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
# layers_names_all = network.getLayerNames()
# layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]
#
# # Definindo probabilidades mínimas e limite de filtragem
# probability_minimum = 0.5
# threshold = 0.3
# colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
#
# # Carregando classificador de faces
# classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# reconhecedor = cv2.face.LBPHFaceRecognizer_create()
# reconhecedor.read('classificadorLBPH_V1.yml')
#
# # Inicializando a câmera
# camera = cv2.VideoCapture(0)
#
# # Inicializando o arquivo CSV para salvar as detecções
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         start = time.time()
#         output_from_network = network.forward(layers_names_output)
#         end = time.time()
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][1], bounding_boxes[i][1]
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#                 # # Trigger alert if a bottle is detected
#                 # if int(class_numbers[i]) == 1:
#                 #     # Add your alert logic here
#                 #     tk.Tk().withdraw()  # Hide the main window
#                 #     messagebox.showinfo("Alert", "Bottle Detected!")
#
#                 if int(class_numbers[i]) == 1:
#                     # Add your alert logic here
#                     tk.Tk().withdraw()  # Hide the main window
#                     messagebox.showinfo("Alert", "Bottle Detected!")
#
#                 # Trigger alert if "Fabio" is detected
#                 if int(class_numbers[i]) == 1:  # Assuming "Fabio" has label index 0
#                     # Add your alert logic here
#                     pygame.mixer.music.load('alert_sound.wav')
#                     pygame.mixer.music.play()
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#         for (x, y, l, a) in faceDetectadas:
#             imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
#             cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
#             id, confianca = reconhecedor.predict(imagemFace)
#
#             if id == 1:
#                 nome = "Fabio"
#             elif id == 2:
#                 nome = "Luiz"
#             #elif id == 3:
#             #   nome = "aleta"
#
#             cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
#
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()


# import numpy as np
# import cv2
# import time
# from csv import DictWriter
# import tkinter as tk
# from tkinter import messagebox
#
# # Carregando arquivo com o nome dos objetos
# with open('yoloDados/YoloNames.names') as f:
#     labels = [line.strip() for line in f]
#
# # Carregando os arquivos treinados pelo framework YOLO
# network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
# layers_names_all = network.getLayerNames()
# layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]
#
# # Definindo probabilidades mínimas e limite de filtragem
# probability_minimum = 0.5
# threshold = 0.3
# colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
#
# # Carregando classificador de faces
# classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# reconhecedor = cv2.face.LBPHFaceRecognizer_create()
# reconhecedor.read('classificadorLBPH_V1.yml')
#
# # Inicializando a câmera
# camera = cv2.VideoCapture(1)
#
# # Inicializando o arquivo CSV para salvar as detecções
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         start = time.time()
#         output_from_network = network.forward(layers_names_output)
#         end = time.time()
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][3], bounding_boxes[i][3]
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#                 # Trigger alert if a bottle is detected
#                 if int(class_numbers[i]) == 3:
#                     # Add your alert logic here
#                     tk.Tk().withdraw()  # Hide the main window
#                     messagebox.showinfo("Alert", "Bottle Detected!")
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#         for (x, y, l, a) in faceDetectadas:
#             imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
#             cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
#             id, confianca = reconhecedor.predict(imagemFace)
#
#             if id == 1:
#                 nome = "Vinicios"
#             elif id == 2:
#                 nome = "Zé drogues"
#             elif id == 3:
#                 nome = "aleta"
#
#             cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
#
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()

# import numpy as np
# import cv2
# import time
# from csv import DictWriter
#
# # Carregando arquivo com o nome dos objetos
# with open('yoloDados/YoloNames.names') as f:
#     labels = [line.strip() for line in f]
#
# # Carregando os arquivos treinados pelo framework YOLO
# network = cv2.dnn.readNetFromDarknet('yoloDados/yolov3.cfg', 'yoloDados/yolov3.weights')
# layers_names_all = network.getLayerNames()
# layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]
#
# # Definindo probabilidades mínimas e limite de filtragem
# probability_minimum = 0.5
# threshold = 0.3
# colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
#
# # Carregando classificador de faces
# classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# reconhecedor = cv2.face.LBPHFaceRecognizer_create()
# reconhecedor.read('classificadorLBPH_V1.yml')
#
# # Inicializando a câmera
# camera = cv2.VideoCapture(1)
#
# # Inicializando o arquivo CSV para salvar as detecções
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         start = time.time()
#         output_from_network = network.forward(layers_names_output)
#         end = time.time()
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#         faceDetectadas = classificador.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.5)
#
#         for (x, y, l, a) in faceDetectadas:
#             imagemFace = cv2.resize(cv2.cvtColor(frame[y:y + a, x:x + l], cv2.COLOR_BGR2GRAY), (100, 100))
#             cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
#             id, confianca = reconhecedor.predict(imagemFace)
#
#             if id == 1:
#                 nome = "Vinicios"
#             elif id == 2:
#                 nome = "Zé drogues"
#
#
#             cv2.putText(frame, nome, (x, y + (a + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
#
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()


# import numpy as np
# import cv2
# import time
# from csv import DictWriter
# import pywhatkit
# import keyboard
# from datetime import datetime
# from yolov3.yoloc3 import Yolo, camera
# # Load YOLO model and face classifier
# # ...
#
# # Load WhatsApp parameters
# numero = ['+5511982593295']
# mensagem = "Olá sou bot, Vinicius. Seu capacete está sendo roubado"
# imagem = [r'C:\Users\fabfe\PycharmProjects\OpenCVScript_4\pythonProject1\imagem\capacete\Image_1.jpg']
#
# # Start after 1 minute
# time.sleep(60)
#
# # Initialize CSV file
# with open('teste.csv', 'w') as arquivo:
#     cabecalho = ['Detectado', 'Acuracia']
#     escritor_csv = DictWriter(arquivo, fieldnames=cabecalho)
#     escritor_csv.writeheader()
#
#     while True:
#         _, frame = camera.read()
#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         network.setInput(blob)
#         output_from_network = network.forward(layers_names_output)
#
#         bounding_boxes = []
#         confidences = []
#         class_numbers = []
#
#         for result in output_from_network:
#             for detected_objects in result:
#                 scores = detected_objects[5:]
#                 class_current = np.argmax(scores)
#                 confidence_current = scores[class_current]
#
#                 if confidence_current > probability_minimum:
#                     box_current = detected_objects[0:4] * np.array([w, h, w, h])
#                     x_center, y_center, box_width, box_height = box_current
#                     x_min = int(x_center - (box_width / 2))
#                     y_min = int(y_center - (box_height / 2))
#                     bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
#                     confidences.append(float(confidence_current))
#                     class_numbers.append(class_current)
#
#         results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
#
#         if len(results) > 0:
#             for i in results.flatten():
#                 x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
#                 box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]
#
#                 # Check if the detected object is a bottle (ID = 2)
#                 if class_numbers[i] == 2:
#                     # Send WhatsApp message
#                     for num in numero:
#                         pywhatkit.sendwhatmsg(num, mensagem, datetime.now().hour, datetime.now().minute + 2)
#                         time.sleep(15)  # Wait 15 seconds before pressing enter
#                         keyboard.press_and_release('enter')
#                         time.sleep(5)  # Wait 5 seconds after sending message
#
#                         # Send the image
#                         pywhatkit.sendwhats_image(num, imagem[0], "Imagem1")
#                         time.sleep(10)  # Wait 10 seconds before pressing enter
#                         keyboard.press_and_release('enter')
#                         time.sleep(60)  # Wait 1 minute after sending image
#                         keyboard.press_and_release('ctrl + w')  # Close WhatsApp window
#                         break  # Exit the loop after sending message and image
#
#                 # Draw bounding box and label for detected object
#                 colour_box_current = colours[class_numbers[i]].tolist()
#                 cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 2)
#                 text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])], confidences[i])
#                 cv2.putText(frame, text_box_current, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
#                 escritor_csv.writerow({"Detectado": text_box_current.split(':')[0], "Acuracia": text_box_current.split(':')[1]})
#                 print(text_box_current.split(':')[0] + " - " + text_box_current.split(':')[1])
#
#         # Display the frame
#         cv2.namedWindow('YOLO v3 WebCamera', cv2.WINDOW_NORMAL)
#         cv2.imshow('YOLO v3 WebCamera', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# camera.release()
# cv2.destroyAllWindows()