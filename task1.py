import requests
from bs4 import BeautifulSoup

url='https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in'
re=requests.get(url)
new=re.content
soup=BeautifulSoup(new,'html.parser')


top_movies=[]
def top_rated():
    main_div=soup.find('div',class_='lister')
    tbody=main_div.find('tbody',class_='lister-list')
    trs=tbody.find_all('tr')
    # print(main_div)
    movie_rank=[]
    movie_name=[]
    movie_rate=[]
    movie_year=[]
    movie_url=[]
    for tr in trs:
        position=tr.find('td',class_='titleColumn').get_text().strip()
        rank=''
    #    print(position)
        for i in position:
            if '.' not in i:
                rank=rank+i
            else:
                break
        movie_rank.append(rank)

        title=tr.find('td',class_='titleColumn').a.get_text()
        movie_name.append(title)
        # print(movie_name)

        year=tr.find('td',class_='titleColumn').span.get_text()
        movie_year.append(year)

        rate=tr.find('td',class_='ratingColumn imdbRating').strong.get_text()
        movie_rate.append(rate)
        
        link=tr.find('td',class_='titleColumn').a['href']
        movie_link='https://www.imdb.com'+link
        movie_url.append(movie_link)

    details={'position':'','name':'','rate':'','url':'','year':''}
    for i in range(0,len(movie_rank)):
        details['position']=int(movie_rank[i])
        details['name']=str(movie_name[i])
        details['rate']=float(movie_rate[i])
        details['url']=(movie_url[i])
        movie_year[i]= movie_year[i][1:5]
        details['year']=(movie_year[i])

        top_movies.append(details.copy())
        # details={'position':'','name':'','rate':'','url':'','year':''}

        
    return top_movies

print(top_rated())

import json
with open ('task1.json','w') as file:
    json.dump(top_movies,file,indent=4)



# import requests
# from bs4 import BeautifulSoup

# url='https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in'
# re=requests.get(url)
# new=re.content
# soup=BeautifulSoup(new,'html.parser')


# scrab_movie=soup.find_all('td',class_='titleColumn')

# movies=[]
# for movie in scrab_movie:
#     movie=movie.get_text().strip().replace('\n','')
#     movie=movie.strip('')
    
#     movies.append(movie)
# # print(movies)

# scrab_rating=soup.find_all('td',class_='ratingColumn imdbRating')
# ratings=[]
# for rating in scrab_rating:
#     rating=rating.get_text().replace('\n','')
#     rating=rating.strip('')
#     ratings.append(rating)
# # print(ratings)


# scrab_year=soup.find_all('span',class_='secondaryInfo')
# years=[]
# for year in scrab_year:
#     year=year.get_text().replace('\n','')
#     year=year.strip('')
#     years.append(year)
# print(years)
