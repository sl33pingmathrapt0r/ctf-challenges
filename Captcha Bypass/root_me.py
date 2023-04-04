from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import base64
import numpy as np
import cv2
import pytesseract

# setup driver
driver= webdriver.Chrome('chromedriver')
driver.minimize_window()
url= 'http://challenge01.root-me.org/programmation/ch8/'
driver.get(url)

# while flag not found, keep attempting
flag= False
while not flag:
    # obtain image b64
    content= driver.page_source
    soup= bs(content, features= "html.parser")
    im_b64= soup.find('img').get('src').replace('data:image/png;base64,', '')

    # convert to cv2 img
    im_bytes= base64.b64decode(im_b64)
    im_arr= np.frombuffer(im_bytes, dtype= np.uint8)
    img= cv2.imdecode(im_arr, flags= cv2.IMREAD_COLOR)

    # image processing
    gray_img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur= cv2.GaussianBlur(gray_img, (3,3), 0)
    thresh= cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    opening= cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert= 255 - opening

    # tesseract text and processing
    text= pytesseract.image_to_string(invert, lang= 'eng', config='--psm 6')
    text= sorted(text.split(' '), key= lambda x: len(x), reverse=True)[0]
    start=0
    end=-1
    # trim invalid char for higher solve probability
    valid_range= [*range(ord('A'), ord('Z')+1)] + [*range(ord('a'), ord('z')+1)] + [*range(ord('0'), ord('9')+1)]
    while ord(text[start]) not in valid_range: start+=1
    while ord(text[end]) not in valid_range: end-=1
    text= text[start:len(text)+end+1]

    # submit form
    inputs= driver.find_elements(By.TAG_NAME, 'input')
    inputs[0].send_keys(text)
    inputs[1].click()

    # view image; delay for page to load and before window closes
    # cv2.imshow('processed_img', invert)
    # cv2.waitKey()

    # obtain return string, contains flag if successful
    p_elems= driver.find_elements(By.TAG_NAME, 'p')
    for p in p_elems: 
        if 'flag' in p.text: 
            flag= True
            flag_text= p.text

print(flag_text)
