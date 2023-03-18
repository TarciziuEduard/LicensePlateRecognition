# import required libraries
import string
import re
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tkinter import *
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read input image



def verificare_numar():

    cap = cv2.VideoCapture('proba2.mp4')
    config = ('-l eng --oem 1 --psm 3')
    number_list=[]
    dictionar={}
    elements_count = {}
    while (cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            cv2.imshow('original video', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # read haarcascade for number plate detection
            cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

            # Detect license number plates
            plates = cascade.detectMultiScale(gray, 1.2, 5)
            print('Number of detected license plates:', len(plates))

            # loop over all plates
            for (x, y, w, h) in plates:
                # draw bounding rectangle around the license number plate
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                gray_plates = gray[y:y + h, x:x + w]


                # save number plate detected
                #Extract Text from Images
                pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                text = pytesseract.image_to_string(gray_plates, config=config)
                #Filtram textul
                text=text[:8]
                filter(not(str.isdigit)and not(str.isascii) and not(str.isupper), text)
                text.translate({ord(c):None for c in string.whitespace})
                print('Remove all spaces using regex:\n', re.sub(r"\s+", "", text), sep='')

                #Introducem posibilele texte in vector
                if(text!=''):
                    number_list.append(text)

                font =  cv2.COLOR_BGR2RGB
                # Use putText() method for
                # inserting text on video
                cv2.putText(img, text, (x-5, y-5), font, 1, (0, 255, 0), 2, cv2.LINE_4)



                cv2.imwrite('Numberplate.jpg', gray_plates)
                cv2.imshow('Number Plate', gray_plates)
                cv2.imshow('Number Plate Image', img)
        else:
            cap.release()
            cv2.destroyAllWindows()

    for element in number_list:
        if element in elements_count:
            elements_count[element]+=1
        else:
            elements_count[element]=1


    max_keys = [key for key, value in elements_count.items() if value == max(elements_count.values())]
    print("\n\tNUMARUL DETECTAT ESTE:")
    print(max_keys)

    return max_keys





def onClick():

    web = webdriver.Chrome()
    web.maximize_window()
    web.get('https://www.aida.info.ro/polite-rca')


    tip_verificare = web.find_element(By.XPATH, '//*[@id="numar"]')
    tip_verificare.click()


    introduceti_numar = web.find_element(By.XPATH, '//*[@id="SerieNumar"]')
    introduceti_numar.send_keys(text)
    time.sleep(1)


    termeni_conditii = web.find_element(By.XPATH, '//*[@id="EsteDeAcordCuConditiile"]')
    termeni_conditii.click()

    #time.sleep(5)

    time.sleep(50)
    web.quit()





if __name__ == "__main__":

    text=verificare_numar()

    window = Tk()
    window.title('Verificare Asigurare Auto')
    window.geometry("320x200+10+20")

    label1 = Label(window, text="Numarul detectat este:")
    label1.place(x=45, y=10)
    label3 = Label(window, text=text)
    label3.place(x=170, y=10)
    label2=Label(window,text="Doriti sa verificati daca numarul are asigurare?")
    label2.place(x=45,y=50)
    button1 = Button(window,text="DA",fg='blue',command=onClick)
    button1.place(x=70,y=120)
    button2 = Button(window, text="NU",fg='red', command=window.destroy)
    button2.place(x=200,y=120)


    window.mainloop()




