from bs4 import BeautifulSoup
import urllib
import os
import json

from tqdm import tqdm
from .utilities import format_filename, get_soup, get_pdf_text, create_script_dirs

def get_imsdb():
    ALL_URL = "https://imsdb.com/all-scripts.html"
    BASE_URL = "https://imsdb.com"
    SOURCE = "imsdb"
    DIR, TEMP_DIR, META_DIR = create_script_dirs(SOURCE)

    def get_script_from_url(script_url):
        text = ""

        try:

            if script_url.endswith('.pdf'):
                text = get_pdf_text(script_url, os.path.join(SOURCE, file_name))
                return text

            if script_url.endswith('.html'):
                script_soup = get_soup(
                    script_url)
                if script_soup == None:
                    return text
                if len(script_soup.find_all('td', class_="scrtext")) < 1:
                    return ""
                script_text = script_soup.find_all(
                    'td', class_="scrtext")[0].pre

                if script_text:
                    script_text = script_soup.find_all(
                        'td', class_="scrtext")[0].pre.pre
                    if script_text:
                        text = script_text.get_text()

                    else:
                        script_text = script_soup.find_all(
                            'td', class_="scrtext")[0].pre
                        text = script_text.get_text()
        except Exception as err:
            print(script_url)
            print(err)
            text = ""

        return text

    def get_script_url(movie):
        # script_page_url = movie.contents[0].get('href')
        # name = movie.contents[0].text
        # movie_name = script_page_url.split("/")[-1].strip('Script.html')

        # script_page_soup = get_soup(
        #     BASE_URL + urllib.parse.quote(script_page_url))
        # if script_page_soup == None:
        #     return "", name
        # paras = script_page_soup.find_all('p', align="center")
        # if len(paras) < 1:
        #     return "", ""
        # script_url = paras[0].contents[0].get('href')
        # print(script_url)
        name = movie
        script_url = f"/scripts/{name.replace(' ', '-')}.html"
        script_url

        return script_url, name

    files = [os.path.join(DIR, f) for f in os.listdir(DIR) if os.path.isfile(
        os.path.join(DIR, f)) and os.path.getsize(os.path.join(DIR, f)) > 3000]

    metadata = {}
    # soup = get_soup(ALL_URL)
    # movielist = soup.find_all('p')

    movielist = [item["title"] for item in data]

    # TODO: fix
    for movie in movielist:
        script_url, name = get_script_url(movie)
        print(script_url, name)
        if script_url == "":
            continue
        # if script_url.endswith('.html'):
        #     name = script_url.split("/")[-1].split('.html')[0]
        # elif script_url.endswith('.pdf'):
        #     name = script_url.split("/")[-1].split('.pdf')[0]

        script_url = BASE_URL + urllib.parse.quote(script_url)
        file_name = format_filename(name)
        metadata[name] = {
            "file_name": file_name,
            "script_url": script_url
        }

        if os.path.join(DIR, file_name + '.txt') in files:
            continue

        text = get_script_from_url(script_url)

        if text == "" or name == "":
            metadata.pop(name, None)
            continue


        with open(os.path.join(DIR, file_name + '.txt'), 'w', errors="ignore") as out:
            out.write(text)

    with open(os.path.join(META_DIR, SOURCE + ".json"), "w") as outfile: 
        json.dump(metadata, outfile, indent=4)



