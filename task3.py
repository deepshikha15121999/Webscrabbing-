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

scrapped=top_rated()

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

    return movie_dict

dec_arg=group_by_year(scrapped)


moviedec={}
def group_by_decade(movies):
   
    list1=[]
    
    for index in movies:  
        # index=int(index[1:5])
        index=int(index)
        mod=index%10
        decade=index-mod

        if decade not in list1:
            list1.append(decade)
    list1.sort()
    for i in list1:
        moviedec[i]=[]

    for i in moviedec:
        dec10=i+9

        for x in movies:
            if int(x)<=dec10 and int(x)>=i:
                for v in movies[x]:
                    moviedec[i].append(v)            
   

    import json
    with open ('task3.json','w') as file:
        json.dump(moviedec,file,indent=4)

    return moviedec
     

print(group_by_decade(dec_arg))