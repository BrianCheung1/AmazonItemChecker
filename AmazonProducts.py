from bs4 import BeautifulSoup
import requests
 
# Function to extract Product Title
def get_title(soup):
     
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
 
        # Inner NavigableString Object
        title_value = title.string
 
        # Title as a string value
        title_string = title_value.strip()
 
    except AttributeError:
        title_string = ""   
 
    return title_string
 
# Function to extract Product Price
def get_price(soup):
 
    try:
        price = soup.find("span", attrs={'class':'a-size-medium a-color-price priceBlockBuyingPriceString'})
        if price is None:
            price = soup.find("span", attrs={"class":'a-size-medium a-color-price priceBlockDealPriceString'}).get_text(strip=True)
        else:
            price = price.get_text(strip=True)

    except AttributeError:
        price = ""
 
    return price
 
# Function to extract Product Rating
def get_rating(soup):
 
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
         
    except AttributeError:
         
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = "" 
 
    return rating
 
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
         
    except AttributeError:
        review_count = ""   
 
    return review_count
 
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
 
    except AttributeError:
        available = "In Stock"  
 
    return available    

# Function to extract Product description
def get_description(soup):
    try:
        description = soup.find("div", attrs={"id":'productDescription'})#.get_text(strip=True)
        description = description.find('p').get_text(strip=True)
    except AttributeError:
        description = ""

    return description

#Function to extract a Page of products
def get_all_products(soup):
    productString = ""
    try:
        product = soup.find_all("span", attrs={"class": 'celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results'},limit=10) 

        for x in range(10):
            productString += '[{}] '.format(x+1) + product[x].find("a",attrs={"class":'a-link-normal a-text-normal'}).get_text(strip=True) + "\n"
            productString += 'Link: https://www.amazon.com/' + product[x].find("a",attrs={"class":'a-link-normal a-text-normal'}).get('href') + "\n"
            try:
                productString += 'Price: '  + product[x].find("span", attrs={"class":"a-offscreen"}).get_text(strip=True) + ' '
            except:
                productString += 'Price: Not Found ' 
            try:
                productString += 'Rating: ' + product[x].find("span",attrs={"class":'a-icon-alt'}).get_text(strip=True) + ' '
            except:
                productString += 'Rating: Not Found '
            try:
                productString += 'Number of Reviews: ' + product[x].find("span", attrs={"class":'a-size-base', "dir":"auto"}).get_text(strip=True) + "\n"
            except:
                productString += 'Number of Reviews: Not Found \n'
            productString += "================================================================================================\n"

    except AttributeError:
        productString = ""
    
    return productString

if __name__ == '__main__':
 
    # Headers for request
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    
    running = True
    while running != False:
        choice = input('''1. Information On Product\n2. Information On Multiple Products \nSearch: \n''')

        if choice == '1':
            # The webpage URL
            #URL = input("Enter Product URL: ")
            #URL.strip()
            #URL = 'https://www.amazon.com/Star-Wars-Infant-Costume-Bodysuit/dp/B07QD2W6BS/ref=sr_1_1?_encoding=UTF8&c=ts&dchild=1&keywords=Kids%27%2B%26%2BBabies%27%2BCostumes%2B%26%2BAccessories&qid=1600214121&sr=8-1&ts_id=14194742011&th=1'
            URL = input("Enter Product URL: \n")
            # HTTP Request
            webpage = requests.get(URL, headers=HEADERS)
        
            # Soup Object containing all data
            soup = BeautifulSoup(webpage.content, "lxml")

        # Function calls to display all necessary product information
            print("\nProduct Title =", get_title(soup))
            print("Product Price =", get_price(soup))
            print("Product Rating =", get_rating(soup))
            print("Number of Product Reviews =", get_review_count(soup))
            print("Availability =", get_availability(soup))
            print("Description =", get_description(soup))
            print("================================================================================================\n")

        if choice == '2':
            search = input('What product do you want to search: \n')
            search = search.strip()
            search = search.split(" ")
            search = "+".join(search)
            URL = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'.format(search)

            webpage = requests.get(URL, headers=HEADERS)
        
            # Soup Object containing all data
            soup = BeautifulSoup(webpage.content, "lxml")
            print(get_all_products(soup))

        elif choice != '1' and choice != '2':
            running = False

        