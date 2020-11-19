from bs4 import BeautifulSoup
import pip._vendor.requests as requests
import urllib.request as urlrequests
from PIL import Image
from io import BytesIO
import os

search = input("Hit Enter-Key to begin")
r = requests.get("https://www.atptour.com/en/rankings/singles")

soup = BeautifulSoup(r.text, "html.parser")
player_flags = soup.findAll("div", {"class": "country-item"})
rank_dates = soup.find("ul", {"data-value": "rankDate"})
# flag_div_list = []
html_page_list = []
opening_html_tags = "<html><body><p>"
closing_html_tags = "</p></body></html>"
flag_data = {}
flag_svg = {}
flag_count = 0

# old_dates = rank_dates.findAll("li", {"class": ""})
# current_date = rank_dates.find("li", {"class": "dropdown-default-label"})
# date_params = {"rankDate": old_dates[0]["data-value"]}
# old_date_r = requests.get("https://www.atptour.com/en/rankings/singles", params=date_params)
# print("Status:", old_date_r.status_code)
# old_soup = BeautifulSoup(old_date_r.text, "html.parser")
# if not os.path.exists('./date_pages'):
#     os.makedirs('./date_pages')
# for dates in old_dates:
#     date_str = dates["data-value"]
#     date_params = {"rankDate": date_str}
#     old_date_r = requests.get("https://www.atptour.com/en/rankings/singles", params=date_params)
#     old_soup = BeautifulSoup(old_date_r.text, "html.parser")
#     date_page = open('./date_pages/' + date_str + ".html", "w+")
#     date_page.write(opening_html_tags +
#                     date_str +
#                     closing_html_tags)

for flag in player_flags:

    flag_img = flag.find("img")
    img_url = "https://www.atptour.com"

    img_name = flag_img["alt"]
    flag_keys = flag_data.keys()
    flag_values = flag_data.values()

    if img_name in flag_data:
        flag_data[img_name] += 1
    else:
        flag_data[img_name] = 1
        img_url += flag_img["src"]
        flag_svg[img_name] = img_url
        flag_count += 1

print(flag_data.items())
i = 0
top_countries = []
for country in flag_data:
    print(top_countries)
    print(country, flag_data[country])
    if len(top_countries) < 1:
        top_countries.append(country)
    else:
        rank = 0
        inserted = False
        for top_country in top_countries:
            if flag_data[top_country] < flag_data[country]:
                top_countries.insert(rank, country)
                inserted = True
                print(country, "inserted.")
                print("top_country length:", str(len(top_countries)))
                break
            else:
                rank += 1
        if len(top_countries) < 10 and not inserted:
            top_countries.append(country)
        elif len(top_countries) > 10:
            print("remove", top_countries.pop())
print(top_countries)
for country in top_countries:
    print(flag_data[country])

# Open top ten html file
top_ten_html = open("./toptentenniscountries.html", "r+")
top_ten_soup = BeautifulSoup(top_ten_html.read(), "html.parser")
top_ten_html.close()
top_ten_items = top_ten_soup.findAll("li", {"class": "rankedCountry"})
print("top ten items", top_ten_items)
countryIndex = 0
for item in top_ten_items:
    current_country = top_countries[countryIndex]
    img_tag = top_ten_soup.new_tag("img")
    img_tag['src'] = flag_svg[current_country]
    item.string = current_country + ": " + str(flag_data[current_country])
    item.insert(0, img_tag)
    print(str(item))
    countryIndex += 1

print("output:", top_ten_soup.prettify())
top_ten_html = open("./toptentenniscountries.html", "w+")
top_ten_html.write(top_ten_soup.prettify())

#
# i = 0
# opening_html_tags = "<html><body><p>"
# closing_html_tags = "</p></body></html>"
# if not os.path.exists('./flag_pages'):
#     os.makedirs('./flag_pages')
# for country, quantity in flag_data.items():
#
#     country_page = open("./flag_pages/" + country + ".html", "w+")
#     print(country, quantity)
#     print(flag_url_list[i])
#     country_page.write(opening_html_tags +
#                        "<img src=" + flag_url_list[i] + ">" +
#                        "<p>" + str(quantity) + "</p>" +
#                        closing_html_tags)
#     i += 1

