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

scrap=top_rated()

def scrap_movie_details(movie_url):
    
    page=requests.get(movie_url)
    soup=BeautifulSoup(page.text,'html.parser')
    title_div=soup.find('div',class_='sc-80d4314-1 fbQftq').h1.get_text() #movie name and year

    runtime=soup.find('ul',class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base").li.div.get_text()

    # runtime=sub_div.find('div',class_='ipc-metadata-list-item__content-container').get_text()

    runtime_hour=int(runtime[0])*60
    if 'minutes' in runtime:
        runtime_min=int(runtime[8:].strip('minutes'))
        movie_runtime=runtime_min+runtime_hour
    else:
        movie_runtime=runtime_hour

    g=soup.find('div',class_='ipc-chip-list__scroller')#scrapping the drama,romance etc
    u=g.find_all('span')
    gener=[]
    for i in u:
        gener.append(i.get_text())

    movie_bio=soup.find('div',class_='sc-16ede01-7 hrgVKw').get_text()   # summury of movie

    d=soup.find('li',class_='ipc-metadata-list__item').div.get_text()   #director name
    director=list(d.split(',')) # give split in list of director name

    # image link of the movie
    post=soup.find('div',class_='ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width sc-d383958-0 gvOdLN celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2').a['href']
    movie_poster='https://www.imdb.com'+post

    movie_dsetails_dic={'name':'','director':'','runtime':'','gener':'','poster_image':'','bio':''}

    movie_dsetails_dic['name']=title_div
    movie_dsetails_dic['director']=director
    movie_dsetails_dic['bio']=movie_bio
    movie_dsetails_dic['runtime']=runtime_hour
    movie_dsetails_dic['gener']=gener
    movie_dsetails_dic['poster_image']=movie_poster
   


    import json
    with open ('task4.json','w') as file:
        json.dump(movie_dsetails_dic,file,indent=4)

    return(movie_dsetails_dic)

url1='https://www.imdb.com/title/tt0367495/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=R4MS9GEQJ2KTG4P43H60&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_2print(scrap_movie_details(url1))'
print(scrap_movie_details(url1))

