"""
Code to parse

https://www.davidrumsey.com

"""
from bs4 import BeautifulSoup
import os
from urllib import request
import numpy as np
from multiprocessing import Process
from threading import Thread

header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
   
#url = "https://www.davidrumsey.com/rumsey/Size2/RUMSEY~8~1/179/13129003.jpg"

def trim_string(string):
    
    out = string.replace(':', '')
    out = out.replace('?', '')
    out = out.replace('/', '')
    out = out.replace('*', '')
    out = out.replace('"', '')
    out = out.replace('<', '')
    out = out.replace('>', '')
    out = out.replace('|', '')
    out = out.replace('\\', '')
    
    return out

def save_image(img, name):
    try:
        
        name = trim_string(name)
        
        save_name = 'data/davidrumsey/'+ str(name) + '.jpg'
        
        while os.path.isfile(save_name):
            save_name = 'data/davidrumsey/'+ str(name) + '-' + str(np.random.randint(0,10000)) + '.jpg'
            
        request.urlretrieve(img, save_name)
        return True    
    
    except Exception as e:
        print('Exception {} has occured on image {}'.format(e, name))
        return False
    
def get_img(index, iteration = 50):
    
    #page_url = "https://www.davidrumsey.com/luna/servlet/view/" \
    #            + "all?sort=Pub_List_No_InitialSort%2CPub_Date%2CPub_List_No%2CSeries_No&os=0"
    #increases os by 50 for next page
    
    print('Starting Getting images of pages with range {}'.format(index))
    
    page_url = "https://www.davidrumsey.com/luna/servlet/view/all?sort=" \
            + "Pub_List_No_InitialSort%2CPub_Date%2CPub_List_No%2CSeries_No&os={}".format(index-1)
    
    if not os.path.exists(os.path.join('data', 'davidrumsey')):
        os.mkdir(os.path.join('data','davidrumsey'))
    
    page = request.urlopen(page_url)
    page_html = BeautifulSoup(page, 'lxml')
    img_urls = page_html.find_all('img')
    
    for i in range(0, len(img_urls)):
        try:
            img = img_urls[i]['src']
            name = img_urls[i]['alt']
            
            save_image(img, name)
            
        except Exception as e:
            print('Exception {} has occured on image {}'.format(e, name))
            return False
    
    print('Finished sucessfully Getting images of pages with range {}'.format(index))
    
    return True

if __name__ == '__main__':
    
    for i in range(20701, 88768, 300):

        #get_img('https://media.davidrumsey.com/rumsey/Size4/RUMSEY~8~1/171/12241003.jpg')

        print('Starting process # {}'.format(i))
        
        p1 = Thread(target=get_img, args=(i,))
        p2 = Thread(target=get_img, args=(i + 50,))
        p3 = Thread(target=get_img, args=(i + 100,))
        p4 = Thread(target=get_img, args=(i + 150,))
        p5 = Thread(target=get_img, args=(i + 200,))
        p6 = Thread(target=get_img, args=(i + 250,))
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()