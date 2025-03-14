import requests
from bs4 import BeautifulSoup
from process import launch_script

BASE_LINK = "https://serial.kukaj.fi/"
BASE_LINK_2 = "https://film.kukaj.fi/"


def option():
    while True:
        decision = input("Choose series or movies s/m ")
        if decision == "s":
            return "s"

        elif decision == "m":
            return "m"


def main_movie():

    movie_name = input("Enter a movie name: ")
    movie_name = movie_name.lower()
    movie_name = movie_name.replace(" ", "-")

    # tries making request to BASE_LINK_2

    new_request_url = BASE_LINK_2 + movie_name

    # checks if http request was successful or not (200 means yes)

    if (requests.get(new_request_url)).status_code == 200:
        launch_script(new_request_url, movie_name)


def main_series():

    name = input("Zadaj meno série: ")
    name = name.lower()
    if " " in name:
        name = name.split(" ")
        name = "-".join(name)
    request_link = BASE_LINK + name

    # checking if http request was successful

    if (content := requests.get(request_link)).status_code == 200:

        print(f"Found result in {request_link}")

        soup = BeautifulSoup(content.text, "html.parser")

        # number of series is located under id "numser"

        helper_series = soup.find('div', id="numser")

        # we parse it once again to retrieve number of series for convenience

        soup = BeautifulSoup(helper_series.text, "html.parser")

        number_of_series = soup.text.split()[2]

    else:
        print("Invalid name")
        return

    print(f"Počet sérí {name} : {number_of_series}")

    string = ""

    while True:
        try:
            seria = int(input("Zadaj sériu: "))
            episode = int(input("Zadaj epizódu: "))
            if int(number_of_series) >= seria > 0:
                break

        except ValueError:
            print("Zadaj validné celé číslo")

    # adjusts the url based on given number of season and number of episode

    if seria // 10 == 0:
        string += "S" + "0" + str(seria)
    else:
        string += "S" + str(seria)

    if episode // 10 == 0:
        string += "E" + "0" + str(episode)
    else:
        string += "E" + str(episode)

    request_link += "/" + string

    question = input("Do you want to proceed? y/n")
    print(name + string)
    if question == "y":
        print(request_link)
        launch_script(request_link, name + "_" + string)


def main():
    res = option()
    if res == "m":
        main_movie()

    else:
        main_series()


if __name__ == "__main__":
    main()
