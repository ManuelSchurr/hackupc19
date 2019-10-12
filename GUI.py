import tkinter as tk
from tkinter import *
from PIL import Image

##Data to pass:
country="DE",
currency="EUR",
locale="DE",
destination_place="BER",
origin_place="FRA",
outbound_partial_date="2019-11-11",
inbound_partial_date="2019-11-12",
#more data
HEIGHT = 700,
WIDTH = 800,
dataRecieved = True

formHeight = 0.25
formFont = 40

# #Add Biene image (only need to use it once)
# filename = r'biene.jpg'
# img = Image.open(filename)
# img.save('biene.ico')

###### main:
root = tk.Tk()
root.title("Travel planner 4 cheapskates ©BIENE")
root.iconbitmap('biene.ico')


#RadioBox
var = IntVar()
def sel():
   selection = "You selected the option " + str(var.get())
#    radioLabel.config(text = selection)

def getData():
    dataRecieved = True
    offers(True)

#Seize of the Windows is set with the biggest "Form"
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#Formframe 
formFrame = tk.Frame(root, bg='#ccefff', bd=5)
formFrame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.4,anchor='n')

#Form - Subframes
subFrame1 = tk.Frame(formFrame)
subFrame2 = tk.Frame(formFrame)
subFrame3 = tk.Frame(formFrame)
subFrame4 = tk.Frame(formFrame)
subFrame5 = tk.Frame(formFrame)
subFrame6 = tk.Frame(formFrame)
subFrame7 = tk.Frame(formFrame)
subFrame8 = tk.Frame(formFrame)
subFrame1.place(relx=0.5, rely=0.000, relwidth=1, relheight=0.125,anchor='n')
subFrame2.place(relx=0.5, rely=0.125, relwidth=1, relheight=0.125,anchor='n')
subFrame3.place(relx=0.5, rely=0.250, relwidth=1, relheight=0.125,anchor='n')
subFrame4.place(relx=0.5, rely=0.375, relwidth=1, relheight=0.125,anchor='n')
subFrame5.place(relx=0.5, rely=0.500, relwidth=1, relheight=0.125,anchor='n')
subFrame6.place(relx=0.5, rely=0.625, relwidth=1, relheight=0.125,anchor='n')
subFrame7.place(relx=0.5, rely=0.750, relwidth=1, relheight=0.125,anchor='n')
subFrame8.place(relx=0.5, rely=0.875, relwidth=1, relheight=0.125,anchor='n')


#First Row (Default text)
currencyLabel = tk.Label(subFrame1, text="Your selected currency: ", bg='#ccefff', font = formFont)
currencyLabel.place(relwidth=0.7, relheight=1)
currencyText = tk.Label(subFrame1, text = currency, font = formFont)
currencyText.place(relx=0.7, relwidth=0.3, relheight=1)

#Second Row (Default text)
countryLabel = tk.Label(subFrame2, text="Your destiny city abbreviation:", bg='#ccefff', font = formFont)
countryLabel.place(relwidth=0.7, relheight=1)
countryText = tk.Label(subFrame2, text = country, font = formFont)
countryText.place(relx=0.7, relwidth=0.3, relheight=1)

#Third Row (Default text)
localeLabel = tk.Label(subFrame3, text="Your start city abbreviation: ", bg='#ccefff', font = formFont)
localeLabel.place(relwidth=0.7, relheight=1)
localeText = tk.Label(subFrame3, text = locale, font = formFont)
localeText.place(relx=0.7, relwidth=0.3, relheight=1)

#4. Row
destLabel = tk.Label(subFrame4, text="Enter your Destiny City Abbreviation", bg='#ccefff', font=formFont)
destLabel.place(relwidth=0.7, relheight=1)
destInput = tk.Entry(subFrame4, font=formFont)
destInput.insert(END, destination_place)
destInput.place(relx=0.7, relwidth=0.3, relheight=1)

#5. Row
orLabel = tk.Label(subFrame5, text="Enter your City Abbreviation", bg='#ccefff', font=formFont)
orLabel.place(relwidth=0.7, relheight=1)
orInput = tk.Entry(subFrame5, font=formFont)
orInput.insert(END, origin_place)
orInput.place(relx=0.7, relwidth=0.3, relheight=1)

#7. Row
outbLabel = tk.Label(subFrame6, text="Enter your outbound date (YYYY-MM-DD)", bg='#ccefff', font=formFont)
outbLabel.place(relwidth=0.7, relheight=1)
outbInput = tk.Entry(subFrame6, font=formFont)
outbInput.insert(END, outbound_partial_date)
outbInput.place(relx=0.7, relwidth=0.3, relheight=1)

#7. Row
inbLabel = tk.Label(subFrame7, text="Enter your inbound date (YYYY-MM-DD)", bg='#ccefff', font=formFont)
inbLabel.place(relwidth=0.7, relheight=1)
inbInput = tk.Entry(subFrame7, font=formFont)
inbInput.insert(END, inbound_partial_date)
inbInput.place(relx=0.7, relwidth=0.3, relheight=1)

# 8. Row Commit
button = tk.Button (subFrame8, text="Submit Data to get the best trip for me", font=35, bg='blue', command = getData)
button.place(relx=0.5, relwidth=1, relheight=1, anchor='n')


#Result Frame
def offers(myBool):
    if myBool:
        resultFrame = tk.Frame(root, bg='orange', bd=5)
        resultFrame.place(relx=0.5,rely=0.55, relwidth=0.85, relheight=0.25, anchor='n')
        #8. Row Radio Box
        R1 = Radiobutton(resultFrame, text="Fastest (1)", variable=var, value=1, command=sel)
        R2 = Radiobutton(resultFrame, text="Cheapest (2)", variable=var, value=2, command=sel)
        R3 = Radiobutton(resultFrame, text="Fewest Changes (3)", variable=var, value=3, command=sel)
        R1.pack( anchor = W )
        R2.pack( anchor = W )
        R3.pack( anchor = W)

offers(False)

getData
# label = Label(resultFrame)
# label.place()










### run in the main loop
root.mainloop()
