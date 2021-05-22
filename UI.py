# -*- coding: utf-8 -*-
"""
@author: Tarun Arora
"""

import tkinter as tk
from tkinter import Message,Text
from PIL import ImageTk,Image
import cv2
import numpy as np
import keras
import time
import sys
import keras
from keras.models import load_model
from keras import models,layers
from keras import optimizers
import tensorflow as tf

window = tk.Tk()
window.title("Sign Language Detection")
dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

#window.attributes('-fullscreen', True)

window.geometry('1400x760')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

image1= tk.PhotoImage(file = "asl.png")
label_for_image= tk.Label(window, image=image1)
label_for_image.pack()

message = tk.Label(window, text="Sign Language Detector" , fg='black' ,bg="white"  ,width=20  ,height=3,font=('times', 30, 'italic bold underline'))
message.place(x=450, y=400)

lbl3 = tk.Label(window, text="Word(s) Detected:",width=20  ,fg="black"  ,bg="cyan"  ,height=2 ,font=('times', 15, ' bold underline '))
lbl3.place(x=300, y=560)

message = tk.Label(window, text="" ,bg="cyan"  ,fg="black"  ,width=35  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message.place(x=600, y=560)

res1 = ""

def clear():
    global res1
    res = ""
    res1 = ""
    message.configure(text= res)
    
def pronounce():
    global res1
    from win32com.client import Dispatch 
    speak = Dispatch("SAPI.Spvoice") 
    speak.Speak(res1)
    

def real_time():
    global res1
    model = load_model('asl_alphabet.h5')
    classes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'del', ' ', 'Nothing']

    cur_text = ''
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        cv2.rectangle(frame, (50, 50), (350, 350), (0, 255, 0), 3)

        cropped_image = frame[50:350, 50:350]
        resized_frame = cv2.resize(cropped_image, (200, 200))
        reshaped_frame = (np.array(resized_frame)).reshape((1, 200, 200, 3))
        frame_for_model = reshaped_frame / 255
        prediction = np.array(model.predict(frame_for_model))
        predicted_class = classes[prediction.argmax()]

        prediction_probability = prediction[0, prediction.argmax()]
        if prediction_probability > 0.2:
            cv2.putText(frame, '{} - {:.2f}%'.format(predicted_class, prediction_probability * 100),
                        (10, 450), 1, 2, (255, 255, 0), 2, cv2.LINE_AA)
            keypress = cv2.waitKey(1)
            if keypress == ord('s'):
                alph = predicted_class  # chr(num+96)
                cur_text += alph
                res1 += alph
                print(cur_text)
            elif keypress == ord('q'):
                break
        else:
            cv2.putText(frame, 'space', (10, 450), 1, 2, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    message.configure(text = cur_text)
    cap.release()
    cv2.destroyAllWindows()

clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="orange"  ,width=10  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=850, y=620)

takeImg = tk.Button(window, text="Open Camera to detect", command = real_time, fg="black"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=20, y=600)

photo = tk.PhotoImage(file= "pro1.png")
speakup = tk.Button(window, image=photo, command = pronounce, bg="white"  ,width=100  ,height=100, activebackground = "Red")
speakup.place(x=700, y=620)

quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="red"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=600)

window.mainloop()
