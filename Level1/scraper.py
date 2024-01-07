import requests
import pandas as pd
from bs4 import BeautifulSoup

# Here i am defining The  output list which i have to store in my CSV file
Medicine_name = []
MRP = []
Discounted_Prices = []
Manufacturer_name = []
URL_of_medicine = []
salts = []
quantity = []

print("Loading start.......")

# Here i am defining how much data i want from which website

#---------------------MAIN NETMED WEBSITE SCRAPPING CODE INTRO--------------------------------------#
#Here,I am Defining the fucntion and in this fucntion,i have to click on two Urls 
#-> One for  that link whoever product start with with 'B' -> Other for that link whoever product start with F
#->We are in Disease/Problem related page-> THen will go in Medicine page->Then go in medicine product page
#---------------------MAIN NETMED WEBSITE SCRAPPING CODE Start--------------------------------------#

def scrape_netmeds_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    listOfDisease = soup.find_all("ul", class_="alpha-drug-list")

    #-----------------------------NetMeds Scrapping B Start--------------------------------------#
    # ---Write now,We are at page which have all Diseases.Ony by one ,Going in disease page,
    #--we will select that disease medicine which starts with 'B'
    print("NetMeds Scrapping B Start")
    count = 0
    nlb = 900
    for ul in listOfDisease:
        links = ul.find_all("a")
        if count == nlb:
            break

        for link in links:

            if count == nlb:
                break

            href = link.get("href")
            new_disease_page_url = href
            new_r = requests.get(new_disease_page_url)

            new_soup = BeautifulSoup(new_r.text, "lxml")
            listOfMedicines = new_soup.find_all("li", class_="product-item")

            for medicine in listOfMedicines:
                #--We are now in Medicine page which is having all of product with links
                if count == nlb:
                    break

                product_links = medicine.find_all("a")
                #this above product_link is the list having the link of all product in the medicine page (All alphabets are there)
                #We are going in each link one by one

                for product_link in product_links:
                    #--Extracting Product NAME and its LINK----#---#---#---#---#
                    product_name = product_link.text.strip()
                    product_link_href = product_link.get("href")
                    
                    if product_name and (product_name[0].upper() == 'B'):                               #if and only if ,Product name is starting with B,then we will continue further
                        product_page_href_link = product_link_href

                        #--Now this product_page_href_link is product page link and
                        #--after clicking this,We will reach product page

                        product_page_r = requests.get(product_page_href_link)
                        product_page_soup = BeautifulSoup(product_page_r.text, "lxml")

                        #Now we have reached at product page
                        #########Extracting NAME ########
                        name = product_page_soup.find("h1", class_="black-txt")

                        #########Extracting Discounted price ########
                        DiscountedPrice = product_page_soup.find("span", class_="final-price")

                        #########Extracting Before Discount price ########
                        BeforeDiscount = product_page_soup.find("span", class_="price")

                        #########Extracting Manufacturer Details ########
                        Manufacturer = product_page_soup.find("span", class_="drug-manu")

                        #########Extracting How much to quantity is there ########
                        how_much_take = product_page_soup.find("span", class_="drug-varient")

                        #########Extracting Salt Scrapping ########
                        product_desc_info = product_page_soup.find("div",class_="product_desc_info")
                        if product_desc_info:
                            manufacturer__name_value = product_desc_info.find_all("div",class_="manufacturer__name_value")
                            if(manufacturer__name_value and len(manufacturer__name_value)>2):
                                salts.append(manufacturer__name_value[2].text)
                            else:
                                salts.append("N/A")
                        else:
                            salts.append("N/A")

                        #########Taking PRODUCT LINK  ########
                        UrlOfPageProduct = product_page_href_link


                        ## Now we are checking whether we scrapped exists or not,if not then we
                        # have to insert N/A in list otherwise we will put value
                        ## append function we use to insert data in our answer list

                        if (how_much_take):
                            quantity.append(how_much_take.text)
                        else:
                            quantity.append("N/A")

                        if name:
                            print(f'{"NetMed starting with B"} {count}')
                            Medicine_name.append(name.text.strip())
                        else:
                            Medicine_name.append("N/A")

                        if DiscountedPrice:
                            Selling_price = DiscountedPrice.text.strip()
                            if Selling_price[0] == 'M':
                                Selling_price = Selling_price[3:len(Selling_price)]

                            Selling_price.strip()
                            Discounted_Prices.append(Selling_price)
                        else:
                            Discounted_Prices.append("N/A")

                        if BeforeDiscount:
                            MRP_PRice_of_product = BeforeDiscount.find_all("strike")
                            for strike_element in MRP_PRice_of_product:
                                MRP.append(strike_element.text)
                        else:
                            MRP.append("N/A")

                        Manufacturer_company = Manufacturer.find("a")
                        if Manufacturer_company:
                            Manufacturer_name.append(Manufacturer_company.text.strip())
                        else:
                            Manufacturer_name.append("N/A")

                        URL_of_medicine.append(UrlOfPageProduct)
                        count += 1
    #-----------------------------NetMeds Scrapping B ENDS--------------------------------------#



    #-----------------------------NetMeds Scrapping F Start--------------------------------------#
    #-------------------------with similar logic of scrapping B,We will scrap product starting with F----#


    print("NetMeds starting with F starts")
    count = 0
    nlf = 1000
    for ul in listOfDisease:
        links = ul.find_all("a")
        if count == nlf:
            break

        for link in links:
            if count == nlf:
                break

            href = link.get("href")
            new_disease_page_url = href
            new_r = requests.get(new_disease_page_url)

            new_soup = BeautifulSoup(new_r.text, "lxml")
            listOfMedicines = new_soup.find_all("li", class_="product-item")

            for medicine in listOfMedicines:
                if count == nlf:
                    break

                product_links = medicine.find_all("a")
                for product_link in product_links:

                    product_link_href = product_link.get("href")
                    product_name = product_link.text.strip()

                    ####Here at this point we are checking if this is 'F' #######
                    if product_name and (product_name[0].upper() == 'F'):

                        product_page_href_link = product_link_href
                        product_page_r = requests.get(product_page_href_link)

                        product_page_soup = BeautifulSoup(product_page_r.text, "lxml")

                        #########Extracting NAME ########
                        name = product_page_soup.find("h1", class_="black-txt")

                        #########Extracting Discounted price ########
                        DiscountedPrice = product_page_soup.find("span", class_="final-price")

                        #########Extracting Before Discount price ########
                        BeforeDiscount = product_page_soup.find("span", class_="price")

                        #########Extracting Manufacturer Details ########
                        Manufacturer = product_page_soup.find("span", class_="drug-manu")

                        #########Extracting How much to quantity is there ########
                        how_much_take = product_page_soup.find("span", class_="drug-varient")

                        #########Extracting Salt Scrapping ########
                        product_desc_info = product_page_soup.find("div",class_="product_desc_info")
                        if product_desc_info:
                            manufacturer__name_value = product_desc_info.find_all("div",class_="manufacturer__name_value")
                            if(manufacturer__name_value and len(manufacturer__name_value)>2):
                                salts.append(manufacturer__name_value[2].text)                      
                            else:
                                salts.append("N/A")                      
                        else: 
                            salts.append("N/A")

                        #########Taking PRODUCT LINK  ########
                        UrlOfPageProduct = product_page_href_link

                        ## Now we are checking whether we scrapped exists or not,if not then we
                        # have to insert N/A in list otherwise we will put value
                        ## append function we use to insert data in our answer list

                        if (how_much_take):
                            quantity.append(how_much_take.text)
                        else:
                            quantity.append("N/A")


                        if name:
                            print(f'{"NetMed starting with F"} {count}')
                            Medicine_name.append(name.text.strip())
                        else:
                            Medicine_name.append("N/A")

                        if DiscountedPrice:
                            Selling_price = DiscountedPrice.text.strip()

                            if Selling_price[0] == 'M':
                                Selling_price = Selling_price[3:len(Selling_price)]

                            Selling_price.strip()
                            Discounted_Prices.append(Selling_price)
                        else:
                            Discounted_Prices.append("N/A")

                        if BeforeDiscount:
                            MRP_PRice_of_product = BeforeDiscount.find_all("strike")
                            for strike_element in MRP_PRice_of_product:
                                MRP.append(strike_element.text)
                        else:
                            MRP.append("N/A")

                        Manufacturer_company = Manufacturer.find("a")
                        if Manufacturer_company:
                            Manufacturer_name.append(Manufacturer_company.text.strip())
                        else:
                            Manufacturer_name.append("N/A")

                        URL_of_medicine.append(UrlOfPageProduct)
                        count += 1
    #-----------------------------NetMeds Scrapping F ENDS--------------------------------------#


    return Medicine_name, MRP, Discounted_Prices, Manufacturer_name, salts, URL_of_medicine, quantity

