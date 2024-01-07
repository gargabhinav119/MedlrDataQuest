import requests
from bs4 import BeautifulSoup
import pandas as pd

#Now first,I am creating the list in which i will store all 10 URL informtation

Name_of_lab = []
MRP_Test = []
DiscountSellingPrice = []
Testing_iNcluded_list = []
AddressList = []


#Now this is the function for lab_Scrapper

def lab_scraper(url):
    #write the code to scrape the lab data here


    lab_name = "N/A"
    mrp = "N/A"
    discounted_price = "N/A"
    tests_included = ""
    address = "N/A"

    r = requests.get(url)
    soup = BeautifulSoup(r.text,"lxml")
    
    #Extracting Lab Name
    lab_name_element  = soup.find("h3",class_="common_main")
    if lab_name_element:
            # Get the text content of the lab name
        lab_name = lab_name_element.contents[0].strip()
        Name_of_lab.append(lab_name)
        # print(lab_name)
    else:
         Name_of_lab.append("n/a")

    #Extracting MRP ----------------------------------
         
    MRP_element  = soup.find("h5",class_="crossedd")
    if MRP_element:
            # Get the text content of the lab name
        mrp = MRP_element.text.strip()
        MRP_Test.append(mrp)
        # print(MRP)
    else:
         MRP_Test.append("n/a")


    #Extracting Price------------------------------- 
    Price_element  = soup.find("h5",class_="new_price")
    if Price_element:
            # Get the text content of the lab name
        discounted_price = Price_element.text.strip()
        DiscountSellingPrice.append(discounted_price)
        # print(price)
    else:
        DiscountSellingPrice.append("N/A")


    # Extracting Test Included------------------------------

    Test_included_element_list = soup.find_all("div", class_="test-title collapsed")
    if Test_included_element_list:
        for test_element in Test_included_element_list:
            test_title = test_element.contents[0].strip()
            tests_included = tests_included +(test_title) + ","
    else:
        tests_included = "No test avaialble"
        
    if tests_included[-1] == ',':
        tests_included = tests_included[:-1]
    Testing_iNcluded_list.append(tests_included)
                        

    #Extracting Address from the page-----------------------------
    
    contact_details_div = soup.find("div", class_="contact_details")
    if contact_details_div:
        min_contacts_divs = contact_details_div.find_all("div", class_="min_contacts")
        if len(min_contacts_divs) >= 2:  # Ensure there is at least a second div
            second_min_contacts_div = min_contacts_divs[1]
            address_p_tag = second_min_contacts_div.find("p")
            if address_p_tag:
                address = address_p_tag.text.strip()
                AddressList.append(address)
            else:
                AddressList.append("N/A")
        else:
            AddressList.append("N/A")
    else:
        AddressList.append("N/A")

    #Now i have Extract EVerything,So now Rerutning accordting to given template-----------

    return lab_name,mrp,discounted_price,tests_included,address

#Now 10 available URL for which i want-------------------


#My lab scrapper functions end above


#Now i am calling my lab Scrabble function

lab_scraper("https://www.labuncle.com/packages/good-health-package-1433")
lab_scraper("https://www.labuncle.com/packages/basic-whole-body-health-checkup-package-1543")
lab_scraper("https://www.labuncle.com/packages/health-champion-radiology-package-1677")
lab_scraper("https://www.labuncle.com/packages/good-health-package-with-vitamins-1434")
lab_scraper("https://www.labuncle.com/packages/full-body-health-checkup-package-1656")
lab_scraper("https://www.labuncle.com/packages/health-champion-radiology-package-1677")
lab_scraper("https://www.labuncle.com/packages/whole-body-health-checkup-package-1657")
lab_scraper("https://www.labuncle.com/packages/good-health-package-1433")
lab_scraper("https://www.labuncle.com/packages/comprehensive-full-body-radiology-package-1679")
lab_scraper("https://www.labuncle.com/packages/whole-body-radiology-package-1678")


#Here i am making dataframe using library panda

df = pd.DataFrame({"lab_name":Name_of_lab,"mrp":MRP_Test,"discounted_price":DiscountSellingPrice,"Test includes":Testing_iNcluded_list,"address":AddressList })

df.index = range(1, len(df) + 1)  # Starting index from 1
print(df)

#Here I am creating df to CSV file
df.to_csv("LabuncleFInalFInal.csv", index_label="Serial Number")


print("File done")