from bs4 import BeautifulSoup
import pip._vendor.requests as requests
import pip._vendor.urllib3 as urllib3  # Used for exception handling in searchBing()
from PIL import Image
from io import BytesIO
import os
import sys  # Used for exception handling in searchBing()
import ssl  # Used for exception handling in searchBing()
import socket  # Used for exception handling in searchBing()
import logging

logger = logging.Logger('catch_all')

def printErrorMessage(img_title, error):
    print("ERROR:", img_title, "could not be saved,", str(error))


def searchBing():
    search = input("Search for: ")
    params = {"q": search}
    if search == "quit":
        sys.exit()
    else:
        r = requests.get("http://bing.com/images/search", params=params)

        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.findAll("a", {"class": "thumb"})
        renamed_image_index = 1
        dir_name = search.replace(" ", "_").lower()
        # if not os.path.exists('./' + search):
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        print("links length:", str(len(links)))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
              "~~~")
        for item in links:
            print("****************************************************************************************************"
                  "*******")

            try:
                item_href = item.attrs["href"]
                img_obj = requests.get(item_href)
                title = item_href.split("/")[-1]
                print("    ", title)
                image = Image.open(BytesIO(img_obj.content))
                print("     save folder:", search)
                print("     title:", title)
                print("     format:", image.format)
                try:
                    image.save(dir_name + "/" + title + "." + image.format)
                except:
                    image.save("./" + dir_name + "/" + dir_name + str(renamed_image_index) + "." + image.format)
                    print(title, "was renamed to", search + str(renamed_image_index))
                    renamed_image_index += 1

            except OSError as error:
                printErrorMessage(title, error)

            # Image errors
            except Image.UnidentifiedImageError as error:
                printErrorMessage(title, error)

            # ssl errors
            except ssl.SSLCertVerificationError as error:
                printErrorMessage(title, error)

            # urllib3 errors
            except urllib3.exceptions.MaxRetryError as error:
                printErrorMessage(title, error)
            except urllib3.exceptions.NewConnectionError as error:
                printErrorMessage(title, error)
            except urllib3.exceptions.ProtocolError as error:
                printErrorMessage(title, error)

            # requests errors
            except requests.exceptions.SSLError as error:
                printErrorMessage(title, error)
            except requests.exceptions.ConnectionError as error:
                printErrorMessage(title, error)

            # socket errors
            except socket.gaierror as error:
                printErrorMessage(title, error)

        print("***********************************************************************************************************")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        searchBing()


searchBing()



