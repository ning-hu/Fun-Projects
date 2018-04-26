import os
import re
import sys
import requests
from bs4 import BeautifulSoup

# store image url that I want to save in img
def get_img(soup):
    img_link = soup.select(".background-mask")
    my_img = img_link[0].select('img')
    img = my_img[0]['src']
    return img

# get the monster number and store it in num
# only 1 number under the pcprofile class
def get_num(soup): 
    num_string = soup.select(".pcprofile")
    temp = str(num_string)
    num = re.findall("[0-9]+", temp)[0]
    return num

# change start_url to the next one that i need
# on the first and last pages, there is only one link
# on the other pages, there are two links
def get_next_url(soup, num):
    url_front = "http://monst.appbank.net/monster/"
    url_link = soup.select("div.page-nav.clearfix")
    all_links = url_link[0].find_all("a")

    if len(all_links) == 2:
        start_url = url_front + all_links[1]['href']
    elif num == '1': # so the link on the last page doesn't cause an infinite loop
        start_url = url_front + all_links[0]['href']
    else:
        start_url = None
    return start_url

def main():
    # get HTML for the starting page
    start_url = "http://monst.appbank.net/monster/1.html"

    # folder you want to save the images in
    save_dir = "/Users/ninghu/Documents/Monsterstrike"

    while (1):
        page = requests.get(start_url)
        html = page.content

        # parse the html
        soup = BeautifulSoup(html, 'html.parser')

        img = get_img(soup)
        num = get_num(soup)
        start_url = get_next_url(soup, num)

        # check that the file exists, and if it does, ignore it and continue
        my_file = save_dir + num + ".jpg"
        if os.path.isfile(my_file) == False:
            f = open(os.path.join(save_dir, num + ".jpg"), "wb+")
            f.write(requests.get(img).content)
            f.close()

        if start_url == None:
            sys.exit(0)

if __name__ == "__main__":
    main()