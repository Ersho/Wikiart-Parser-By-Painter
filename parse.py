from bs4 import BeautifulSoup
import os
from urllib import request

header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

def get_image_url(href, url = 'https://www.wikiart.org'):
    
    whole_url = url + href
    page = request.urlopen(whole_url)
    page_html = BeautifulSoup(page, 'lxml')
    img_url = page_html.find('img', {"class" : "ms-zoom-cursor"})
   
    if img_url:
        return img_url['src']
    else:
        print('Image not found ')
        return False
            
def save_image(img, author, name):
    try:
        save_name = 'data/'+ str(author) + '/' + str(name) + '.jpg'
        request.urlretrieve(img, save_name)
        return True    
    except Exception as e:
        print('Exception {} has occured on image {}'.format(e, name))
        return False

def save_image_directly(author, name, url = 'https://uploads4.wikiart.org/images/'):
    try:
        whole_url = url + str(author) + '/' + str(name) + '.jpg!Large.jpg'
        save_name = 'data/'+ str(author) + '/' + str(name) + '.jpg'
        request.urlretrieve(whole_url, save_name)
        
        return True
    
    except Exception as e:
        print('Exception {} has occured on image {}, trying with undirect URL'.format(e, name))
        
        return False

def main(author):
    
    url = 'https://www.wikiart.org/en/{}/all-works/text-list'.format(str(author))
    html = request.urlopen(url)
    
    path = os.path.join('data', author)
        
    if not os.path.exists(path):
        os.mkdir(path)
    
    soup = BeautifulSoup(html, 'lxml')
    
    find_text = soup.find_all('li', 'painting-list-text-row')
    
    for picture in find_text:
        location_header = picture.find('a')
        href = location_header['href']
    
        name = href.split('/')[-1]    
        
        img_path = os.path.join(path, name) + '.jpg'
        
        if os.path.exists(img_path):
            print("Image with the name {} already exists. Going to next one".format(name))
            continue
        else:
            print("Creating image file for {}".format(name))
            
        if not save_image_directly(author, name):
            img_url = get_image_url(href)
            save_image(img_url, author, name)

if __name__ == '__main__':
    #change author name here
    main('niko-pirosmani')
