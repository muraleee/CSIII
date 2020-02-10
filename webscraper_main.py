import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse

#Right now one page takes 31 seconds to load
def run():
    url = "https://sfbay.craigslist.org/search/sfc/apa"

    housing_urls= []
    sqft_urls= [] 
    section_ranked=[]
    #all of the apts
    ranked = []
    final_ranks=[]
    apts= []
    #goes through 24 pages of craigslist  
    for i in range(24):
          if i==0:
            housing_urls=souper(url)
            sqft_urls=sqft_search(housing_urls)
            section_ranked= rank_sqft(sqft_urls)
            for j in range(len(section_ranked)) :
                ranked.append(section_ranked[j])
            
            '''
            if i < 23:
              url= next_page(url)
       # if i==1:
           #housing_urls=souper(url)
           '''

    #this invocation of the method orders all of the apartments by sqft
    final_ranks=rank_sqft(ranked)   

    #info of sqft apartments w/o pictures
    apts, pic_urls=info_of_apts(final_ranks)

    #pictures 
    
    #printed out info

    storage_file = open("apt_info.txt", "w")
    for i in range(len(apts)):
        storage_file.write(str(i+1)+". ")
        storage_file.write("title:  "+ apts[i][1])
        storage_file.write("\n")
        storage_file.write("sqft: " + str(apts[i][3]))
        storage_file.write(" price:  "+apts[i][0])
        storage_file.write(" location:  "+ apts[i][2])



    # with pictures     

#supposed to get all of the links from each page
def souper(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul',{'class':'rows'})
    s=0

    #supposed to have the urls for the 1 page
    housing_urls= []
    li_tags= soup.findAll('li',{'class':'result-row'})
    for i in range(len(li_tags)):
      for tag in li_tags[i].find_all('a'):
           if s%3==0:
             housing_urls.append(tag.get('href',None))
           s+=1       
    
    #need to find a way to isolate the link

    #print(li_tags[0])
    '''
    for child in ul_tags[0].children:
        if z==0:
          print(child)
          #s=re.findall('<a.+', child)
    '''    
        
           

    '''
    for index in range(len(ul_tags)): 
        for child in ul_tags[index].children:
            if z== 0:
              print(child)
            z+=1
    '''
    return housing_urls

#supposed to find the features of the page of apartments and return a ranking, takes a while for it run
def sqft_search(housing_urls):
    housing_urls = housing_urls
   #list of sqft and corresponding urls
    sqft_urls =[]
    for i in range(len(housing_urls)): 
          r= requests.get(housing_urls[i]) 
          soup= BeautifulSoup(r.text, 'html.parser')

          spans= soup.findAll('span',{'class':'housing'})
          if len(spans) != 0:
            if re.search('.+\-(.+)ft.+',spans[0].text):
              sqfts= re.findall('.+\- (.+)ft.+',spans[0].text)
              sqft_urls.append([int(sqfts[0]), housing_urls[i]])
              print("done")
            else:
               housing_urls[i]= "error"
            spans.clear() 

                     
    return sqft_urls

#in this method a page's apartments are ordered by sqft and repeated listings are removed
def rank_sqft(sqft_urls):
 
  sqft_urls.sort() 
  sqft_urls.reverse()      
  #print(sqft_urls[0][0])
  sqft_urls = repeat_check(sqft_urls)

  ranks= sqft_urls
  
  return ranks

#include the pictures later
def info_of_apts(final_ranks):
  apts_5= []
  price= ""
  title= ""
  location= ""
  sqft=""
  pic_urls=[]
  for i in range(len(final_ranks)):
     if i < 5:
       r= requests.get(final_ranks[i][1])
       soup = BeautifulSoup(r.text, 'html.parser')
       spans_price= soup.findAll('span',{'class':'price'})
       spans_title= soup.findAll('span',{'id':'titletextonly'})
       spans_location= soup.findAll('small')
       if len(spans_price) != 0:
        price=str(spans_price[0].text)
       if len(spans_price) != 0:
        title=str(spans_title[0].text)
       if len(spans_location) != 0:
        location=str(spans_location[0].text)
       sqft= final_ranks[i][0]
       apts_5.append([price,title,location,sqft])
       pic_urls.append(final_ranks[i][1])

      
  return apts_5, pic_urls
    

def repeat_check(sqft_urls):
     no_repeats = sqft_urls
     url_string= ""
     removing= []
     for i in range(len(sqft_urls)-1):
        j=i+1
        url_string= sqft_urls[i][1]
        url_st= sqft_urls[j][1]
        #re.search('.+\/d/(.+)\/.+',url_string)
        lists= re.findall('.+\/d/(.+)\/.+',url_string)
        temp= re.findall('.+\/d/(.+)\/.+',url_st)
        if lists[0] == temp[0]:
           #print("check")
           removing.append([sqft_urls[j][0],sqft_urls[j][1]])

     for counter in range(len(removing)):
        no_repeats.remove(removing[counter])


     
     return no_repeats

def next_page(url):
    r= requests.get(url)
    new_url= ""
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags= soup.findAll('a',{'class':'button next'})
    for tag in a_tags:
        new_url = tag.get('href', None)
    
    
    return "https://sfbay.craigslist.org"+ new_url



#method is supposed to download pictures
def pic_return(pic_urls):
     return 0
run()

