from random import randint
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import string

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 "
                  "Safari/537.36",
    "Accept": "*/*"}
HOST = "https://wallpaperscraft.ru"


def get_content_on_pages(pages_count, link):
    random_page = randint(1, pages_count)
    html = get_html(f"{link}/page{random_page}")
    picture_link = get_picture_link(html.text)
    return get_hq_picture(picture_link)


def get_hq_picture(picture_link):
    html = get_html(picture_link).text
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="wallpaper__image")["src"]
    return image


def get_picture_link(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="wallpapers__item")
    pictures_link = []
    for item in items:
        pictures_link.append(item.find("a", class_="wallpapers__link")['href'])
    random_picture_link = HOST + pictures_link[randint(1, len(pictures_link))]
    return random_picture_link


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("li", class_="pager__item")
    last_page_link = HOST + pagination[-1].find("a")["href"]
    last_page = get_html(last_page_link).text
    soup = BeautifulSoup(last_page, "html.parser")
    pages_count = soup.find_all("span", class_="pager__link")[0].get_text()
    return int(pages_count)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def parse(link):
    html = get_html(link)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        return get_content_on_pages(pages_count, link)
    else:
        print("error")


class Parser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="categories")
    async def categories(self, ctx):
        html = get_html(HOST)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            ul = soup.find("ul", class_="filters__list")
            list_a = ul.find_all("a")
            names = []
            for a in list_a:
                names.append(a.text)
            for i in range(len(names)):
                names[i] = names[i].replace(" ", '')
                names[i] = names[i].replace("\n", '')
                names[i] = names[i].rstrip(string.digits)
            for i in range(len(names)):
                names[i] = f"{i + 1}. {names[i]}"
            await ctx.send("\n".join(names))

    @commands.command(name="parsing")
    async def parser(self, ctx, category_number: int):
        html = get_html("https://wallpaperscraft.ru/all/1920x1080")
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            ul = soup.find("ul", class_="filters__list")
            list_a = ul.find_all("a")
            links = []
            for a in list_a:
                links.append(HOST + a.get("href"))
            for number, link in enumerate(links, 1):
                if number == category_number:
                    await ctx.send(parse(link))


def setup(bot):
    bot.add_cog(Parser(bot))
    print("cog setup работает")