#---------------------MAIN NETMED WEBSITE SCRAPPING CODE ENDS HERE--------------------------------------#





#---------------------MAIN PharmaEasy WEBSITE SCRAPPING CODE INTRO--------------------------------------#
#Here,I am Defining the fucntion and in this fucntion,i have to click on two Urls
#-> One for  that link whoever product start with with 'B' -> Other for that link whoever product start with F
#---------------------MAIN PharmaEasy WEBSITE SCRAPPING CODE Start--------------------------------------#
def scrape_pharmeasy_data(url):

    #-----------------------------PharmaEasy Scrapping B Starts--------------------------------------#
    # we are adding b in that part of url which is responsible for opening link of product starting with alphabet B
    url1 = url[0:59] + 'b' + url[60:len(url)]

    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "lxml")

    count = 0
    plb = 100
    #in this,a page has only some Medicines ,thats why we have to keep a counter of pageNumber and
    #when we dont extracting the page 1 ,then we have to go on page 2
    pageNUmber = 1
    while count<plb:

        nextPageButton = soup.find("span", class_="PageIndex_hover__I_gmH")

        #This below line now determining the link with correct page number
        nextPageLinkWithSameAlphabet = url1[0:len(url1)-1] + str(pageNUmber)

        pageNUmber += 1
        print(nextPageLinkWithSameAlphabet)
        r = requests.get(nextPageLinkWithSameAlphabet)
        soup = BeautifulSoup(r.text, "lxml")
        # now this above soup have the content of current page

        # Now we will make a list and store all Medicine products
        listOfMedicines_start_with_alphabet = soup.find_all("div", class_="BrowseList_medicineContainer__Fi9u7")

        # Now one by one,We will go through each medicine products
        for i in listOfMedicines_start_with_alphabet:
            if count == plb:
                break

            #This will will find all links in single medicine product div
            links = i.find_all("a")
            for link in links:
                if count == plb:
                    break
                # Getting the link of  individual product
                Product_link_starting_with_B = "https://pharmeasy.in/" + link.get("href")

                product_page_r = requests.get(Product_link_starting_with_B)

                product_page_soup = BeautifulSoup(product_page_r.text, "lxml")
                # Now this above soup has contents of product page link

                # Extract information from the product page

                #########Extracting NAME ########
                name = product_page_soup.find("h1", class_="MedicineOverviewSection_medicineName__dHDQi")

                #########Extracting Discounted price ########
                DiscountedPrice = product_page_soup.find("div", class_="PriceInfo_gcdDiscountContainer__hr0YD")

                #########Extracting Before Discount price ########
                BeforeDiscount = product_page_soup.find("span", class_="PriceInfo_striked__Hk2U_")

                #########Extracting Manufacturer Details ########
                Manufacturer = product_page_soup.find("div", class_="MedicineOverviewSection_brandName__rJFzE")

                #########Extracting How much to quantity is there ########
                how_much_take = product_page_soup.find("div", class_="MedicineOverviewSection_measurementUnit__7m5C3")

                #########Taking PRODUCT LINK  ########
                URL_of_medicine.append(Product_link_starting_with_B)

                #########Extracting Salt Scrapping ########
                ingredients = product_page_soup.find_all("td", class_="DescriptionTable_value__0GUMC")

                ## Now we are checking whether we scrapped exists or not,if not then we
                # have to insert N/A in list otherwise we will put value
                ## append function we use to insert data in our answer list

                if name:
                    print(f'{"Pharmeasy starting with B"} {count}')
                    Medicine_name.append(name.text.strip())
                else:
                     Medicine_name.append("N/A")

                if DiscountedPrice:
                    first_span = DiscountedPrice.find("span")
                    if first_span:
                        Discounted_Prices.append(first_span.text.strip())
                else:
                    Discounted_Prices.append("N/A")

                if BeforeDiscount:
                    MRP.append(BeforeDiscount.text.strip())
                else:
                    MRP.append("N/A")

                if Manufacturer:
                    Manufacturer_name.append(Manufacturer.text.strip())
                else:
                    Manufacturer_name.append("N/A")

                if how_much_take:
                    quantity.append(how_much_take.text.strip())
                else:
                    quantity.append("N/A")

                if ingredients:
                    salts.append(ingredients[2].text.strip())
                else:
                    salts.append("N/A")
                    
                count += 1
    #-----------------------------PharmaEasy Scrapping B ENDS--------------------------------------#



    #-----------------------------PharmaEasy Scrapping F BEGINS--------------------------------------#
    #-----------------------------Similarly like of b,We can do of f--------------------------------------#
    url2 = url[0:59] + 'f' + url[60:len(url)]
    r = requests.get(url2)

    soup = BeautifulSoup(r.text, "lxml")
    count = 0
    pageNUmber = 1
    plf = 0
    while count<plf:
        nextPageButton = soup.find("span", class_="PageIndex_hover__I_gmH")
        nextPageLinkWithSameAlphabet = url2[0:len(url1)-1] + str(pageNUmber)
        pageNUmber += 1
        r = requests.get(nextPageLinkWithSameAlphabet)
        soup = BeautifulSoup(r.text, "lxml")
        listOfMedicines_start_with_alphabet = soup.find_all("div", class_="BrowseList_medicineContainer__Fi9u7")
        # Loop through each medicine
        for i in listOfMedicines_start_with_alphabet:
            if count == plf:
                break
            links = i.find_all("a")
            for link in links:
                if count == plf:
                    break
                # Get the link for the individual product
                Product_link_starting_with_F = "https://pharmeasy.in/" + link.get("href")

                # Request to get the HTML content of the product page
                product_page_r = requests.get(Product_link_starting_with_F)

                product_page_soup = BeautifulSoup(product_page_r.text, "lxml")

                #########Extracting NAME ########
                name = product_page_soup.find("h1", class_="MedicineOverviewSection_medicineName__dHDQi")

                #########Extracting Discounted price ########
                DiscountedPrice = product_page_soup.find("div", class_="PriceInfo_gcdDiscountContainer__hr0YD")

                #########Extracting Before Discount price ########
                BeforeDiscount = product_page_soup.find("span", class_="PriceInfo_striked__Hk2U_")

                #########Extracting Manufacturer Details ########
                Manufacturer = product_page_soup.find("div", class_="MedicineOverviewSection_brandName__rJFzE")

                #########Extracting How much to quantity is there ########
                how_much_take = product_page_soup.find("div", class_="MedicineOverviewSection_measurementUnit__7m5C3")

                #########Taking PRODUCT LINK  ########
                URL_of_medicine.append(Product_link_starting_with_F)

                #########Extracting Salt Scrapping ########
                ingredients = product_page_soup.find_all("td", class_="DescriptionTable_value__0GUMC")

                ## Now we are checking whether it (we just scrapped) exists or not,if not then we
                # have to insert N/A in list otherwise we will put value
                ## append function we use to insert data in our answer list

                if name:
                    print(f'{"Pharmeasy starting with F"} {count}')
                    Medicine_name.append(name.text.strip())
                else:
                     Medicine_name.append("N/A")

                if DiscountedPrice:
                    first_span = DiscountedPrice.find("span")
                    if first_span:
                        Discounted_Prices.append(first_span.text.strip())
                else:
                    Discounted_Prices.append("N/A")

                if BeforeDiscount:
                    MRP.append(BeforeDiscount.text.strip())
                else:
                    MRP.append("N/A")

                if Manufacturer:
                    Manufacturer_name.append(Manufacturer.text.strip())
                else:
                    Manufacturer_name.append("N/A")

                if how_much_take:
                    quantity.append(how_much_take.text.strip())
                else:
                    quantity.append("N/A")

                if ingredients:
                    salts.append(ingredients[2].text.strip())
                else:
                    salts.append("N/A")
                    
                count += 1
    #-----------------------------PharmaEasy Scrapping F ENDS--------------------------------------#


    return Medicine_name, MRP, Discounted_Prices, Manufacturer_name, salts, URL_of_medicine

##########################---MAIN PHARMAEASYWEBSITE SCRAPPING CODE ENDS HERE--###########################



# Here ,we are taking url of netmeds and Pharmaeasy

net_med_URL = "https://www.netmeds.com/prescriptions"
scrape_netmeds_data(net_med_URL)
pharma_easy_URL = "https://pharmeasy.in/online-medicine-order/browse?alphabet=a&page=0"
scrape_pharmeasy_data(pharma_easy_URL)


df = pd.DataFrame({"Medicine_Name": Medicine_name, "Discounted_Prices": Discounted_Prices,"Real_Price:": MRP, "Manufacturer Name": Manufacturer_name,"Medicine_Link:": URL_of_medicine,"quantity":quantity,"salts":salts})

#Here i am creating dataframe to CSV
df.to_csv("FInalAbhinavfinalYes.csv")
print("Program end.......")

