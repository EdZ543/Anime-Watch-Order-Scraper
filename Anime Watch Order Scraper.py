from bs4 import BeautifulSoup
import requests.certs
from termcolor import colored
import time

mal_query_base = "https://myanimelist.net/search/all?q="
mal_result_base = "https://myanimelist.net/anime/"
chiaki_result_base = "https://chiaki.site/?/tools/watch_order/id/"

watch_order_format_options = [
    "name",
    "name and link",
    "hyperlink"
]

watch_order_format_choice = "name and link"


def scrape_mal_search_results(search_term):
    search_results = []
    source_link = mal_query_base + search_term
    source = requests.get(source_link).text
    time.sleep(0.1)
    soup = BeautifulSoup(source, "lxml")
    rows = soup.find_all("div", class_="information di-tc va-t pt4 pl8")

    for row in rows:
        name = row.a.text
        link = row.a["href"]
        result = [name, link]
        search_results.append(result)

    return search_results


def mal_to_chiaki(mal_link):
    mal_id = mal_link.replace(mal_result_base, "").split("/")[0]
    chiaki_link = chiaki_result_base + mal_id

    return chiaki_link


def scrape_chiaki_watch_order(chiaki_link):
    watch_order = []
    source = requests.get(chiaki_link).text
    time.sleep(0.1)
    soup = BeautifulSoup(source, "lxml")
    rows = soup.find_all("td")

    for row in rows:
        name = row.find("span", class_="wo_title")
        link = row.a

        if name != None and link != None:
            anime = [name.text, link["href"]]
            watch_order.append(anime)

    return watch_order


def scrape_series_name(chiaki_link):
    source = requests.get(chiaki_link).text
    time.sleep(0.1)
    soup = BeautifulSoup(source, "lxml")
    header = soup.h2.text
    series_name = header.split(" Watch Order")[0]

    return series_name


print("Yo welcome to the world's epicest Anime Watch Order Scraper")

main_loop = True
while main_loop:
    search_term = input(colored("\nEnter your desired anime series: ", "yellow"))

    if len(search_term) < 3:
        print(colored("No results, search term was too short", "red"))
        continue

    mal_search_results = scrape_mal_search_results(search_term)

    print(f"\nAight, here's the top {len(mal_search_results)} search results from MyAnimeList:\n")

    for mal_search_result_index in range(len(mal_search_results)):
        index = str(mal_search_result_index + 1) + ":"
        name = mal_search_results[mal_search_result_index][0]
        link = mal_search_results[mal_search_result_index][1].rsplit("/", 1)[0]

        print(f"{index.ljust(4)}{name}", end="")
        print(colored(f" ({link})", "blue"))

    print("0: ", "My anime isn't here\n")

    anime_choice = ""

    while True:
        mal_search_result_choice = input(colored("Enter your choice: ", "yellow"))
        
        try:
            if mal_search_result_choice == "0":
                anime_choice = mal_search_result_choice
                break
            else:
                anime_choice = mal_search_results[int(mal_search_result_choice) - 1]
                break

        except:
            print(colored("Invalid choice", "red"))

    if anime_choice == "0":
        print("Aight, try another search")
        continue

    chiaki_link = mal_to_chiaki(anime_choice[1])
    chiaki_watch_order = scrape_chiaki_watch_order(chiaki_link)
    series_name = scrape_series_name(chiaki_link)

    print(f"\n{series_name}'s watch order:\n")

    if watch_order_format_choice == watch_order_format_options[0]:
        for anime in chiaki_watch_order:
            print(anime[0])
    elif watch_order_format_choice == watch_order_format_options[1]:
        for anime in chiaki_watch_order:
            print(anime[0], end="")
            print(colored(f" ({anime[1]})", "blue"))
    elif watch_order_format_choice == watch_order_format_options[2]:
        for anime in chiaki_watch_order:
            print(f"[{anime[0]}]", end="")
            print(colored(f"({anime[1]})", "blue"))
    else:
        print(colored("Invalid watch order format option!", "red"))

    while True:
        again_choice = input(colored("\nSearch for another anime? (y/n) ", "yellow"))

        if again_choice == "y":
            print("Aight lets run it again")
            break
        elif again_choice == "n":
            print("Aight peace")
            main_loop = False
            break
        else:
            print(colored("Invalid choice", "red"))