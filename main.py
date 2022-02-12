import requests
from bs4 import BeautifulSoup
import json
import time

HOST = "https://spb.cian.ru/"
URL="https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=244909&offer_type=flat&room1=1&room2=1&type=4"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}
start_time = time.time()

def get_links():
    response = requests.get(
        url="https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=244909&offer_type=flat&room1=1&room2=1&type=4",
        headers=headers)
    src = response.text

    soup = BeautifulSoup(src, 'lxml')

    pages_count = int(soup.find("div", class_="_93444fe79c--wrapper--bKcEk").find_all("li")[-1].text)
    links = []

    for page in range(1, pages_count + 1):
        r = requests.get(url=f"https://spb.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=244909&offer_type=flat&p={page}&room1=1&room2=1&type=4", headers=headers)
        src = r.text
        soup = BeautifulSoup(src, "lxml")

        cards = soup.find_all('article', class_='_93444fe79c--cont--OzgVc')

        for item in cards:
            link_product = item.find('div', class_='_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy').find('a').get('href')
            links.append(link_product)
        # print(f"Обработал страницу {page}/{pages_count}")
    return links

def get_content(links):

    all_cards = []
    i = 1
    for link in links:
        r = requests.get(link, headers=headers)
        src = r.text
        soup = BeautifulSoup(src, "lxml")

        try:
            title = soup.find('h1', class_='a10a3f92e9--title--UEAG3').text
        except:
            title = "Нет названия"

        try:
            prise = soup.find('span', class_='a10a3f92e9--price_value--lqIK0').text
        except:
            prise = "Нет цены"

        try:
            address = soup.find('address', class_='a10a3f92e9--address--F06X3').text.rstrip('На карте')
        except:
            address = "Нет адреса"

        try:
            opisanie = soup.find('p', class_='a10a3f92e9--description-text--YNzWU').text
        except:
            opisanie = "Нет описания"

        try:
            image = soup.find('div', class_='a10a3f92e9--photo_gallery_container--OS_kt').find("div").find("span").find("span").get("content")
        except Exception:
            image = "Нет картинки"

        all_cards.append(
            {
                "Название": title,
                "Цена": prise.replace(" ", " "),
                "Адрес": address,
                "Описание": opisanie.replace("\n", ""),
                "Ссылка": link,
                "Картинка": image
            }
        )

        # print (f"Выполнил страницу {i}/{len(links)}")
        i += 1

    with open(f"all_cards.json", "w", encoding="utf-8") as file:
        json.dump(all_cards, file, indent=4, ensure_ascii=False)


        # print(title, prise, address)
        # print(opisanie)
        # print(image)




def main():

    links=get_links()
    get_content(links)
    # print(f"Итоговое время {time.time() - start_time}")


if __name__ == "__main__":
    main()