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

        for i in position:
            if '.' not in i:
                rank=rank+i
            else:
                break
        movie_rank.append(rank)

        title=tr.find('td',class_='titleColumn').a.get_text()
        movie_name.append(title)

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

scrabed=top_rated()
movie_dict={}
def group_by_year(movies):
    years=[]
    for i in movies:
        year=i['year']
        if year not in years:
            years.append(year)

    movie_dict={j:[]for j in years}

    for i in movies:
        year=i['year']

        for x in movie_dict:
            if str(x)==str(year):
                movie_dict[x].append(i)

    import json
    with open ('task2.json','w') as file:
        json.dump(movie_dict,file,indent=4)

    return movie_dict

print(group_by_year(scrabed))

# import json
# with open ('task2.json','w') as file:
#     json.dump(movie_dict,file,indent=4)


