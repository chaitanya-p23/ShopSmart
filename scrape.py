import httpx
import re
import json
from bs4 import BeautifulSoup
import locale
import cchardet
locale.setlocale(locale.LC_MONETARY, 'en_IN')
#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0', 'referer':'https://www.google.com'}

months = {
    'Jan' : '1',
    'Feb' : '2',
    'Mar' : '3',
    'Apr' : '4',
    'May' : '5',
    'Jun' : '6',
    'Jul' : '7',
    'Aug' : '8',
    'Sep' : '9',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12'
}

def flipkart(product, pincode, q) :
    client = httpx.Client(follow_redirects=True)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0', 'referer':'https://www.google.com'}
    URL_orig = "https://www.flipkart.com"
    URL = URL_orig + '/search?q=' + product
    r = client.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    parent = soup.find_all('div', attrs={'class':re.compile('^_13oc-S')})
    prod_page=None
    if len(parent[0]) == 1 :
        for prod in parent :
            if prod.find('div', attrs={'class':'_2tfzpE'}) is None :
                prod_page = prod
                break
    else :
        row_prod = parent[0].contents
        for prod in row_prod :
            if prod.find('span').text != "Sponsored" :
                prod_page = prod
                break
    url = prod_page.find('a')['href']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0', 'Referer':'https://www.flipkart.com', 'Origin':'https://www.flipkart.com', 'X-User-Agent':'X-User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0 FKUA/website/42/website/Desktop'}
    api = "https://1.rome.api.flipkart.com/api/4/page/fetch"
    prod_json = {'locationContext':{'pincode':pincode}, 'pageUri': url, 'isReloadRequest':True}
    prod_fetch = httpx.Client(follow_redirects=True).post(api, json=prod_json, headers=headers)
    prod = prod_fetch.json()['RESPONSE']['pageData']['pageContext']
    price = locale.currency(prod['pricing']['finalPrice']['value'], grouping=True)[:-3]
    rating = prod['rating']['average']
    try :
        delivery = prod['trackingDataV2']['slaText']
        if delivery[1].isdigit() :
            delivery_num = int(delivery[3:6]+delivery[:2])
        else :
            delivery_num = int(delivery[2:5]+'0'+delivery[0])
    except :
        delivery = "Not deliverable to " + pincode
        delivery_num = 1232
    
    q.put([price, rating, delivery, URL_orig+url, delivery_num])

def amazon(product, pincode, q) :
    client = httpx.Client(follow_redirects=True)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0', 'referer':'https://www.google.com'}
    URL = "https://www.amazon.in/s?k="
    URL += product.replace(' ', '+')
    r = client.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    cookies =  r.cookies
    headers = r.headers
    anti_csrf = json.loads(soup.find('span', attrs={'id':'nav-global-location-data-modal-action'})['data-a-modal'])['ajaxHeaders']['anti-csrftoken-a2z']
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0', 'anti-csrftoken-a2z':anti_csrf}
    client.post('https://www.amazon.in/portal-migration/hz/glow/address-change?actionSource=glow', headers=headers, cookies=cookies, data={"locationType":"LOCATION_INPUT","zipCode":pincode,"deviceType":"web","storeContext":"generic","pageType":"Search","actionSource":"glow"})
    r = client.get(URL, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.text, 'lxml')
    prod = soup.find('div', attrs={'class':'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
    prod_link = prod.find('a', attrs={'class':'a-link-normal s-no-outline', 'target':'_blank'})
    link=prod_link['href'][prod_link['href'].find('&url')+1:]
    r = client.get("https://www.amazon.in"+link, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.text, 'lxml')
    block = soup.find('div', attrs={'id':'newAccordionRow_0'})
    price = '₹' + block.find('span', attrs={'class':'a-color-price'}).text.strip()[:-3]
    rating = soup.find('span', attrs={'id':'acrPopover', 'class':'reviewCountTextLinkedHistogram noUnderline'})['title'][:3]
    if (block.find('div', attrs={'id':'mir-layout-DELIVERY_BLOCK-slot-SECONDARY_DELIVERY_MESSAGE_LARGE'})) :
        delivery = block.find('div', attrs={'id':'mir-layout-DELIVERY_BLOCK-slot-SECONDARY_DELIVERY_MESSAGE_LARGE'}).find('span', attrs={'class':'a-text-bold'}).text
    else :
        delivery = block.find('div', attrs={'id':'mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE'}).find('span', attrs={'class':'a-text-bold'}).text
    comma = delivery.find(',')
    if comma == -1 :
        delivery_num = months[delivery[8:11]] + delivery[5:7]
    else :
        if delivery[comma+3].isdigit() :
            delivery_num = int(months[delivery[comma+5:comma+8]] + delivery[comma+2:comma+4])
        else :
            delivery_num = int(months[delivery[comma+4:comma+7]] + '0' + delivery[comma+2])

    q.put([price, rating, delivery, "https://www.amazon.in"+link, delivery_num])

def rd(product, pincode, q) :
    client = httpx.Client(follow_redirects=True)
    url_orig = "https://www.reliancedigital.in"
    url = url_orig + '/search?q=' + product + ":relevance"
    r = client.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    redirect = soup.find('div', attrs={'class':'sp grid'}).find('a')['href']
    url = url_orig + redirect
    r = client.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    price = '₹' + soup.find('li', attrs={'class':'pdp__priceSection__priceListText'}).find('span').find_all('span')[1].text[:-3]
    try :
        rating_block = soup.find('div', attrs={'class':'pdp__rating mr__16'}).find('span')
        rating = len(rating_block.find_all('i', attrs={'class':'fa fa-star'})) + len(rating_block.find_all('i', attrs={'class':'fa fa-star-half-o'}))/2
    except :
        rating = 0
    productcode = soup.find('meta', attrs={'property':'product:retailer_item_id'})['content']
    delivery_url = "https://www.reliancedigital.in/rildigitalws/v2/rrldigital/productavailability/serviceability?productcode=" + productcode + "&toPincode=" + pincode
    delivery = client.get(delivery_url).json()['data']['serviceabilityInfo']['expectedDeliveryTime']
    if delivery is None : 
        delivery = "Not deliverable to " + pincode
        delivery_num = 1232
    else :
        delivery_num = int(months[delivery[3:6]]+delivery[:2])
    q.put([price, rating, delivery, url,delivery_num])
