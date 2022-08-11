
import os
import re
import time
from selenium import webdriver
#use By in selenium to find the element
from selenium.webdriver.common.by import By
from zipfile import ZipFile
import fitz
import pytesseract

class Elections:
    def __init__(self, candidates, voters):
        self.candidates = candidates
        self.voters = voters
        self.votes = {}
        self.percentages = {}
        for candidate in candidates:
            self.votes[candidate] = 0
        self.winner = None
        self.winner_votes = 0
        self.tie = False

        self.download_time = 1800

        self.base_url = "https://forms.iebc.or.ke/#/" # year, state
        self.driver = webdriver.Chrome('./chromedriver.exe')

   
        pytesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)

    def get_results(self):
        time.sleep(5)
        #webdriver wait till we find  class="download-results"
        download_forms = self.driver.find_element(By.CLASS_NAME, 'download-results')
        download_forms.click()
        print("Downloading results...")
        time.sleep(5)

        #find table with class q-table
        try:
            print("Trying to find table...")
            table = self.driver.find_element(By.CLASS_NAME, 'q-table')
            #go to the table body and for each row find the td element and get the text
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            print(len(rows))
            #loop through the rows and download the results
            for row in rows:
                #print len of
                print("Row: ", row)
                #data is in class="q-td text-right"
                time.sleep(5)
                data = row.find_element(By.CLASS_NAME, 'text-right')
                print("Data: ", data)              
                #click on a tag in the data to download the file
                file = data.find_element(By.TAG_NAME, 'a')
                print("File: ", file)
                file.click()
                time.sleep(3600)

            time.sleep(3600)
            print("Downloading complete...")

        except:
            print("No results found")
            pass
   
   #function to unzip
    def unzip(self):
        #find all files in the current directory
        files = os.listdir(os.getcwd())
        #loop through the files and unzip them
        for file in files:
            if file.endswith(".zip"):
                #use Zipfile to unzip the file
                with ZipFile(file, 'r') as zip:
                    #create a random folder to extract the file to
                    folder = os.path.basename(file).split('.')[0]
                    os.mkdir(folder)
                    #check if the folder is empty
                    if os.listdir(folder) == []:
                        #extract the file to the folder
                        zip.extractall(folder)
                        #delete the zip file
                        #navigate to the folder
                        os.chdir(folder)
                        #find all pdf files in the current directory
                        files = os.listdir(os.getcwd())
                        #loop through the files and open them and read the text
                        for file in files:
                            #use pypdf to extract text
                            pdf = fitz.open(file)
                          
                            images = pdf.get_page_images(0)
                            #loop through the images and save them to the current directory
                            for image in images:
                                print(image)
                                xref = image[0]
                                pix = fitz.Pixmap(pdf, xref)
                                if pix.n < 5:
                                    pix.save(file + ".png", "png")
                                pix = None
                            
                            #printlen(image_list), 'detected')
                            print(len(images), 'detected')


                    else:
                        print("Folder not empty")
                        pass


    def imagesData(self):
        #find all folders in the current directory
        folders = os.listdir(os.getcwd())
        #loop through the folders and find all files in the folder
        for folder in folders:
            #if the folder starts with 1_34 format
            if folder.startswith('1_34'):
                #navigate to the folder
                os.chdir(folder)
                #find all images in the current directory
                images = os.listdir(os.getcwd())
                #loop through the images and open them 
                for file in images:
                    #check if the file is an image
                    if file.endswith(".png"):
                        #initialize pytesseract library
                        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
                        #use pytesseract to extract text from the image
                        text = pytesseract.image_to_string(file)
                        #print the text
                        print(text)
                        #store the text in a dictionary
                        # self.images[file] = text
                        with open(file + ".txt", "w") as text_file:
                            text_file.write(text)
                        #navigate to the parent directory
                os.chdir("..")
      



  



#main function
def main():
    elections = Elections(["RAILA ODINGA", "WILLIAM SAMOEI RUTO", "GEORGE LUCHIRI WAJACKOYAH", "DAVID MWAURE WAIHIGA"], ["RAILA ODINGA", "WILLIAM SAMOEI RUTO", "GEORGE LUCHIRI WAJACKOYAH", "DAVID MWAURE WAIHIGA"])
    elections.get_results()
    elections.unzip()
    elections.imagesData()



if __name__ == '__main__':
    main()


