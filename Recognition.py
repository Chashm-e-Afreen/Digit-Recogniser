
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import Button, Canvas, LEFT, Tk, Label, YES, BOTH
# import torchvision
# import torch
import torch
import tkinter.font as font
# import model_test
import numpy as np
import torch
import torchvision
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
from time import time
from PIL import ImageTk, Image, ImageDraw, ImageOps, ImageFilter
from torchvision import datasets, transforms
from torch import nn, optim
from tkinter import messagebox
from pathlib import Path

transform = transforms.Compose([transforms.ToTensor(),
                              transforms.Normalize((0.5,), (0.5,)),
                              ])
width = 500
height = 500
center = height//2
white = (255, 255, 255)
green = (0,128,0)
black = (0,0,0)

dir1 = Path(__file__).parent.absolute()
model = torch.load( str(dir1) + '/mnist1.pth')

def predict():
    img = Image.open(str(dir1) + '/image.png')
    img = img.resize((28,28),Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
    img = ImageOps.grayscale(img)
    img = transform(img)
    im2arr = np.array(img)
    # im2arr = np.array([(255 - x)/255. for x in im2arr])
    tensor1 = torch.from_numpy(im2arr)
    with torch.no_grad():
        logps = model(tensor1.view(1,784).float())

# Output of the network are log-proba  bilities, need to take exponential for probabilities
    ps = torch.exp(logps)
    probab = list(ps.numpy()[0])
    # print("Predicted Digit =", probab.index(max(probab)))
    a = "Predicted Digit =" + str(probab.index(max(probab)))
    # label = Label(root, text = a)
    label['text'] = a
    

def save():
    filename = str(dir1) + '/image.png'
    image1.save(filename, as_gray = True)
    predict()


def paint(event):
    # python_green = "#476042"
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    cv.create_oval(x1, y1, x2, y2, fill="white",width=10)
    draw.line([x1, y1, x2, y2],fill="white",width=10)

def erase():
    cv.delete("all")
    draw.rectangle((0, 0, 500, 500), fill=(0, 0, 0, 0))
    #label.pack_forget()
    
    # txt.delete('1.0', END)


root = Tk()
label = Label(root)
myFont = font.Font(family='Victor Mono', size=13)
# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()

image1 = PIL.Image.new("RGB", (width, height), black)
draw = ImageDraw.Draw(image1)


cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

label = Label(root, text = "Predicted Digit = ")
label.pack()
button=Button(text="Erase",command=erase)
button.pack(side= LEFT)
button1=Button(text="Predict",command=save)
button1.pack(side = LEFT)
button['font'] = myFont
button1['font'] = myFont
root.title('Digit Recogniser')
root.mainloop()