data =[
    {
      "id": "tt0111161",
      "rank": "1",
      "title": "The Shawshank Redemption",
      "fullTitle": "The Shawshank Redemption (1994)",
      "year": "1994",
      "image": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "9.3",
      "imDbRatingCount": "2825099"
    },
    {
      "id": "tt0068646",
      "rank": "2",
      "title": "The Godfather",
      "fullTitle": "The Godfather (1972)",
      "year": "1972",
      "image": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "9.2",
      "imDbRatingCount": "1969241"
    },
    {
      "id": "tt0468569",
      "rank": "3",
      "title": "The Dark Knight",
      "fullTitle": "The Dark Knight (2008)",
      "year": "2008",
      "image": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "9",
      "imDbRatingCount": "2806534"
    },
    {
      "id": "tt0071562",
      "rank": "4",
      "title": "The Godfather Part II",
      "fullTitle": "The Godfather Part II (1974)",
      "year": "1974",
      "image": "https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "9",
      "imDbRatingCount": "1336635"
    },
    {
      "id": "tt0050083",
      "rank": "5",
      "title": "12 Angry Men",
      "fullTitle": "12 Angry Men (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "9",
      "imDbRatingCount": "842347"
    },
    {
      "id": "tt0108052",
      "rank": "6",
      "title": "Schindler's List",
      "fullTitle": "Schindler's List (1993)",
      "year": "1993",
      "image": "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "9",
      "imDbRatingCount": "1419829"
    },
    {
      "id": "tt0167260",
      "rank": "7",
      "title": "The Lord of the Rings: The Return of the King",
      "fullTitle": "The Lord of the Rings: The Return of the King (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "9",
      "imDbRatingCount": "1934502"
    },
    {
      "id": "tt0110912",
      "rank": "8",
      "title": "Pulp Fiction",
      "fullTitle": "Pulp Fiction (1994)",
      "year": "1994",
      "image": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.9",
      "imDbRatingCount": "2166297"
    },
    {
      "id": "tt0120737",
      "rank": "9",
      "title": "The Lord of the Rings: The Fellowship of the Ring",
      "fullTitle": "The Lord of the Rings: The Fellowship of the Ring (2001)",
      "year": "2001",
      "image": "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "1961351"
    },
    {
      "id": "tt0060196",
      "rank": "10",
      "title": "The Good, the Bad and the Ugly",
      "fullTitle": "The Good, the Bad and the Ugly (1966)",
      "year": "1966",
      "image": "https://m.media-amazon.com/images/M/MV5BNjJlYmNkZGItM2NhYy00MjlmLTk5NmQtNjg1NmM2ODU4OTMwXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "795822"
    },
    {
      "id": "tt0109830",
      "rank": "11",
      "title": "Forrest Gump",
      "fullTitle": "Forrest Gump (1994)",
      "year": "1994",
      "image": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "2200879"
    },
    {
      "id": "tt0137523",
      "rank": "12",
      "title": "Fight Club",
      "fullTitle": "Fight Club (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BNDIzNDU0YzEtYzE5Ni00ZjlkLTk5ZjgtNjM3NWE4YzA3Nzk3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "2260565"
    },
    {
      "id": "tt0167261",
      "rank": "13",
      "title": "The Lord of the Rings: The Two Towers",
      "fullTitle": "The Lord of the Rings: The Two Towers (2002)",
      "year": "2002",
      "image": "https://m.media-amazon.com/images/M/MV5BZGMxZTdjZmYtMmE2Ni00ZTdkLWI5NTgtNjlmMjBiNzU2MmI5XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "1744339"
    },
    {
      "id": "tt1375666",
      "rank": "14",
      "title": "Inception",
      "fullTitle": "Inception (2010)",
      "year": "2010",
      "image": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "2491233"
    },
    {
      "id": "tt0080684",
      "rank": "15",
      "title": "Star Wars: Episode V - The Empire Strikes Back",
      "fullTitle": "Star Wars: Episode V - The Empire Strikes Back (1980)",
      "year": "1980",
      "image": "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "1353061"
    },
    {
      "id": "tt0133093",
      "rank": "16",
      "title": "The Matrix",
      "fullTitle": "The Matrix (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "2008251"
    },
    {
      "id": "tt0099685",
      "rank": "17",
      "title": "Goodfellas",
      "fullTitle": "Goodfellas (1990)",
      "year": "1990",
      "image": "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "1227599"
    },
    {
      "id": "tt0073486",
      "rank": "18",
      "title": "One Flew Over the Cuckoo's Nest",
      "fullTitle": "One Flew Over the Cuckoo's Nest (1975)",
      "year": "1975",
      "image": "https://m.media-amazon.com/images/M/MV5BZjA0OWVhOTAtYWQxNi00YzNhLWI4ZjYtNjFjZTEyYjJlNDVlL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "1051582"
    },
    {
      "id": "tt0114369",
      "rank": "19",
      "title": "Se7en",
      "fullTitle": "Se7en (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1753178"
    },
    {
      "id": "tt0038650",
      "rank": "20",
      "title": "It's a Wonderful Life",
      "fullTitle": "It's a Wonderful Life (1946)",
      "year": "1946",
      "image": "https://m.media-amazon.com/images/M/MV5BZjc4NDZhZWMtNGEzYS00ZWU2LThlM2ItNTA0YzQ0OTExMTE2XkEyXkFqcGdeQXVyNjUwMzI2NzU@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "483321"
    },
    {
      "id": "tt0047478",
      "rank": "21",
      "title": "Seven Samurai",
      "fullTitle": "Seven Samurai (1954)",
      "year": "1954",
      "image": "https://m.media-amazon.com/images/M/MV5BNTkwY2I5NWMtMjNlNi00ZThjLWI4NzQtNDI4M2I4OGM1YjAzXkEyXkFqcGdeQXVyNzYxODE3NTQ@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "360640"
    },
    {
      "id": "tt0816692",
      "rank": "22",
      "title": "Interstellar",
      "fullTitle": "Interstellar (2014)",
      "year": "2014",
      "image": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "2018873"
    },
    {
      "id": "tt0102926",
      "rank": "23",
      "title": "The Silence of the Lambs",
      "fullTitle": "The Silence of the Lambs (1991)",
      "year": "1991",
      "image": "https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1511084"
    },
    {
      "id": "tt0120815",
      "rank": "24",
      "title": "Saving Private Ryan",
      "fullTitle": "Saving Private Ryan (1998)",
      "year": "1998",
      "image": "https://m.media-amazon.com/images/M/MV5BZjhkMDM4MWItZTVjOC00ZDRhLThmYTAtM2I5NzBmNmNlMzI1XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1463749"
    },
    {
      "id": "tt0317248",
      "rank": "25",
      "title": "City of God",
      "fullTitle": "City of God (2002)",
      "year": "2002",
      "image": "https://m.media-amazon.com/images/M/MV5BMGU5OWEwZDItNmNkMC00NzZmLTk1YTctNzVhZTJjM2NlZTVmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "787338"
    },
    {
      "id": "tt0118799",
      "rank": "26",
      "title": "Life Is Beautiful",
      "fullTitle": "Life Is Beautiful (1997)",
      "year": "1997",
      "image": "https://m.media-amazon.com/images/M/MV5BYmJmM2Q4NmMtYThmNC00ZjRlLWEyZmItZTIwOTBlZDQ3NTQ1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "728674"
    },
    {
      "id": "tt0120689",
      "rank": "27",
      "title": "The Green Mile",
      "fullTitle": "The Green Mile (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1374309"
    },
    {
      "id": "tt9362722",
      "rank": "28",
      "title": "Spider-Man: Across the Spider-Verse",
      "fullTitle": "Spider-Man: Across the Spider-Verse (2023)",
      "year": "2023",
      "image": "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.7",
      "imDbRatingCount": "304222"
    },
    {
      "id": "tt0076759",
      "rank": "29",
      "title": "Star Wars: Episode IV - A New Hope",
      "fullTitle": "Star Wars: Episode IV - A New Hope (1977)",
      "year": "1977",
      "image": "https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1424067"
    },
    {
      "id": "tt0103064",
      "rank": "30",
      "title": "Terminator 2: Judgment Day",
      "fullTitle": "Terminator 2: Judgment Day (1991)",
      "year": "1991",
      "image": "https://m.media-amazon.com/images/M/MV5BMGU2NzRmZjUtOGUxYS00ZjdjLWEwZWItY2NlM2JhNjkxNTFmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "1151140"
    },
    {
      "id": "tt0088763",
      "rank": "31",
      "title": "Back to the Future",
      "fullTitle": "Back to the Future (1985)",
      "year": "1985",
      "image": "https://m.media-amazon.com/images/M/MV5BZmU0M2Y1OGUtZjIxNi00ZjBkLTg1MjgtOWIyNThiZWIwYjRiXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1276276"
    },
    {
      "id": "tt0245429",
      "rank": "32",
      "title": "Spirited Away",
      "fullTitle": "Spirited Away (2001)",
      "year": "2001",
      "image": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "820764"
    },
    {
      "id": "tt0253474",
      "rank": "33",
      "title": "The Pianist",
      "fullTitle": "The Pianist (2002)",
      "year": "2002",
      "image": "https://m.media-amazon.com/images/M/MV5BOWRiZDIxZjktMTA1NC00MDQ2LWEzMjUtMTliZmY3NjQ3ODJiXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.7246_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "888257"
    },
    {
      "id": "tt0054215",
      "rank": "34",
      "title": "Psycho",
      "fullTitle": "Psycho (1960)",
      "year": "1960",
      "image": "https://m.media-amazon.com/images/M/MV5BNTQwNDM1YzItNDAxZC00NWY2LTk0M2UtNDIwNWI5OGUyNWUxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "705521"
    },
    {
      "id": "tt6751668",
      "rank": "35",
      "title": "Parasite",
      "fullTitle": "Parasite (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "906386"
    },
    {
      "id": "tt0172495",
      "rank": "36",
      "title": "Gladiator",
      "fullTitle": "Gladiator (2000)",
      "year": "2000",
      "image": "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1579297"
    },
    {
      "id": "tt0110357",
      "rank": "37",
      "title": "The Lion King",
      "fullTitle": "The Lion King (1994)",
      "year": "1994",
      "image": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1116565"
    },
    {
      "id": "tt0110413",
      "rank": "38",
      "title": "Léon: The Professional",
      "fullTitle": "Léon: The Professional (1994)",
      "year": "1994",
      "image": "https://m.media-amazon.com/images/M/MV5BOTgyMWQ0ZWUtN2Q2MS00NmY0LWI3OWMtNjFkMzZlNDZjNTk0XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1219621"
    },
    {
      "id": "tt0120586",
      "rank": "39",
      "title": "American History X",
      "fullTitle": "American History X (1998)",
      "year": "1998",
      "image": "https://m.media-amazon.com/images/M/MV5BZTJhN2FkYWEtMGI0My00YWM4LWI2MjAtM2UwNjY4MTI2ZTQyXkEyXkFqcGdeQXVyNjc3MjQzNTI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1167158"
    },
    {
      "id": "tt0407887",
      "rank": "40",
      "title": "The Departed",
      "fullTitle": "The Departed (2006)",
      "year": "2006",
      "image": "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1393050"
    },
    {
      "id": "tt2582802",
      "rank": "41",
      "title": "Whiplash",
      "fullTitle": "Whiplash (2014)",
      "year": "2014",
      "image": "https://m.media-amazon.com/images/M/MV5BOTA5NDZlZGUtMjAxOS00YTRkLTkwYmMtYWQ0NWEwZDZiNjEzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "948288"
    },
    {
      "id": "tt0482571",
      "rank": "42",
      "title": "The Prestige",
      "fullTitle": "The Prestige (2006)",
      "year": "2006",
      "image": "https://m.media-amazon.com/images/M/MV5BMjA4NDI0MTIxNF5BMl5BanBnXkFtZTYwNTM0MzY2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1409768"
    },
    {
      "id": "tt0095327",
      "rank": "43",
      "title": "Grave of the Fireflies",
      "fullTitle": "Grave of the Fireflies (1988)",
      "year": "1988",
      "image": "https://m.media-amazon.com/images/M/MV5BZmY2NjUzNDQtNTgxNC00M2Q4LTljOWQtMjNjNDBjNWUxNmJlXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "299823"
    },
    {
      "id": "tt0114814",
      "rank": "44",
      "title": "The Usual Suspects",
      "fullTitle": "The Usual Suspects (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BYTViNjMyNmUtNDFkNC00ZDRlLThmMDUtZDU2YWE4NGI2ZjVmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1126848"
    },
    {
      "id": "tt0056058",
      "rank": "45",
      "title": "Harakiri",
      "fullTitle": "Harakiri (1962)",
      "year": "1962",
      "image": "https://m.media-amazon.com/images/M/MV5BYjBmYTQ1NjItZWU5MS00YjI0LTg2OTYtYmFkN2JkMmNiNWVkXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_Ratio0.7343_AL_.jpg",
      "crew": "",
      "imDbRating": "8.6",
      "imDbRatingCount": "65280"
    },
    {
      "id": "tt0034583",
      "rank": "46",
      "title": "Casablanca",
      "fullTitle": "Casablanca (1942)",
      "year": "1942",
      "image": "https://m.media-amazon.com/images/M/MV5BY2IzZGY2YmEtYzljNS00NTM5LTgwMzUtMzM1NjQ4NGI0OTk0XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "595958"
    },
    {
      "id": "tt1675434",
      "rank": "47",
      "title": "The Intouchables",
      "fullTitle": "The Intouchables (2011)",
      "year": "2011",
      "image": "https://m.media-amazon.com/images/M/MV5BMTYxNDA3MDQwNl5BMl5BanBnXkFtZTcwNTU4Mzc1Nw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "907619"
    },
    {
      "id": "tt0027977",
      "rank": "48",
      "title": "Modern Times",
      "fullTitle": "Modern Times (1936)",
      "year": "1936",
      "image": "https://m.media-amazon.com/images/M/MV5BYjJiZjMzYzktNjU0NS00OTkxLWEwYzItYzdhYWJjN2QzMTRlL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "254677"
    },
    {
      "id": "tt0095765",
      "rank": "49",
      "title": "Cinema Paradiso",
      "fullTitle": "Cinema Paradiso (1988)",
      "year": "1988",
      "image": "https://m.media-amazon.com/images/M/MV5BM2FhYjEyYmYtMDI1Yy00YTdlLWI2NWQtYmEzNzAxOGY1NjY2XkEyXkFqcGdeQXVyNTA3NTIyNDg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "276552"
    },
    {
      "id": "tt0064116",
      "rank": "50",
      "title": "Once Upon a Time in the West",
      "fullTitle": "Once Upon a Time in the West (1968)",
      "year": "1968",
      "image": "https://m.media-amazon.com/images/M/MV5BODQ3NDExOGYtMzI3Mi00NWRlLTkwNjAtNjc4MDgzZGJiZTA1XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "343912"
    },
    {
      "id": "tt0047396",
      "rank": "51",
      "title": "Rear Window",
      "fullTitle": "Rear Window (1954)",
      "year": "1954",
      "image": "https://m.media-amazon.com/images/M/MV5BNGUxYWM3M2MtMGM3Mi00ZmRiLWE0NGQtZjE5ODI2OTJhNTU0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "512826"
    },
    {
      "id": "tt0078748",
      "rank": "52",
      "title": "Alien",
      "fullTitle": "Alien (1979)",
      "year": "1979",
      "image": "https://m.media-amazon.com/images/M/MV5BOGQzZTBjMjQtOTVmMS00NGE5LWEyYmMtOGQ1ZGZjNmRkYjFhXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "929078"
    },
    {
      "id": "tt0021749",
      "rank": "53",
      "title": "City Lights",
      "fullTitle": "City Lights (1931)",
      "year": "1931",
      "image": "https://m.media-amazon.com/images/M/MV5BY2I4MmM1N2EtM2YzOS00OWUzLTkzYzctNDc5NDg2N2IyODJmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "192771"
    },
    {
      "id": "tt0078788",
      "rank": "54",
      "title": "Apocalypse Now",
      "fullTitle": "Apocalypse Now (1979)",
      "year": "1979",
      "image": "https://m.media-amazon.com/images/M/MV5BYmQyNTA1ZGItNjZjMi00NzFlLWEzMWEtNWMwN2Q2MjJhYzEyXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "697268"
    },
    {
      "id": "tt1853728",
      "rank": "55",
      "title": "Django Unchained",
      "fullTitle": "Django Unchained (2012)",
      "year": "2012",
      "image": "https://m.media-amazon.com/images/M/MV5BMjIyNTQ5NjQ1OV5BMl5BanBnXkFtZTcwODg1MDU4OA@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "1652752"
    },
    {
      "id": "tt0209144",
      "rank": "56",
      "title": "Memento",
      "fullTitle": "Memento (2000)",
      "year": "2000",
      "image": "https://m.media-amazon.com/images/M/MV5BZTcyNjk1MjgtOWI3Mi00YzQwLWI5MTktMzY4ZmI2NDAyNzYzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1297608"
    },
    {
      "id": "tt0082971",
      "rank": "57",
      "title": "Raiders of the Lost Ark",
      "fullTitle": "Raiders of the Lost Ark (1981)",
      "year": "1981",
      "image": "https://m.media-amazon.com/images/M/MV5BNTU2ODkyY2MtMjU1NC00NjE1LWEzYjgtMWQ3MzRhMTE0NDc0XkEyXkFqcGdeQXVyMjM4MzQ4OTQ@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1019729"
    },
    {
      "id": "tt0910970",
      "rank": "58",
      "title": "WALL·E",
      "fullTitle": "WALL·E (2008)",
      "year": "2008",
      "image": "https://m.media-amazon.com/images/M/MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1174706"
    },
    {
      "id": "tt0405094",
      "rank": "59",
      "title": "The Lives of Others",
      "fullTitle": "The Lives of Others (2006)",
      "year": "2006",
      "image": "https://m.media-amazon.com/images/M/MV5BNmQyNmJjM2ItNTQzYi00ZjMxLWFjMDYtZjUyN2YwZDk5YWQ2XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "404032"
    },
    {
      "id": "tt0043014",
      "rank": "60",
      "title": "Sunset Blvd.",
      "fullTitle": "Sunset Blvd. (1950)",
      "year": "1950",
      "image": "https://m.media-amazon.com/images/M/MV5BMTU0NTkyNzYwMF5BMl5BanBnXkFtZTgwMDU0NDk5MTI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "232332"
    },
    {
      "id": "tt15398776",
      "rank": "61",
      "title": "Oppenheimer",
      "fullTitle": "Oppenheimer (2023)",
      "year": "2023",
      "image": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.5",
      "imDbRatingCount": "526189"
    },
    {
      "id": "tt0050825",
      "rank": "62",
      "title": "Paths of Glory",
      "fullTitle": "Paths of Glory (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BOTI5Nzc0OTMtYzBkMS00NjkxLThmM2UtNjM2ODgxN2M5NjNkXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "208175"
    },
    {
      "id": "tt4154756",
      "rank": "63",
      "title": "Avengers: Infinity War",
      "fullTitle": "Avengers: Infinity War (2018)",
      "year": "2018",
      "image": "https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1169258"
    },
    {
      "id": "tt0081505",
      "rank": "64",
      "title": "The Shining",
      "fullTitle": "The Shining (1980)",
      "year": "1980",
      "image": "https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTg0YjQtYzY1ZGE3NTA5NGQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1083235"
    },
    {
      "id": "tt4633694",
      "rank": "65",
      "title": "Spider-Man: Into the Spider-Verse",
      "fullTitle": "Spider-Man: Into the Spider-Verse (2018)",
      "year": "2018",
      "image": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "642786"
    },
    {
      "id": "tt0032553",
      "rank": "66",
      "title": "The Great Dictator",
      "fullTitle": "The Great Dictator (1940)",
      "year": "1940",
      "image": "https://m.media-amazon.com/images/M/MV5BMmExYWJjNTktNGUyZS00ODhmLTkxYzAtNWIzOGEyMGNiMmUwXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "233754"
    },
    {
      "id": "tt0051201",
      "rank": "67",
      "title": "Witness for the Prosecution",
      "fullTitle": "Witness for the Prosecution (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BNDQwODU5OWYtNDcyNi00MDQ1LThiOGMtZDkwNWJiM2Y3MDg0XkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "133982"
    },
    {
      "id": "tt0090605",
      "rank": "68",
      "title": "Aliens",
      "fullTitle": "Aliens (1986)",
      "year": "1986",
      "image": "https://m.media-amazon.com/images/M/MV5BOGJkY2EyOWYtYWRmNy00ZTEzLTllMDAtYzYzYjA0ZjFhZWJjXkEyXkFqcGdeQXVyMTUzMDUzNTI3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "749178"
    },
    {
      "id": "tt0361748",
      "rank": "69",
      "title": "Inglourious Basterds",
      "fullTitle": "Inglourious Basterds (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BOTJiNDEzOWYtMTVjOC00ZjlmLWE0NGMtZmE1OWVmZDQ2OWJhXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1542077"
    },
    {
      "id": "tt1345836",
      "rank": "70",
      "title": "The Dark Knight Rises",
      "fullTitle": "The Dark Knight Rises (2012)",
      "year": "2012",
      "image": "https://m.media-amazon.com/images/M/MV5BMTk4ODQzNDY3Ml5BMl5BanBnXkFtZTcwODA0NTM4Nw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1790241"
    },
    {
      "id": "tt0169547",
      "rank": "71",
      "title": "American Beauty",
      "fullTitle": "American Beauty (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BNTBmZWJkNjctNDhiNC00MGE2LWEwOTctZTk5OGVhMWMyNmVhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1193549"
    },
    {
      "id": "tt0057012",
      "rank": "72",
      "title": "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
      "fullTitle": "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1964)",
      "year": "1964",
      "image": "https://m.media-amazon.com/images/M/MV5BMWMxYjZkOWUtM2FjMi00MmI1LThkNzQtNTM5Y2E2ZGQ2NGFhXkEyXkFqcGdeQXVyMTA0MTM5NjI2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "510007"
    },
    {
      "id": "tt0364569",
      "rank": "73",
      "title": "Oldboy",
      "fullTitle": "Oldboy (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BMTI3NTQyMzU5M15BMl5BanBnXkFtZTcwMTM2MjgyMQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "617972"
    },
    {
      "id": "tt2380307",
      "rank": "74",
      "title": "Coco",
      "fullTitle": "Coco (2017)",
      "year": "2017",
      "image": "https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkMDE3ZjAxXkEyXkFqcGdeQXVyODIxMzk5NjA@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "566335"
    },
    {
      "id": "tt0086879",
      "rank": "75",
      "title": "Amadeus",
      "fullTitle": "Amadeus (1984)",
      "year": "1984",
      "image": "https://m.media-amazon.com/images/M/MV5BNWJlNzUzNGMtYTAwMS00ZjI2LWFmNWQtODcxNWUxODA5YmU1XkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "420335"
    },
    {
      "id": "tt0114709",
      "rank": "76",
      "title": "Toy Story",
      "fullTitle": "Toy Story (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1046723"
    },
    {
      "id": "tt0082096",
      "rank": "77",
      "title": "Das Boot",
      "fullTitle": "Das Boot (1981)",
      "year": "1981",
      "image": "https://m.media-amazon.com/images/M/MV5BNDBjMWUxNTUtNjZiNi00YzJhLTgzNzUtMTRiY2FkZmMzYTNjXkEyXkFqcGdeQXVyMTUzMDUzNTI3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "260529"
    },
    {
      "id": "tt0112573",
      "rank": "78",
      "title": "Braveheart",
      "fullTitle": "Braveheart (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BMzkzMmU0YTYtOWM3My00YzBmLWI0YzctOGYyNTkwMWE5MTJkXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1075289"
    },
    {
      "id": "tt4154796",
      "rank": "79",
      "title": "Avengers: Endgame",
      "fullTitle": "Avengers: Endgame (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1229436"
    },
    {
      "id": "tt7286456",
      "rank": "80",
      "title": "Joker",
      "fullTitle": "Joker (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "1425328"
    },
    {
      "id": "tt0119698",
      "rank": "81",
      "title": "Princess Mononoke",
      "fullTitle": "Princess Mononoke (1997)",
      "year": "1997",
      "image": "https://m.media-amazon.com/images/M/MV5BNTZkYmI0MmEtNGFlZC00OWZjLWFjMmItMjk1OWZkOWJiZGVjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "420528"
    },
    {
      "id": "tt0119217",
      "rank": "82",
      "title": "Good Will Hunting",
      "fullTitle": "Good Will Hunting (1997)",
      "year": "1997",
      "image": "https://m.media-amazon.com/images/M/MV5BOTI0MzcxMTYtZDVkMy00NjY1LTgyMTYtZmUxN2M3NmQ2NWJhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1032510"
    },
    {
      "id": "tt5311514",
      "rank": "83",
      "title": "Your Name.",
      "fullTitle": "Your Name. (2016)",
      "year": "2016",
      "image": "https://m.media-amazon.com/images/M/MV5BODRmZDVmNzUtZDA4ZC00NjhkLWI2M2UtN2M0ZDIzNDcxYThjL2ltYWdlXkEyXkFqcGdeQXVyNTk0MzMzODA@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "304858"
    },
    {
      "id": "tt0087843",
      "rank": "84",
      "title": "Once Upon a Time in America",
      "fullTitle": "Once Upon a Time in America (1984)",
      "year": "1984",
      "image": "https://m.media-amazon.com/images/M/MV5BMmQzZjdmZDAtOGE2Yy00MmUwLTljYzgtZTMwMjk3ZDdiOWUyXkEyXkFqcGdeQXVyNjc5NjEzNA@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "370151"
    },
    {
      "id": "tt0057565",
      "rank": "85",
      "title": "High and Low",
      "fullTitle": "High and Low (1963)",
      "year": "1963",
      "image": "https://m.media-amazon.com/images/M/MV5BOTI4NTNhZDMtMWNkZi00MTRmLWJmZDQtMmJkMGVmZTEzODlhXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "50802"
    },
    {
      "id": "tt1187043",
      "rank": "86",
      "title": "3 Idiots",
      "fullTitle": "3 Idiots (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "422403"
    },
    {
      "id": "tt0045152",
      "rank": "87",
      "title": "Singin' in the Rain",
      "fullTitle": "Singin' in the Rain (1952)",
      "year": "1952",
      "image": "https://m.media-amazon.com/images/M/MV5BZDRjNGViMjQtOThlMi00MTA3LThkYzQtNzJkYjBkMGE0YzE1XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "255395"
    },
    {
      "id": "tt8267604",
      "rank": "88",
      "title": "Capernaum",
      "fullTitle": "Capernaum (2018)",
      "year": "2018",
      "image": "https://m.media-amazon.com/images/M/MV5BMmExNzU2ZWMtYzUwYi00YmM2LTkxZTQtNmVhNjY0NTMyMWI2XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "101032"
    },
    {
      "id": "tt0180093",
      "rank": "89",
      "title": "Requiem for a Dream",
      "fullTitle": "Requiem for a Dream (2000)",
      "year": "2000",
      "image": "https://m.media-amazon.com/images/M/MV5BOTdiNzJlOWUtNWMwNS00NmFlLWI0YTEtZmI3YjIzZWUyY2Y3XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "882035"
    },
    {
      "id": "tt0091251",
      "rank": "90",
      "title": "Come and See",
      "fullTitle": "Come and See (1985)",
      "year": "1985",
      "image": "https://m.media-amazon.com/images/M/MV5BODM4Njg0NTAtYjI5Ny00ZjAxLTkwNmItZTMxMWU5M2U3M2RjXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.4",
      "imDbRatingCount": "92072"
    },
    {
      "id": "tt0435761",
      "rank": "91",
      "title": "Toy Story 3",
      "fullTitle": "Toy Story 3 (2010)",
      "year": "2010",
      "image": "https://m.media-amazon.com/images/M/MV5BMTgxOTY4Mjc0MF5BMl5BanBnXkFtZTcwNTA4MDQyMw@@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "876451"
    },
    {
      "id": "tt0086190",
      "rank": "92",
      "title": "Star Wars: Episode VI - Return of the Jedi",
      "fullTitle": "Star Wars: Episode VI - Return of the Jedi (1983)",
      "year": "1983",
      "image": "https://m.media-amazon.com/images/M/MV5BOWZlMjFiYzgtMTUzNC00Y2IzLTk1NTMtZmNhMTczNTk0ODk1XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1101326"
    },
    {
      "id": "tt0338013",
      "rank": "93",
      "title": "Eternal Sunshine of the Spotless Mind",
      "fullTitle": "Eternal Sunshine of the Spotless Mind (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1054989"
    },
    {
      "id": "tt0062622",
      "rank": "94",
      "title": "2001: A Space Odyssey",
      "fullTitle": "2001: A Space Odyssey (1968)",
      "year": "1968",
      "image": "https://m.media-amazon.com/images/M/MV5BMmNlYzRiNDctZWNhMi00MzI4LThkZTctMTUzMmZkMmFmNThmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "704616"
    },
    {
      "id": "tt2106476",
      "rank": "95",
      "title": "The Hunt",
      "fullTitle": "The Hunt (2012)",
      "year": "2012",
      "image": "https://m.media-amazon.com/images/M/MV5BMTg2NDg3ODg4NF5BMl5BanBnXkFtZTcwNzk3NTc3Nw@@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "354177"
    },
    {
      "id": "tt0105236",
      "rank": "96",
      "title": "Reservoir Dogs",
      "fullTitle": "Reservoir Dogs (1992)",
      "year": "1992",
      "image": "https://m.media-amazon.com/images/M/MV5BZmExNmEwYWItYmQzOS00YjA5LTk2MjktZjEyZDE1Y2QxNjA1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1067726"
    },
    {
      "id": "tt0044741",
      "rank": "97",
      "title": "Ikiru",
      "fullTitle": "Ikiru (1952)",
      "year": "1952",
      "image": "https://m.media-amazon.com/images/M/MV5BYWM1YmZkNTctZDAwNy00ZTY4LWFjMTktYzU4ZjViMmU1OTJmXkEyXkFqcGdeQXVyMTA0MTM5NjI2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "85053"
    },
    {
      "id": "tt0056172",
      "rank": "98",
      "title": "Lawrence of Arabia",
      "fullTitle": "Lawrence of Arabia (1962)",
      "year": "1962",
      "image": "https://m.media-amazon.com/images/M/MV5BYWY5ZjhjNGYtZmI2Ny00ODM0LWFkNzgtZmI1YzA2N2MxMzA0XkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "308103"
    },
    {
      "id": "tt0053604",
      "rank": "99",
      "title": "The Apartment",
      "fullTitle": "The Apartment (1960)",
      "year": "1960",
      "image": "https://m.media-amazon.com/images/M/MV5BNzkwODFjNzItMmMwNi00MTU5LWE2MzktM2M4ZDczZGM1MmViXkEyXkFqcGdeQXVyNDY2MTk1ODk@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "191954"
    },
    {
      "id": "tt0033467",
      "rank": "100",
      "title": "Citizen Kane",
      "fullTitle": "Citizen Kane (1941)",
      "year": "1941",
      "image": "https://m.media-amazon.com/images/M/MV5BYjBiOTYxZWItMzdiZi00NjlkLWIzZTYtYmFhZjhiMTljOTdkXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "459198"
    },
    {
      "id": "tt0022100",
      "rank": "101",
      "title": "M",
      "fullTitle": "M (1931)",
      "year": "1931",
      "image": "https://m.media-amazon.com/images/M/MV5BODA4ODk3OTEzMF5BMl5BanBnXkFtZTgwMTQ2ODMwMzE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "165590"
    },
    {
      "id": "tt0053125",
      "rank": "102",
      "title": "North by Northwest",
      "fullTitle": "North by Northwest (1959)",
      "year": "1959",
      "image": "https://m.media-amazon.com/images/M/MV5BZDA3NDExMTUtMDlhOC00MmQ5LWExZGUtYmI1NGVlZWI4OWNiXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "340797"
    },
    {
      "id": "tt0052357",
      "rank": "103",
      "title": "Vertigo",
      "fullTitle": "Vertigo (1958)",
      "year": "1958",
      "image": "https://m.media-amazon.com/images/M/MV5BYTE4ODEwZDUtNDFjOC00NjAxLWEzYTQtYTI1NGVmZmFlNjdiL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "419665"
    },
    {
      "id": "tt0036775",
      "rank": "104",
      "title": "Double Indemnity",
      "fullTitle": "Double Indemnity (1944)",
      "year": "1944",
      "image": "https://m.media-amazon.com/images/M/MV5BOTdlNjgyZGUtOTczYi00MDdhLTljZmMtYTEwZmRiOWFkYjRhXkEyXkFqcGdeQXVyNDY2MTk1ODk@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "164571"
    },
    {
      "id": "tt0211915",
      "rank": "105",
      "title": "Amélie",
      "fullTitle": "Amélie (2001)",
      "year": "2001",
      "image": "https://m.media-amazon.com/images/M/MV5BNDg4NjM1YjMtYmNhZC00MjM0LWFiZmYtNGY1YjA3MzZmODc5XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "783061"
    },
    {
      "id": "tt0086250",
      "rank": "106",
      "title": "Scarface",
      "fullTitle": "Scarface (1983)",
      "year": "1983",
      "image": "https://m.media-amazon.com/images/M/MV5BNjdjNGQ4NDEtNTEwYS00MTgxLTliYzQtYzE2ZDRiZjFhZmNlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "894293"
    },
    {
      "id": "tt0093058",
      "rank": "107",
      "title": "Full Metal Jacket",
      "fullTitle": "Full Metal Jacket (1987)",
      "year": "1987",
      "image": "https://m.media-amazon.com/images/M/MV5BNzkxODk0NjEtYjc4Mi00ZDI0LTgyYjEtYzc1NDkxY2YzYTgyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "776030"
    },
    {
      "id": "tt1255953",
      "rank": "108",
      "title": "Incendies",
      "fullTitle": "Incendies (2010)",
      "year": "2010",
      "image": "https://m.media-amazon.com/images/M/MV5BMWE3MGYzZjktY2Q5Mi00Y2NiLWIyYWUtMmIyNzA3YmZlMGFhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "191839"
    },
    {
      "id": "tt0066921",
      "rank": "109",
      "title": "A Clockwork Orange",
      "fullTitle": "A Clockwork Orange (1971)",
      "year": "1971",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY3MjM1Mzc4N15BMl5BanBnXkFtZTgwODM0NzAxMDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "866214"
    },
    {
      "id": "tt0113277",
      "rank": "110",
      "title": "Heat",
      "fullTitle": "Heat (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BYjZjNTJlZGUtZTE1Ny00ZDc4LTgwYjUtMzk0NDgwYzZjYTk1XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "700838"
    },
    {
      "id": "tt1049413",
      "rank": "111",
      "title": "Up",
      "fullTitle": "Up (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BYjBkM2RjMzItM2M3Ni00N2NjLWE3NzMtMGY4MzE4MDAzMTRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "1100376"
    },
    {
      "id": "tt0056592",
      "rank": "112",
      "title": "To Kill a Mockingbird",
      "fullTitle": "To Kill a Mockingbird (1962)",
      "year": "1962",
      "image": "https://m.media-amazon.com/images/M/MV5BNmVmYzcwNzMtMWM1NS00MWIyLThlMDEtYzUwZDgzODE1NmE2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "328172"
    },
    {
      "id": "tt8503618",
      "rank": "113",
      "title": "Hamilton",
      "fullTitle": "Hamilton (2020)",
      "year": "2020",
      "image": "https://m.media-amazon.com/images/M/MV5BNjViNWRjYWEtZTI0NC00N2E3LTk0NGQtMjY4NTM3OGNkZjY0XkEyXkFqcGdeQXVyMjUxMTY3ODM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "108365"
    },
    {
      "id": "tt0070735",
      "rank": "114",
      "title": "The Sting",
      "fullTitle": "The Sting (1973)",
      "year": "1973",
      "image": "https://m.media-amazon.com/images/M/MV5BNGU3NjQ4YTMtZGJjOS00YTQ3LThmNmItMTI5MDE2ODI3NzY3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "274728"
    },
    {
      "id": "tt1832382",
      "rank": "115",
      "title": "A Separation",
      "fullTitle": "A Separation (2011)",
      "year": "2011",
      "image": "https://m.media-amazon.com/images/M/MV5BN2JmMjViMjMtZTM5Mi00ZGZkLTk5YzctZDg5MjFjZDE4NjNkXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "254601"
    },
    {
      "id": "tt0097576",
      "rank": "116",
      "title": "Indiana Jones and the Last Crusade",
      "fullTitle": "Indiana Jones and the Last Crusade (1989)",
      "year": "1989",
      "image": "https://m.media-amazon.com/images/M/MV5BY2Q0ODg4ZmItNDZiYi00ZWY5LTg2NzctNmYwZjA5OThmNzE1XkEyXkFqcGdeQXVyMjM4MzQ4OTQ@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "797088"
    },
    {
      "id": "tt0017136",
      "rank": "117",
      "title": "Metropolis",
      "fullTitle": "Metropolis (1927)",
      "year": "1927",
      "image": "https://m.media-amazon.com/images/M/MV5BMTg5YWIyMWUtZDY5My00Zjc1LTljOTctYmI0MWRmY2M2NmRkXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "182236"
    },
    {
      "id": "tt0095016",
      "rank": "118",
      "title": "Die Hard",
      "fullTitle": "Die Hard (1988)",
      "year": "1988",
      "image": "https://m.media-amazon.com/images/M/MV5BZjRlNDUxZjAtOGQ4OC00OTNlLTgxNmQtYTBmMDgwZmNmNjkxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "919551"
    },
    {
      "id": "tt0986264",
      "rank": "119",
      "title": "Like Stars on Earth",
      "fullTitle": "Like Stars on Earth (2007)",
      "year": "2007",
      "image": "https://m.media-amazon.com/images/M/MV5BYjY0MGU3MmQtMGVhOS00M2IyLWI1MTktZGUxMzBjMTE5ZDA3XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "202997"
    },
    {
      "id": "tt0208092",
      "rank": "120",
      "title": "Snatch",
      "fullTitle": "Snatch (2000)",
      "year": "2000",
      "image": "https://m.media-amazon.com/images/M/MV5BMTA2NDYxOGYtYjU1Mi00Y2QzLTgxMTQtMWI1MGI0ZGQ5MmU4XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "893045"
    },
    {
      "id": "tt0040522",
      "rank": "121",
      "title": "Bicycle Thieves",
      "fullTitle": "Bicycle Thieves (1948)",
      "year": "1948",
      "image": "https://m.media-amazon.com/images/M/MV5BNmI1ODdjODctMDlmMC00ZWViLWI5MzYtYzRhNDdjYmM3MzFjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "171805"
    },
    {
      "id": "tt0119488",
      "rank": "122",
      "title": "L.A. Confidential",
      "fullTitle": "L.A. Confidential (1997)",
      "year": "1997",
      "image": "https://m.media-amazon.com/images/M/MV5BMDQ2YzEyZGItYWRhOS00MjBmLTkzMDUtMTdjYzkyMmQxZTJlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "605501"
    },
    {
      "id": "tt0075314",
      "rank": "123",
      "title": "Taxi Driver",
      "fullTitle": "Taxi Driver (1976)",
      "year": "1976",
      "image": "https://m.media-amazon.com/images/M/MV5BM2M1MmVhNDgtNmI0YS00ZDNmLTkyNjctNTJiYTQ2N2NmYzc2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "896344"
    },
    {
      "id": "tt8579674",
      "rank": "124",
      "title": "1917",
      "fullTitle": "1917 (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BOTdmNTFjNDEtNzg0My00ZjkxLTg1ZDAtZTdkMDc2ZmFiNWQ1XkEyXkFqcGdeQXVyNTAzNzgwNTg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "651619"
    },
    {
      "id": "tt0363163",
      "rank": "125",
      "title": "Downfall",
      "fullTitle": "Downfall (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BMTU0NTU5NTAyMl5BMl5BanBnXkFtZTYwNzYwMDg2._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "369396"
    },
    {
      "id": "tt5074352",
      "rank": "126",
      "title": "Dangal",
      "fullTitle": "Dangal (2016)",
      "year": "2016",
      "image": "https://m.media-amazon.com/images/M/MV5BMTQ4MzQzMzM2Nl5BMl5BanBnXkFtZTgwMTQ1NzU3MDI@._V1_Ratio0.7150_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "204222"
    },
    {
      "id": "tt0059578",
      "rank": "127",
      "title": "For a Few Dollars More",
      "fullTitle": "For a Few Dollars More (1965)",
      "year": "1965",
      "image": "https://m.media-amazon.com/images/M/MV5BMzJlZTNkYjQtMTE1OS00YTJlLTgxNjItYzg4NTllODdkMzBiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "269215"
    },
    {
      "id": "tt0372784",
      "rank": "128",
      "title": "Batman Begins",
      "fullTitle": "Batman Begins (2005)",
      "year": "2005",
      "image": "https://m.media-amazon.com/images/M/MV5BOTY4YjI2N2MtYmFlMC00ZjcyLTg3YjEtMDQyM2ZjYzQ5YWFkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1546677"
    },
    {
      "id": "tt1745960",
      "rank": "129",
      "title": "Top Gun: Maverick",
      "fullTitle": "Top Gun: Maverick (2022)",
      "year": "2022",
      "image": "https://m.media-amazon.com/images/M/MV5BZWYzOGEwNTgtNWU3NS00ZTQ0LWJkODUtMmVhMjIwMjA1ZmQwXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "643733"
    },
    {
      "id": "tt0053291",
      "rank": "130",
      "title": "Some Like It Hot",
      "fullTitle": "Some Like It Hot (1959)",
      "year": "1959",
      "image": "https://m.media-amazon.com/images/M/MV5BNzAyOGIxYjAtMGY2NC00ZTgyLWIwMWEtYzY0OWQ4NDFjOTc5XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "278898"
    },
    {
      "id": "tt0012349",
      "rank": "131",
      "title": "The Kid",
      "fullTitle": "The Kid (1921)",
      "year": "1921",
      "image": "https://m.media-amazon.com/images/M/MV5BZjhhMThhNDItNTY2MC00MmU1LTliNDEtNDdhZjdlNTY5ZDQ1XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "132499"
    },
    {
      "id": "tt0993846",
      "rank": "132",
      "title": "The Wolf of Wall Street",
      "fullTitle": "The Wolf of Wall Street (2013)",
      "year": "2013",
      "image": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1531406"
    },
    {
      "id": "tt10272386",
      "rank": "133",
      "title": "The Father",
      "fullTitle": "The Father (2020)",
      "year": "2020",
      "image": "https://m.media-amazon.com/images/M/MV5BZGJhNWRiOWQtMjI4OS00ZjcxLTgwMTAtMzQ2ODkxY2JkOTVlXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "181688"
    },
    {
      "id": "tt6966692",
      "rank": "134",
      "title": "Green Book",
      "fullTitle": "Green Book (2018)",
      "year": "2018",
      "image": "https://m.media-amazon.com/images/M/MV5BYzIzYmJlYTYtNGNiYy00N2EwLTk4ZjItMGYyZTJiOTVkM2RlXkEyXkFqcGdeQXVyODY1NDk1NjE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "543801"
    },
    {
      "id": "tt0042192",
      "rank": "135",
      "title": "All About Eve",
      "fullTitle": "All About Eve (1950)",
      "year": "1950",
      "image": "https://m.media-amazon.com/images/M/MV5BYmE1M2Y3NTYtYTI0Mi00N2JlLTkzMzItOTY1MTlhNWNkMDgzXkEyXkFqcGdeQXVyMTUzMDUzNTI3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "136757"
    },
    {
      "id": "tt0055031",
      "rank": "136",
      "title": "Judgment at Nuremberg",
      "fullTitle": "Judgment at Nuremberg (1961)",
      "year": "1961",
      "image": "https://m.media-amazon.com/images/M/MV5BNDc2ODQ5NTE2MV5BMl5BanBnXkFtZTcwODExMjUyNA@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.3",
      "imDbRatingCount": "82840"
    },
    {
      "id": "tt0120382",
      "rank": "137",
      "title": "The Truman Show",
      "fullTitle": "The Truman Show (1998)",
      "year": "1998",
      "image": "https://m.media-amazon.com/images/M/MV5BMDIzODcyY2EtMmY2MC00ZWVlLTgwMzAtMjQwOWUyNmJjNTYyXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1160012"
    },
    {
      "id": "tt0469494",
      "rank": "138",
      "title": "There Will Be Blood",
      "fullTitle": "There Will Be Blood (2007)",
      "year": "2007",
      "image": "https://m.media-amazon.com/images/M/MV5BMjAxODQ4MDU5NV5BMl5BanBnXkFtZTcwMDU4MjU1MQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "626585"
    },
    {
      "id": "tt0112641",
      "rank": "139",
      "title": "Casino",
      "fullTitle": "Casino (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BMTcxOWYzNDYtYmM4YS00N2NkLTk0NTAtNjg1ODgwZjAxYzI3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "551124"
    },
    {
      "id": "tt1130884",
      "rank": "140",
      "title": "Shutter Island",
      "fullTitle": "Shutter Island (2010)",
      "year": "2010",
      "image": "https://m.media-amazon.com/images/M/MV5BYzhiNDkyNzktNTZmYS00ZTBkLTk2MDAtM2U0YjU1MzgxZjgzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1412821"
    },
    {
      "id": "tt0089881",
      "rank": "141",
      "title": "Ran",
      "fullTitle": "Ran (1985)",
      "year": "1985",
      "image": "https://m.media-amazon.com/images/M/MV5BMmU1NGYwZWYtOWExNi00ZTEyLTgwMmUtM2ZlMDVjNWM4YjVlXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "133252"
    },
    {
      "id": "tt0457430",
      "rank": "142",
      "title": "Pan's Labyrinth",
      "fullTitle": "Pan's Labyrinth (2006)",
      "year": "2006",
      "image": "https://m.media-amazon.com/images/M/MV5BYzFjMThiMGItOWRlMC00MDI4LThmOGUtYTNlZGZiYWI1YjMyXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "693278"
    },
    {
      "id": "tt0107290",
      "rank": "143",
      "title": "Jurassic Park",
      "fullTitle": "Jurassic Park (1993)",
      "year": "1993",
      "image": "https://m.media-amazon.com/images/M/MV5BMjM2MDgxMDg0Nl5BMl5BanBnXkFtZTgwNTM2OTM5NDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1043746"
    },
    {
      "id": "tt0167404",
      "rank": "144",
      "title": "The Sixth Sense",
      "fullTitle": "The Sixth Sense (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BMWM4NTFhYjctNzUyNi00NGMwLTk3NTYtMDIyNTZmMzRlYmQyXkEyXkFqcGdeQXVyMTAwMzUyOTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1032479"
    },
    {
      "id": "tt0105695",
      "rank": "145",
      "title": "Unforgiven",
      "fullTitle": "Unforgiven (1992)",
      "year": "1992",
      "image": "https://m.media-amazon.com/images/M/MV5BODM3YWY4NmQtN2Y3Ni00OTg0LWFhZGQtZWE3ZWY4MTJlOWU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "429276"
    },
    {
      "id": "tt0268978",
      "rank": "146",
      "title": "A Beautiful Mind",
      "fullTitle": "A Beautiful Mind (2001)",
      "year": "2001",
      "image": "https://m.media-amazon.com/images/M/MV5BMzcwYWFkYzktZjAzNC00OGY1LWI4YTgtNzc5MzVjMDVmNjY0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "970007"
    },
    {
      "id": "tt0477348",
      "rank": "147",
      "title": "No Country for Old Men",
      "fullTitle": "No Country for Old Men (2007)",
      "year": "2007",
      "image": "https://m.media-amazon.com/images/M/MV5BMjA5Njk3MjM4OV5BMl5BanBnXkFtZTcwMTc5MTE1MQ@@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1033624"
    },
    {
      "id": "tt0040897",
      "rank": "148",
      "title": "The Treasure of the Sierra Madre",
      "fullTitle": "The Treasure of the Sierra Madre (1948)",
      "year": "1948",
      "image": "https://m.media-amazon.com/images/M/MV5BOTJlZWMxYzEtMjlkMS00ODE0LThlM2ItMDI3NGQ2YjhmMzkxXkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "130547"
    },
    {
      "id": "tt0055630",
      "rank": "149",
      "title": "Yojimbo",
      "fullTitle": "Yojimbo (1961)",
      "year": "1961",
      "image": "https://m.media-amazon.com/images/M/MV5BZThiZjAzZjgtNDU3MC00YThhLThjYWUtZGRkYjc2ZWZlOTVjXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "128946"
    },
    {
      "id": "tt0266697",
      "rank": "150",
      "title": "Kill Bill: Vol. 1",
      "fullTitle": "Kill Bill: Vol. 1 (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BNzM3NDFhYTAtYmU5Mi00NGRmLTljYjgtMDkyODQ4MjNkMGY2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1167949"
    },
    {
      "id": "tt0084787",
      "rank": "151",
      "title": "The Thing",
      "fullTitle": "The Thing (1982)",
      "year": "1982",
      "image": "https://m.media-amazon.com/images/M/MV5BNGViZWZmM2EtNGYzZi00ZDAyLTk3ODMtNzIyZTBjN2Y1NmM1XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "454794"
    },
    {
      "id": "tt0071853",
      "rank": "152",
      "title": "Monty Python and the Holy Grail",
      "fullTitle": "Monty Python and the Holy Grail (1975)",
      "year": "1975",
      "image": "https://m.media-amazon.com/images/M/MV5BN2IyNTE4YzUtZWU0Mi00MGIwLTgyMmQtMzQ4YzQxYWNlYWE2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "562054"
    },
    {
      "id": "tt0057115",
      "rank": "153",
      "title": "The Great Escape",
      "fullTitle": "The Great Escape (1963)",
      "year": "1963",
      "image": "https://m.media-amazon.com/images/M/MV5BNzA2NmYxMWUtNzBlMC00MWM2LTkwNmQtYTFlZjQwODNhOWE0XkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "254850"
    },
    {
      "id": "tt0266543",
      "rank": "154",
      "title": "Finding Nemo",
      "fullTitle": "Finding Nemo (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BZmYxZjg3OWEtNzg5Yi00M2YzLWI1YzYtYTQ0NTgwNzhjN2E1XkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1091956"
    },
    {
      "id": "tt0042876",
      "rank": "155",
      "title": "Rashomon",
      "fullTitle": "Rashomon (1950)",
      "year": "1950",
      "image": "https://m.media-amazon.com/images/M/MV5BMjEzMzA4NDE2OF5BMl5BanBnXkFtZTcwNTc5MDI2NQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "177048"
    },
    {
      "id": "tt0080678",
      "rank": "156",
      "title": "The Elephant Man",
      "fullTitle": "The Elephant Man (1980)",
      "year": "1980",
      "image": "https://m.media-amazon.com/images/M/MV5BMDVjNjIwOGItNDE3Ny00OThjLWE0NzQtZTU3YjMzZTZjMzhkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "253837"
    },
    {
      "id": "tt0071315",
      "rank": "157",
      "title": "Chinatown",
      "fullTitle": "Chinatown (1974)",
      "year": "1974",
      "image": "https://m.media-amazon.com/images/M/MV5BMjJkMDZhYzItZTFhMi00ZGI4LThlNTAtZDNlYmEwNjFkNDYzXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "342835"
    },
    {
      "id": "tt0347149",
      "rank": "158",
      "title": "Howl's Moving Castle",
      "fullTitle": "Howl's Moving Castle (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BNmM4YTFmMmItMGE3Yy00MmRkLTlmZGEtMzZlOTQzYjk3MzA2XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "430882"
    },
    {
      "id": "tt0046912",
      "rank": "159",
      "title": "Dial M for Murder",
      "fullTitle": "Dial M for Murder (1954)",
      "year": "1954",
      "image": "https://m.media-amazon.com/images/M/MV5BOWIwODIxYWItZDI4MS00YzhhLWE3MmYtMzlhZDIwOTMzZmE5L2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "185234"
    },
    {
      "id": "tt0031381",
      "rank": "160",
      "title": "Gone with the Wind",
      "fullTitle": "Gone with the Wind (1939)",
      "year": "1939",
      "image": "https://m.media-amazon.com/images/M/MV5BYjUyZWZkM2UtMzYxYy00ZmQ3LWFmZTQtOGE2YjBkNjA3YWZlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "328697"
    },
    {
      "id": "tt0434409",
      "rank": "161",
      "title": "V for Vendetta",
      "fullTitle": "V for Vendetta (2005)",
      "year": "2005",
      "image": "https://m.media-amazon.com/images/M/MV5BOTI5ODc3NzExNV5BMl5BanBnXkFtZTcwNzYxNzQzMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "1162555"
    },
    {
      "id": "tt1392214",
      "rank": "162",
      "title": "Prisoners",
      "fullTitle": "Prisoners (2013)",
      "year": "2013",
      "image": "https://m.media-amazon.com/images/M/MV5BMTg0NTIzMjQ1NV5BMl5BanBnXkFtZTcwNDc3MzM5OQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "781702"
    },
    {
      "id": "tt0081398",
      "rank": "163",
      "title": "Raging Bull",
      "fullTitle": "Raging Bull (1980)",
      "year": "1980",
      "image": "https://m.media-amazon.com/images/M/MV5BYjRmODkzNDItMTNhNi00YjJlLTg0ZjAtODlhZTM0YzgzYThlXkEyXkFqcGdeQXVyNzQ1ODk3MTQ@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "372613"
    },
    {
      "id": "tt0120735",
      "rank": "164",
      "title": "Lock, Stock and Two Smoking Barrels",
      "fullTitle": "Lock, Stock and Two Smoking Barrels (1998)",
      "year": "1998",
      "image": "https://m.media-amazon.com/images/M/MV5BMTAyN2JmZmEtNjAyMy00NzYwLThmY2MtYWQ3OGNhNjExMmM4XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "606680"
    },
    {
      "id": "tt1305806",
      "rank": "165",
      "title": "The Secret in Their Eyes",
      "fullTitle": "The Secret in Their Eyes (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BMTgwNTI3OTczOV5BMl5BanBnXkFtZTcwMTM3MTUyMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "218797"
    },
    {
      "id": "tt2096673",
      "rank": "166",
      "title": "Inside Out",
      "fullTitle": "Inside Out (2015)",
      "year": "2015",
      "image": "https://m.media-amazon.com/images/M/MV5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "763806"
    },
    {
      "id": "tt10872600",
      "rank": "167",
      "title": "Spider-Man: No Way Home",
      "fullTitle": "Spider-Man: No Way Home (2021)",
      "year": "2021",
      "image": "https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjAxZTU3NzBiXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "845964"
    },
    {
      "id": "tt5027774",
      "rank": "168",
      "title": "Three Billboards Outside Ebbing, Missouri",
      "fullTitle": "Three Billboards Outside Ebbing, Missouri (2017)",
      "year": "2017",
      "image": "https://m.media-amazon.com/images/M/MV5BMjI0ODcxNzM1N15BMl5BanBnXkFtZTgwMzIwMTEwNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "541493"
    },
    {
      "id": "tt0117951",
      "rank": "169",
      "title": "Trainspotting",
      "fullTitle": "Trainspotting (1996)",
      "year": "1996",
      "image": "https://m.media-amazon.com/images/M/MV5BMzA5Zjc3ZTMtMmU5YS00YTMwLWI4MWUtYTU0YTVmNjVmODZhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "714293"
    },
    {
      "id": "tt0050212",
      "rank": "170",
      "title": "The Bridge on the River Kwai",
      "fullTitle": "The Bridge on the River Kwai (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BOGY5NmNlMmQtYzRlYy00NGQ5LWFkYjYtNzExZmQyMTg0ZDA0XkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "230049"
    },
    {
      "id": "tt0116282",
      "rank": "171",
      "title": "Fargo",
      "fullTitle": "Fargo (1996)",
      "year": "1996",
      "image": "https://m.media-amazon.com/images/M/MV5BNDJiZDgyZjctYmRjMS00ZjdkLTkwMTEtNGU1NDg3NDQ0Yzk1XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "709065"
    },
    {
      "id": "tt1291584",
      "rank": "172",
      "title": "Warrior",
      "fullTitle": "Warrior (2011)",
      "year": "2011",
      "image": "https://m.media-amazon.com/images/M/MV5BMTk4ODk5MTMyNV5BMl5BanBnXkFtZTcwMDMyNTg0Ng@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "490605"
    },
    {
      "id": "tt0264464",
      "rank": "173",
      "title": "Catch Me If You Can",
      "fullTitle": "Catch Me If You Can (2002)",
      "year": "2002",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY5MzYzNjc5NV5BMl5BanBnXkFtZTYwNTUyNTc2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "1061811"
    },
    {
      "id": "tt1205489",
      "rank": "174",
      "title": "Gran Torino",
      "fullTitle": "Gran Torino (2008)",
      "year": "2008",
      "image": "https://m.media-amazon.com/images/M/MV5BMTc5NTk2OTU1Nl5BMl5BanBnXkFtZTcwMDc3NjAwMg@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "803428"
    },
    {
      "id": "tt4729430",
      "rank": "175",
      "title": "Klaus",
      "fullTitle": "Klaus (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BMWYwOThjM2ItZGYxNy00NTQwLWFlZWEtM2MzM2Q5MmY3NDU5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "175109"
    },
    {
      "id": "tt0096283",
      "rank": "176",
      "title": "My Neighbor Totoro",
      "fullTitle": "My Neighbor Totoro (1988)",
      "year": "1988",
      "image": "https://m.media-amazon.com/images/M/MV5BYzJjMTYyMjQtZDI0My00ZjE2LTkyNGYtOTllNGQxNDMyZjE0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.7150_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "366542"
    },
    {
      "id": "tt0405159",
      "rank": "177",
      "title": "Million Dollar Baby",
      "fullTitle": "Million Dollar Baby (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BMTkxNzA1NDQxOV5BMl5BanBnXkFtZTcwNTkyMTIzMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "711661"
    },
    {
      "id": "tt1201607",
      "rank": "178",
      "title": "Harry Potter and the Deathly Hallows: Part 2",
      "fullTitle": "Harry Potter and the Deathly Hallows: Part 2 (2011)",
      "year": "2011",
      "image": "https://m.media-amazon.com/images/M/MV5BMGVmMWNiMDktYjQ0Mi00MWIxLTk0N2UtN2ZlYTdkN2IzNDNlXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "926253"
    },
    {
      "id": "tt0118849",
      "rank": "179",
      "title": "Children of Heaven",
      "fullTitle": "Children of Heaven (1997)",
      "year": "1997",
      "image": "https://m.media-amazon.com/images/M/MV5BZTYwZWQ4ZTQtZWU0MS00N2YwLWEzMDItZWFkZWY0MWVjODVhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "79008"
    },
    {
      "id": "tt0083658",
      "rank": "180",
      "title": "Blade Runner",
      "fullTitle": "Blade Runner (1982)",
      "year": "1982",
      "image": "https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "807134"
    },
    {
      "id": "tt2024544",
      "rank": "181",
      "title": "12 Years a Slave",
      "fullTitle": "12 Years a Slave (2013)",
      "year": "2013",
      "image": "https://m.media-amazon.com/images/M/MV5BMjExMTEzODkyN15BMl5BanBnXkFtZTcwNTU4NTc4OQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "729882"
    },
    {
      "id": "tt0112471",
      "rank": "182",
      "title": "Before Sunrise",
      "fullTitle": "Before Sunrise (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BZDdiZTAwYzAtMDI3Ni00OTRjLTkzN2UtMGE3MDMyZmU4NTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "331097"
    },
    {
      "id": "tt2278388",
      "rank": "183",
      "title": "The Grand Budapest Hotel",
      "fullTitle": "The Grand Budapest Hotel (2014)",
      "year": "2014",
      "image": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "866991"
    },
    {
      "id": "tt0052618",
      "rank": "184",
      "title": "Ben-Hur",
      "fullTitle": "Ben-Hur (1959)",
      "year": "1959",
      "image": "https://m.media-amazon.com/images/M/MV5BNjgxY2JiZDYtZmMwOC00ZmJjLWJmODUtMTNmNWNmYWI5ODkwL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "249527"
    },
    {
      "id": "tt0015864",
      "rank": "185",
      "title": "The Gold Rush",
      "fullTitle": "The Gold Rush (1925)",
      "year": "1925",
      "image": "https://m.media-amazon.com/images/M/MV5BZjEyOTE4MzMtNmMzMy00Mzc3LWJlOTQtOGJiNDE0ZmJiOTU4L2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_Ratio0.7343_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "116648"
    },
    {
      "id": "tt2267998",
      "rank": "186",
      "title": "Gone Girl",
      "fullTitle": "Gone Girl (2014)",
      "year": "2014",
      "image": "https://m.media-amazon.com/images/M/MV5BMTk0MDQ3MzAzOV5BMl5BanBnXkFtZTgwNzU1NzE3MjE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "1041426"
    },
    {
      "id": "tt0072684",
      "rank": "187",
      "title": "Barry Lyndon",
      "fullTitle": "Barry Lyndon (1975)",
      "year": "1975",
      "image": "https://m.media-amazon.com/images/M/MV5BNmY0MWY2NDctZDdmMi00MjA1LTk0ZTQtZDMyZTQ1NTNlYzVjXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "178851"
    },
    {
      "id": "tt2119532",
      "rank": "188",
      "title": "Hacksaw Ridge",
      "fullTitle": "Hacksaw Ridge (2016)",
      "year": "2016",
      "image": "https://m.media-amazon.com/images/M/MV5BMjQ1NjM3MTUxNV5BMl5BanBnXkFtZTgwMDc5MTY5OTE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "575455"
    },
    {
      "id": "tt0107207",
      "rank": "189",
      "title": "In the Name of the Father",
      "fullTitle": "In the Name of the Father (1993)",
      "year": "1993",
      "image": "https://m.media-amazon.com/images/M/MV5BMmYyOTgwYWItYmU3Ny00M2E2LTk0NWMtMDVlNmQ0MWZiMTMxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "183956"
    },
    {
      "id": "tt0047296",
      "rank": "190",
      "title": "On the Waterfront",
      "fullTitle": "On the Waterfront (1954)",
      "year": "1954",
      "image": "https://m.media-amazon.com/images/M/MV5BY2I0MWFiZDMtNWQyYy00Njk5LTk3MDktZjZjNTNmZmVkYjkxXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "161848"
    },
    {
      "id": "tt0353969",
      "rank": "191",
      "title": "Memories of Murder",
      "fullTitle": "Memories of Murder (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BOGViNTg4YTktYTQ2Ni00MTU0LTk2NWUtMTI4OTc1YTM0NzQ2XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "207181"
    },
    {
      "id": "tt0017925",
      "rank": "192",
      "title": "The General",
      "fullTitle": "The General (1926)",
      "year": "1926",
      "image": "https://m.media-amazon.com/images/M/MV5BYmRiMDFlYjYtOTMwYy00OGY2LWE0Y2QtYzQxOGNhZmUwNTIxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "96382"
    },
    {
      "id": "tt0077416",
      "rank": "193",
      "title": "The Deer Hunter",
      "fullTitle": "The Deer Hunter (1978)",
      "year": "1978",
      "image": "https://m.media-amazon.com/images/M/MV5BNDhmNTA0ZDMtYjhkNS00NzEzLWIzYTItOGNkMTVmYjE2YmI3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "355448"
    },
    {
      "id": "tt3011894",
      "rank": "194",
      "title": "Wild Tales",
      "fullTitle": "Wild Tales (2014)",
      "year": "2014",
      "image": "https://m.media-amazon.com/images/M/MV5BNGQzY2Y0MTgtMDA4OC00NjM3LWI0ZGQtNTJlM2UxZDQxZjI0XkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_Ratio0.7150_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "211558"
    },
    {
      "id": "tt0050986",
      "rank": "195",
      "title": "Wild Strawberries",
      "fullTitle": "Wild Strawberries (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BYWQxYzdhMDMtNjAyZC00NzE0LWFjYmQtYjk0YzMyYjA5NzZkXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "112841"
    },
    {
      "id": "tt0097165",
      "rank": "196",
      "title": "Dead Poets Society",
      "fullTitle": "Dead Poets Society (1989)",
      "year": "1989",
      "image": "https://m.media-amazon.com/images/M/MV5BOGYwYWNjMzgtNGU4ZC00NWQ2LWEwZjUtMzE1Zjc3NjY3YTU1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "528694"
    },
    {
      "id": "tt0041959",
      "rank": "197",
      "title": "The Third Man",
      "fullTitle": "The Third Man (1949)",
      "year": "1949",
      "image": "https://m.media-amazon.com/images/M/MV5BYjE2OTdhMWUtOGJlMy00ZDViLWIzZjgtYjZkZGZmMDZjYmEyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "178932"
    },
    {
      "id": "tt0046268",
      "rank": "198",
      "title": "The Wages of Fear",
      "fullTitle": "The Wages of Fear (1953)",
      "year": "1953",
      "image": "https://m.media-amazon.com/images/M/MV5BZDdkNzMwZmUtY2Q5MS00ZmM2LWJhYjItYTBjMWY0MGM4MDRjXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "65045"
    },
    {
      "id": "tt1392190",
      "rank": "199",
      "title": "Mad Max: Fury Road",
      "fullTitle": "Mad Max: Fury Road (2015)",
      "year": "2015",
      "image": "https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "1057898"
    },
    {
      "id": "tt0015324",
      "rank": "200",
      "title": "Sherlock Jr.",
      "fullTitle": "Sherlock Jr. (1924)",
      "year": "1924",
      "image": "https://m.media-amazon.com/images/M/MV5BZWFhOGU5NDctY2Q3YS00Y2VlLWI1NzEtZmIwY2ZiZjY4OTA2XkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "54991"
    },
    {
      "id": "tt0198781",
      "rank": "201",
      "title": "Monsters, Inc.",
      "fullTitle": "Monsters, Inc. (2001)",
      "year": "2001",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY1NTI0ODUyOF5BMl5BanBnXkFtZTgwNTEyNjQ0MDE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "958023"
    },
    {
      "id": "tt0031679",
      "rank": "202",
      "title": "Mr. Smith Goes to Washington",
      "fullTitle": "Mr. Smith Goes to Washington (1939)",
      "year": "1939",
      "image": "https://m.media-amazon.com/images/M/MV5BZTYwYjYxYzgtMDE1Ni00NzU4LWJlMTEtODQ5YmJmMGJhZjI5L2ltYWdlXkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "119746"
    },
    {
      "id": "tt0073195",
      "rank": "203",
      "title": "Jaws",
      "fullTitle": "Jaws (1975)",
      "year": "1975",
      "image": "https://m.media-amazon.com/images/M/MV5BMmVmODY1MzEtYTMwZC00MzNhLWFkNDMtZjAwM2EwODUxZTA5XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "646248"
    },
    {
      "id": "tt0892769",
      "rank": "204",
      "title": "How to Train Your Dragon",
      "fullTitle": "How to Train Your Dragon (2010)",
      "year": "2010",
      "image": "https://m.media-amazon.com/images/M/MV5BMjA5NDQyMjc2NF5BMl5BanBnXkFtZTcwMjg5ODcyMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "782442"
    },
    {
      "id": "tt0978762",
      "rank": "205",
      "title": "Mary and Max",
      "fullTitle": "Mary and Max (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BMDgzYjQwMDMtNGUzYi00MTRmLWIyMGMtNjE1OGZkNzY2YWIzL2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.7053_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "184232"
    },
    {
      "id": "tt1950186",
      "rank": "206",
      "title": "Ford v Ferrari",
      "fullTitle": "Ford v Ferrari (2019)",
      "year": "2019",
      "image": "https://m.media-amazon.com/images/M/MV5BM2UwMDVmMDItM2I2Yi00NGZmLTk4ZTUtY2JjNTQ3OGQ5ZjM2XkEyXkFqcGdeQXVyMTA1OTYzOTUx._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "445529"
    },
    {
      "id": "tt0050976",
      "rank": "207",
      "title": "The Seventh Seal",
      "fullTitle": "The Seventh Seal (1957)",
      "year": "1957",
      "image": "https://m.media-amazon.com/images/M/MV5BOWM3MmE0OGYtOGVlNC00OWE1LTk5ZTAtYmUwMDIwM2ZlNWJiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6860_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "194836"
    },
    {
      "id": "tt3170832",
      "rank": "208",
      "title": "Room",
      "fullTitle": "Room (2015)",
      "year": "2015",
      "image": "https://m.media-amazon.com/images/M/MV5BMjE4NzgzNzEwMl5BMl5BanBnXkFtZTgwMTMzMDE0NjE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "442104"
    },
    {
      "id": "tt0118715",
      "rank": "209",
      "title": "The Big Lebowski",
      "fullTitle": "The Big Lebowski (1998)",
      "year": "1998",
      "image": "https://m.media-amazon.com/images/M/MV5BMzliZDk0NjctNjhlOC00MWEyLWI3OWYtNjA5ZDYxMTMzNTc5XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "845332"
    },
    {
      "id": "tt0382932",
      "rank": "210",
      "title": "Ratatouille",
      "fullTitle": "Ratatouille (2007)",
      "year": "2007",
      "image": "https://m.media-amazon.com/images/M/MV5BMTMzODU0NTkxMF5BMl5BanBnXkFtZTcwMjQ4MzMzMw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "798702"
    },
    {
      "id": "tt0046438",
      "rank": "211",
      "title": "Tokyo Story",
      "fullTitle": "Tokyo Story (1953)",
      "year": "1953",
      "image": "https://m.media-amazon.com/images/M/MV5BYWQ4ZTRiODktNjAzZC00Nzg1LTk1YWQtNDFmNDI0NmZiNGIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "66609"
    },
    {
      "id": "tt0075148",
      "rank": "212",
      "title": "Rocky",
      "fullTitle": "Rocky (1976)",
      "year": "1976",
      "image": "https://m.media-amazon.com/images/M/MV5BNTBkMjg2MjYtYTZjOS00ODQ0LTg0MDEtM2FiNmJmOGU1NGEwXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "615602"
    },
    {
      "id": "tt0395169",
      "rank": "213",
      "title": "Hotel Rwanda",
      "fullTitle": "Hotel Rwanda (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BZGJjYmIzZmQtNWE4Yy00ZGVmLWJkZGEtMzUzNmQ4ZWFlMjRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "367662"
    },
    {
      "id": "tt3315342",
      "rank": "214",
      "title": "Logan",
      "fullTitle": "Logan (2017)",
      "year": "2017",
      "image": "https://m.media-amazon.com/images/M/MV5BYzc5MTU4N2EtYTkyMi00NjdhLTg3NWEtMTY4OTEyMzJhZTAzXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "811369"
    },
    {
      "id": "tt1895587",
      "rank": "215",
      "title": "Spotlight",
      "fullTitle": "Spotlight (2015)",
      "year": "2015",
      "image": "https://m.media-amazon.com/images/M/MV5BMjIyOTM5OTIzNV5BMl5BanBnXkFtZTgwMDkzODE2NjE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "493270"
    },
    {
      "id": "tt0091763",
      "rank": "216",
      "title": "Platoon",
      "fullTitle": "Platoon (1986)",
      "year": "1986",
      "image": "https://m.media-amazon.com/images/M/MV5BMzRjZjdlMjQtODVkYS00N2YzLWJlYWYtMGVlN2E5MWEwMWQzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "431393"
    },
    {
      "id": "tt0019254",
      "rank": "217",
      "title": "The Passion of Joan of Arc",
      "fullTitle": "The Passion of Joan of Arc (1928)",
      "year": "1928",
      "image": "https://m.media-amazon.com/images/M/MV5BNjBjNDJiYTUtOWY0OS00OGVmLTg2YzctMTE0NzVhODM1ZWJmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "59189"
    },
    {
      "id": "tt0088247",
      "rank": "218",
      "title": "The Terminator",
      "fullTitle": "The Terminator (1984)",
      "year": "1984",
      "image": "https://m.media-amazon.com/images/M/MV5BYTViNzMxZjEtZGEwNy00MDNiLWIzNGQtZDY2MjQ1OWViZjFmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "907101"
    },
    {
      "id": "tt15097216",
      "rank": "219",
      "title": "Jai Bhim",
      "fullTitle": "Jai Bhim (2021)",
      "year": "2021",
      "image": "https://m.media-amazon.com/images/M/MV5BNzFkM2FhMzQtYjUwZi00N2Y3LWFkZWItMmZmMjQxNGQwZmNhXkEyXkFqcGdeQXVyODEyNjEwMDk@._V1_Ratio0.8019_AL_.jpg",
      "crew": "",
      "imDbRating": "8.8",
      "imDbRatingCount": "212758"
    },
    {
      "id": "tt0381681",
      "rank": "220",
      "title": "Before Sunset",
      "fullTitle": "Before Sunset (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BMTQ1MjAwNTM5Ml5BMl5BanBnXkFtZTYwNDM0MTc3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "281831"
    },
    {
      "id": "tt1979320",
      "rank": "221",
      "title": "Rush",
      "fullTitle": "Rush (2013)",
      "year": "2013",
      "image": "https://m.media-amazon.com/images/M/MV5BOWEwODJmZDItYTNmZC00OGM4LThlNDktOTQzZjIzMGQxODA4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "503703"
    },
    {
      "id": "tt0074958",
      "rank": "222",
      "title": "Network",
      "fullTitle": "Network (1976)",
      "year": "1976",
      "image": "https://m.media-amazon.com/images/M/MV5BNzY0NjU5ODUtOTAzMC00NTU5LWJkZjctYWMyOWY2MTZmOWM1XkEyXkFqcGdeQXVyMTI3ODAyMzE2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "167025"
    },
    {
      "id": "tt0070047",
      "rank": "223",
      "title": "The Exorcist",
      "fullTitle": "The Exorcist (1973)",
      "year": "1973",
      "image": "https://m.media-amazon.com/images/M/MV5BYWFlZGY2NDktY2ZjOS00ZWNkLTg0ZDAtZDY4MTM1ODU4ZjljXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "445436"
    },
    {
      "id": "tt0036868",
      "rank": "224",
      "title": "The Best Years of Our Lives",
      "fullTitle": "The Best Years of Our Lives (1946)",
      "year": "1946",
      "image": "https://m.media-amazon.com/images/M/MV5BY2RmNTRjYzctODI4Ni00MzQyLWEyNTAtNjU0N2JkMTNhNjJkXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "69046"
    },
    {
      "id": "tt0092005",
      "rank": "225",
      "title": "Stand by Me",
      "fullTitle": "Stand by Me (1986)",
      "year": "1986",
      "image": "https://m.media-amazon.com/images/M/MV5BODJmY2Y2OGQtMDg2My00N2Q3LWJmZTUtYTc2ODBjZDVlNDlhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "431365"
    },
    {
      "id": "tt0113247",
      "rank": "226",
      "title": "La haine",
      "fullTitle": "La haine (1995)",
      "year": "1995",
      "image": "https://m.media-amazon.com/images/M/MV5BOTQxOGU0OWUtMzExYy00ZjIxLWJmMzAtNTI1Y2YxYTMxN2RkXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "190112"
    },
    {
      "id": "tt0325980",
      "rank": "227",
      "title": "Pirates of the Caribbean: The Curse of the Black Pearl",
      "fullTitle": "Pirates of the Caribbean: The Curse of the Black Pearl (2003)",
      "year": "2003",
      "image": "https://m.media-amazon.com/images/M/MV5BNGYyZGM5MGMtYTY2Ni00M2Y1LWIzNjQtYWUzM2VlNGVhMDNhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "1184568"
    },
    {
      "id": "tt0032138",
      "rank": "228",
      "title": "The Wizard of Oz",
      "fullTitle": "The Wizard of Oz (1939)",
      "year": "1939",
      "image": "https://m.media-amazon.com/images/M/MV5BNjUyMTc4MDExMV5BMl5BanBnXkFtZTgwNDg0NDIwMjE@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "420109"
    },
    {
      "id": "tt0317705",
      "rank": "229",
      "title": "The Incredibles",
      "fullTitle": "The Incredibles (2004)",
      "year": "2004",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY5OTU0OTc2NV5BMl5BanBnXkFtZTcwMzU4MDcyMQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8",
      "imDbRatingCount": "787464"
    },
    {
      "id": "tt0758758",
      "rank": "230",
      "title": "Into the Wild",
      "fullTitle": "Into the Wild (2007)",
      "year": "2007",
      "image": "https://m.media-amazon.com/images/M/MV5BNjQ0ODlhMWUtNmUwMS00YjExLWI4MjQtNjVmMmE2Y2E0MGRmXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "647523"
    },
    {
      "id": "tt1028532",
      "rank": "231",
      "title": "Hachi: A Dog's Tale",
      "fullTitle": "Hachi: A Dog's Tale (2009)",
      "year": "2009",
      "image": "https://m.media-amazon.com/images/M/MV5BYmQzYjgyYzEtOTVhZC00MDRkLWJjNjItYzU3N2RiMTExZjA1XkEyXkFqcGdeQXVyMTcwOTQzOTYy._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "303934"
    },
    {
      "id": "tt0035446",
      "rank": "232",
      "title": "To Be or Not to Be",
      "fullTitle": "To Be or Not to Be (1942)",
      "year": "1942",
      "image": "https://m.media-amazon.com/images/M/MV5BYTIwNDcyMjktMTczMy00NDM5LTlhNDEtMmE3NGVjOTM2YjQ3XkEyXkFqcGdeQXVyNjc0MzMzNjA@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "41565"
    },
    {
      "id": "tt4016934",
      "rank": "233",
      "title": "The Handmaiden",
      "fullTitle": "The Handmaiden (2016)",
      "year": "2016",
      "image": "https://m.media-amazon.com/images/M/MV5BNDJhYTk2MTctZmVmOS00OTViLTgxNjQtMzQxOTRiMDdmNGRjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "165818"
    },
    {
      "id": "tt0476735",
      "rank": "234",
      "title": "My Father and My Son",
      "fullTitle": "My Father and My Son (2005)",
      "year": "2005",
      "image": "https://m.media-amazon.com/images/M/MV5BNzEzMWYyYjEtNmVjZS00YTAyLWIyOTgtMzEzNzQxMTQzZTgwXkEyXkFqcGdeQXVyMTA0MTM5NjI2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "90564"
    },
    {
      "id": "tt0107048",
      "rank": "235",
      "title": "Groundhog Day",
      "fullTitle": "Groundhog Day (1993)",
      "year": "1993",
      "image": "https://m.media-amazon.com/images/M/MV5BZWIxNzM5YzQtY2FmMS00Yjc3LWI1ZjUtNGVjMjMzZTIxZTIxXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8",
      "imDbRatingCount": "668519"
    },
    {
      "id": "tt0058946",
      "rank": "236",
      "title": "The Battle of Algiers",
      "fullTitle": "The Battle of Algiers (1966)",
      "year": "1966",
      "image": "https://m.media-amazon.com/images/M/MV5BN2M4YTA4ZTEtN2EyNy00YTlmLWE4YzYtYjYyYjRkMWM4ZDM0XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "64291"
    },
    {
      "id": "tt0032551",
      "rank": "237",
      "title": "The Grapes of Wrath",
      "fullTitle": "The Grapes of Wrath (1940)",
      "year": "1940",
      "image": "https://m.media-amazon.com/images/M/MV5BNzJiOGI2MjctYjUyMS00ZjkzLWE2ZmUtOTg4NTZkOTNhZDc1L2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "98344"
    },
    {
      "id": "tt0245712",
      "rank": "238",
      "title": "Amores Perros",
      "fullTitle": "Amores Perros (2000)",
      "year": "2000",
      "image": "https://m.media-amazon.com/images/M/MV5BZjUxNmEwOGItMTBmYi00MWQ1LWExY2MtNDUxMjI0OWM4M2NiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "249861"
    },
    {
      "id": "tt0059742",
      "rank": "239",
      "title": "The Sound of Music",
      "fullTitle": "The Sound of Music (1965)",
      "year": "1965",
      "image": "https://m.media-amazon.com/images/M/MV5BNWFhNjg3YjctMjg2Ny00YjBkLTg5M2EtMTk2MjA1NDY3NzQ2XkEyXkFqcGdeQXVyMTA0MTM5NjI2._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "252107"
    },
    {
      "id": "tt0032976",
      "rank": "240",
      "title": "Rebecca",
      "fullTitle": "Rebecca (1940)",
      "year": "1940",
      "image": "https://m.media-amazon.com/images/M/MV5BYTcxYWExOTMtMWFmYy00ZjgzLWI0YjktNWEzYzJkZTg0NDdmL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6957_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "144102"
    },
    {
      "id": "tt0061512",
      "rank": "241",
      "title": "Cool Hand Luke",
      "fullTitle": "Cool Hand Luke (1967)",
      "year": "1967",
      "image": "https://m.media-amazon.com/images/M/MV5BNjcwNTQ3Y2EtMjdmZi00ODBhLWFhNzQtOTc3MWU5NTZlMDViXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "185779"
    },
    {
      "id": "tt0129167",
      "rank": "242",
      "title": "The Iron Giant",
      "fullTitle": "The Iron Giant (1999)",
      "year": "1999",
      "image": "https://m.media-amazon.com/images/M/MV5BYzBjZTNkMzQtZmNkOC00Yzk0LTljMjktZjk3YWVlZjY3NTk2XkEyXkFqcGdeQXVyMTUzMDUzNTI3._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "219362"
    },
    {
      "id": "tt0048473",
      "rank": "243",
      "title": "Pather Panchali",
      "fullTitle": "Pather Panchali (1955)",
      "year": "1955",
      "image": "https://m.media-amazon.com/images/M/MV5BMmFkNDY5OTktNzY3Yy00OTFlLThhNjktOTRhMmZjZmIxYjAxXkEyXkFqcGdeQXVyNTgyNTA4MjM@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.2",
      "imDbRatingCount": "37011"
    },
    {
      "id": "tt1454029",
      "rank": "244",
      "title": "The Help",
      "fullTitle": "The Help (2011)",
      "year": "2011",
      "image": "https://m.media-amazon.com/images/M/MV5BMTM5OTMyMjIxOV5BMl5BanBnXkFtZTcwNzU4MjIwNQ@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "483278"
    },
    {
      "id": "tt0025316",
      "rank": "245",
      "title": "It Happened One Night",
      "fullTitle": "It Happened One Night (1934)",
      "year": "1934",
      "image": "https://m.media-amazon.com/images/M/MV5BYzJmMWE5NjAtNWMyZS00NmFiLWIwMDgtZDE2NzczYWFhNzIzXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "109907"
    },
    {
      "id": "tt0053198",
      "rank": "246",
      "title": "The 400 Blows",
      "fullTitle": "The 400 Blows (1959)",
      "year": "1959",
      "image": "https://m.media-amazon.com/images/M/MV5BNzUwYzU2YjctOGM3YS00YjdiLTk1YjctZjdmMDY4ZTE1YWZkXkEyXkFqcGdeQXVyNzYxODE3NTQ@._V1_Ratio0.7536_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "125527"
    },
    {
      "id": "tt0103639",
      "rank": "247",
      "title": "Aladdin",
      "fullTitle": "Aladdin (1992)",
      "year": "1992",
      "image": "https://m.media-amazon.com/images/M/MV5BZTg5ZTVmM2EtZjdhZC00MzBjLWEwZTYtNWIwZDczYzZkMzA4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8",
      "imDbRatingCount": "454159"
    },
    {
      "id": "tt0099348",
      "rank": "248",
      "title": "Dances with Wolves",
      "fullTitle": "Dances with Wolves (1990)",
      "year": "1990",
      "image": "https://m.media-amazon.com/images/M/MV5BMTY3OTI5NDczN15BMl5BanBnXkFtZTcwNDA0NDY3Mw@@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8",
      "imDbRatingCount": "284217"
    },
    {
      "id": "tt0079470",
      "rank": "249",
      "title": "Life of Brian",
      "fullTitle": "Life of Brian (1979)",
      "year": "1979",
      "image": "https://m.media-amazon.com/images/M/MV5BMDA1ZWI4ZDItOTRlYi00OTUxLWFlNWQtMzM5NDI0YjA4ZGI2XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8",
      "imDbRatingCount": "417463"
    },
    {
      "id": "tt0060827",
      "rank": "250",
      "title": "Persona",
      "fullTitle": "Persona (1966)",
      "year": "1966",
      "image": "https://m.media-amazon.com/images/M/MV5BYmFlOTcxMWUtZTMzMi00NWIyLTkwOTEtNjIxNmViNzc2Yzc1XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_Ratio0.6763_AL_.jpg",
      "crew": "",
      "imDbRating": "8.1",
      "imDbRatingCount": "128173"
    }
  ]     