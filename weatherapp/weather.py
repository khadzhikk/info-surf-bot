import requests
from bs4 import BeautifulSoup
import config


weather_context = False

def weather_parse(city):
    url = f"https://world-weather.ru/pogoda/russia/{city}/" 
    resp = requests.get(url, headers=config.headers)
    # print(resp.text)
    bs = BeautifulSoup(resp.text, "lxml")

    td_day = bs.find_all("td", class_="weather-day")
    td_temp = bs.find_all("td", class_="weather-temperature")
    res_str = "" 

    if td_day == None or len(td_day) < 4:
        return None
    
    for i in range(4):
        res_str += td_day[i].text + "  " + td_temp[i].text + '\n'
        
    res_str += "\n\n"

    blocks = bs.find_all("li", class_="tab-w")

    for bl in blocks:
        divs = bl.find_all("div")
        for d in divs:
            res_str += d.text + ' '
        res_str += bl.find("span")["title"] + "\n\n" 

    res_str += "\nnmore  -  " + url



    return res_str



        

