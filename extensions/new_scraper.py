import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse
from extensions.utils import time_me


# Right now one page takes 31 seconds to load
def run():
    url = "https://sfbay.craigslist.org/search/sfc/apa"
    ranked = []
    housing_urls = souper(url)
    sqft_list = []
    # goes through 24 pages of craigslist
    for i, url in enumerate(housing_urls):
        sqft =sqft_search(url)
        if  sqft:
            sqft_list.append(sqft)

        #section_ranked = rank_sqft(sqft_urls)
        # for j in range(len(section_ranked)):
        #     ranked.append(section_ranked[j])
        #
        # # check for all pages at home
        # if i < 23:
        #     url = next_page(url)
        # else:
        #     break
    sqft_list_flat = [item for sublist in sqft_list for item in sublist]
    # this invocation of the method orders all of the apartments by sqft
    final_ranks = rank_sqft(ranked)

    # info of sqft apartments w/o pictures and urls
    apts, urls = info_of_apts(final_ranks)

    # pictures
    pic_pairs = pic_return(urls)
    dwnloaded_pics(pic_pairs)
    # printed out info

    storage_file = open("apt_info.txt", "w+")
    for i in range(len(apts)):
        storage_file.write("\n")
        storage_file.write(str(i + 1) + ". ")
        storage_file.write(("title:  " + str(apts[i][1])).encode("utf-8").decode("utf-8"))
        storage_file.write("\n")
        storage_file.write("sqft: " + str(apts[i][3]))
        storage_file.write(" price:  " + str(apts[i][0]))
        storage_file.write(" location: " + str(apts[i][2]))
        storage_file.write(" url:  " + str(urls[i]))

        storage_file.write("\n")

    # with pictures


# supposed to get all of the links from each page
def souper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul', {'class': 'rows'})
    s = 0

    # supposed to have the urls for the 1 page
    housing_urls = []
    li_tags = soup.findAll('li', {'class': 'result-row'})
    for i in range(len(li_tags)):
        for tag in li_tags[i].find_all('a'):
            if s % 3 == 0:
                housing_urls.append(tag.get('href', None))
            s += 1

    return housing_urls


# supposed to find the features of the page of apartments and return a ranking, takes a while for it run
def sqft_search(url):
   # list of sqft and corresponding urls
    sqfts = None
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    spans = soup.findAll('span', {'class': 'housing'})
    if len(spans) != 0:
        if re.search('.+\-(.+)ft.+', spans[0].text):
            sqfts = re.findall('.+\- (.+)ft.+', spans[0].text)

    return sqfts


# in this method a page's apartments are ordered by sqft and repeated listings are removed
def rank_sqft(sqft_urls):
    sqft_urls.sort()
    sqft_urls.reverse()
    # print(sqft_urls[0][0])
    sqft_urls = repeat_check(sqft_urls)

    ranks = sqft_urls

    return ranks


# include the pictures later
def info_of_apts(final_ranks):
    apts_5 = []
    price = ""
    title = ""
    location = ""
    sqft = ""
    pic_urls = []
    for i in range(len(final_ranks)):
        if i < 6:
            r = requests.get(final_ranks[i][1])
            soup = BeautifulSoup(r.text, 'html.parser')
            spans_price = soup.findAll('span', {'class': 'price'})
            spans_title = soup.findAll('span', {'id': 'titletextonly'})
            spans_location = soup.findAll('small')
            if len(spans_price) != 0 and len(spans_price) != 0 and len(spans_location) != 0:
                price = str(spans_price[0].text)
                title = str(spans_title[0].text)
                location = str(spans_location[0].text)
                sqft = final_ranks[i][0]
                if sqft < 10000:
                    apts_5.append([price, title, location, sqft])
                    pic_urls.append(final_ranks[i][1])
            else:
                continue

    return apts_5, pic_urls


def repeat_check(sqft_urls):
    no_repeats = sqft_urls
    url_string = ""
    removing = []
    for i in range(len(sqft_urls) - 1):
        j = i + 1
        url_string = sqft_urls[i][1]
        url_st = sqft_urls[j][1]
        # re.search('.+\/d/(.+)\/.+',url_string)
        lists = re.findall('.+\/d/(.+)\/.+', url_string)
        temp = re.findall('.+\/d/(.+)\/.+', url_st)
        if lists[0] == temp[0]:
            # print("check")
            removing.append([sqft_urls[j][0], sqft_urls[j][1]])

    for counter in range(len(removing)):
        no_repeats.remove(removing[counter])

    return no_repeats


def next_page(url):
    r = requests.get(url)
    new_url = ""
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags = soup.findAll('a', {'class': 'button next'})
    for tag in a_tags:
        new_url = tag.get('href', None)

    return "https://sfbay.craigslist.org" + new_url


# this method should give 2 pic_urls to later be downloaded
def pic_return(urls):
    pic_pairs = []
    pic_urls = []

    for i in range(len(urls)):
        r = requests.get(urls[i])
        # is the literal picture urls, supposed to have 2 of them
        soup = BeautifulSoup(r.text, 'html.parser')
        div_tags = soup.findAll('div', {'id': 'thumbs'})
        s = 0
        for i in range(len(div_tags)):
            for tag in div_tags[i].find_all('a'):
                if s < 2:
                    pic_urls.append(tag.get('href', None))
                    s += 1

        pic_pairs.append([pic_urls[len(pic_urls) - 2], pic_urls[len(pic_urls) - 1]])

    return pic_pairs


def dwnloaded_pics(pic_pairs):
    for i in range(len(pic_pairs)):
        for j in range(len(pic_pairs[i])):
            with open('apt' + str(i + 1) + '-' + str(j + 1) + '.jpg', 'wb') as handle:
                r = requests.get(pic_pairs[i][j], stream=True)
                print("attempting download...")
                if not r.ok:
                    print(r)

                for block in r.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            print(handle)
    return 0


@time_me
def main():
    run()


if __name__ == "__main__":
    main()