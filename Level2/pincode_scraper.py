# I made 3 functions in this code
# One is for "finding city from pincode"
# second is for "showing scrapped data in a new window"
# third (MAIN CODE) is actually "the code of scrapping the data from website"  (Line number 83)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
import requests
import json

#I am using Selenium and chrome webDriver to open chrome and for doing operations
#Because tataMg1 take input as city name so first I am
#extracting City from pincode using an API of posalpincode
def extractCityfromPincode(pincode):
        ENDPOINT = "https://api.postalpincode.in/pincode/"
        city = ""
        response = requests.get(ENDPOINT + pincode)
        pincode_information = json.loads(response.text)

        print("Please wait, Area 1....")

        # Assuming 'PostOffice' is a key in the response
        if pincode_information and 'PostOffice' in pincode_information[0]:
            necessary_information = pincode_information[0]['PostOffice'][0]

            # Extract the 'Block' information
            block = necessary_information.get('Block', 'N/A')

            city =  block
        else:
            city = "N/A"
        return city
#Now this is the code of finidng city from pincode

#--------------------------------Just adding a pop up window to show Scrapped data after scrapping----------------------------------------------#
# for beautification of code and process visualisation,After the scrapping
# I am also creating a window in which all the details which i scrapped
# will be shown and below is that function which will show Scrapped data in window
def show_info_window(delivery_date, price,Availability,pincode,location,url):
    # Create a new tkinter window
    info_window = tk.Tk()
    info_window.title("Delivery Information")

    # SEtting  the window size 
    screen_width = info_window.winfo_screenwidth()
    screen_height = info_window.winfo_screenheight()
    window_width = int(screen_width)
    window_height = screen_height

    # SeTting the font size of text
    font_style = ("Helvetica", 15, "bold")

    # labels creating
    delivery_label = tk.Label(info_window, text=f"Delivery Date: {delivery_date}", font=font_style)
    price_label = tk.Label(info_window, text=f"Price: {price}", font=font_style)
    AvalibilityLevel_label = tk.Label(info_window, text=f"Availibility: {Availability}", font=font_style)
    pinCodeLabel = tk.Label(info_window, text=f"Pincode: {pincode}", font=font_style)
    location_lable = tk.Label(info_window, text=f"Location: {location}", font=font_style)
    URL_label = tk.Label(info_window, text=f"URL: {url}", font=font_style)

    # Putting labels ino windows
    price_label.pack(pady=20)
    AvalibilityLevel_label.pack(pady=20)
    pinCodeLabel.pack(pady=20)
    location_lable.pack(pady=20)
    URL_label.pack(pady=20)
    delivery_label.pack(pady=20)

    # Now showing the window
    info_window.mainloop()
#------------------------------------------------------------------------------------------#


#now i am giving path of my chrome driver so that i can perform selenium operations
path = "C:/chromedriver-win64/chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s)


#--------------------------------MAIN CODE INTRO----------------------------------------------#
# here my actuall code starts of scrape_medicine_availability in which
# I am taking the input parameters of pincode,url bcs this is given in task
#--------------------------------MAIN CODE START----------------------------------------------#
def scrape_medicine_availability(pincode, url):
   
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    print("Please wait, Area 2....")

    # To remove popup
    cancel_button = driver.find_element_by_class_name("UpdateCityModal__cancel-btn___2jWwS")
    cancel_button.click()
    print("Clicked on Cancel button successfully!")
    
    #Extracting "city" using pincode and then inserting that city into Search bar for tatamg1
    city = extractCityfromPincode(pincode)
    print(city)
    box = driver.find_element_by_class_name("styles__city-input___6e65P")
    box.clear()  
    box.send_keys(city)

    # Now a dropdown list will come of entered name and we will click this
    DropDown = driver.find_element_by_class_name("styles__location-dropdown___CVd5J")
    DropDown.click()
    time.sleep(1)

    # Now,After loading page 
    delivery_date_element = driver.find_elements_by_xpath("//div[contains(@class, 'style__headerText___3sw_C')]")
    price_element = driver.find_element_by_class_name("PriceBoxPlanOption__offer-price___3v9x8")

    # Finding DElivery Date and Availability
    Availability = "Out Of Stock"
    if delivery_date_element:                                               #if deliver date element is found,that means product is in stock and delievery date can be find out
        delivery_date = delivery_date_element[0].text
        Availability = "Yes,Item is Available"
        print(f"Delivery Date: {delivery_date}")
    else:
        print("Out of stock")
        delivery_date = "N/A"

    # Finding Price
    price = price_element.text


    # Open a tkinter window with delivery date and price(Although not necessary)
    show_info_window(delivery_date, price,Availability,pincode,city,url)

    return delivery_date, pincode, url

#--------------------------------MAIN CODE ENDS----------------------------------------------#



# Here i am taking input from User
pincode = input("Enter pincode")
url = input("Enter Url")


#here i am calling the function
scrape_medicine_availability(pincode, url)


#Example of not avaialble
# pincode = "682551"
# url = "https://www.1mg.com/otc/carbamide-forte-calcium-magnesium-zinc-for-bones-joints-immunity-tablet-otc680652"

#Example of  avaialble
# pincode = "147002"
# url = "https://www.1mg.com/otc/carbamide-forte-calcium-magnesium-zinc-for-bones-joints-immunity-tablet-otc680652"
