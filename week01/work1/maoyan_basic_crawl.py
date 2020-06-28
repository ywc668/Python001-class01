import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"

cookie = 'uuid_n_v=v1; uuid=9EB2A080B96A11EA9F28E30FF5FFF73CB5154A84C7A94D1DAB10BB8C2D31FEB8; _csrf=448d5750ef63e51bf723695e9008d2c176352dad7c0fc460f422f517baa014ba; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593367820; _lxsdk_cuid=172fc1f7724c8-098b7ae06bfb5b-39647b09-1fa400-172fc1f7724c8; _lxsdk=9EB2A080B96A11EA9F28E30FF5FFF73CB5154A84C7A94D1DAB10BB8C2D31FEB8; mojo-uuid=005c478c1b1c76a729dcde705c8ea14b; mojo-session-id={"id":"33fcf00cb6e0c74dadf0ddceac0e89e9","time":1593367822261}; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593368401; __mta=147693064.1593367823108.1593367932163.1593368402062.4; mojo-trace-id=7; _lxsdk_s=172fc1f7726-930-11a-a4c%7C%7C10'

header = {"user-agent": user_agent, "Cookie": cookie}

myurl = "https://maoyan.com/films?showType=3"

response = requests.get(myurl, headers=header)

bs_info = bs(response.text, "html.parser")

movies_info_list = []
get_first_10_counter = 0

for movie_info in bs_info.find_all("div", attrs={"class": "movie-hover-info"}):
    if get_first_10_counter >= 10:
        break
    movie_info_dict = {}
    for info_tags in movie_info.find_all("div", attrs={"class": "movie-hover-title"}):
        if "title" not in movie_info_dict:
            movie_info_dict["title"] = info_tags.get("title")
        if info_tags.find("span").text == "类型:":
            movie_info_dict["category"] = info_tags.text.replace(info_tags.find("span").text, "").strip()
        elif info_tags.find("span").text == "上映时间:":
            movie_info_dict["release"] = info_tags.text.replace(info_tags.find("span").text, "").strip()
    movies_info_list.append(movie_info_dict)
    get_first_10_counter += 1


movies = pd.DataFrame(data = movies_info_list)
movies.to_csv('./movies.csv', encoding='utf8', index=False, header=False)
