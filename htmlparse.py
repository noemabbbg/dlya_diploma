import requests
from bs4 import BeautifulSoup
from downloader import P
from urllib.parse import urlparse
url = "https://mangalib.me/kaeseul/"
async def propsParse(url):
    parsed_url = urlparse(url)
    # Split the path by '/' and only take the first two elements
    new_path = '/'.join(parsed_url.path.split('/')[:2])
    new_url = f'{parsed_url.scheme}://{parsed_url.netloc}{new_path}/'
    print(new_url)



    response = requests.get(new_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Get description
    description_tag = soup.find('meta', {'itemprop': 'description'})

    # Get media tags
    media_tags = soup.find_all(class_="media-tag-item", limit = 3)

    # Get release year, status, and number of chapters
    release_year_tag = soup.find('div', text='Год релиза').find_next_sibling()
    status_tag = soup.find('div', text='Статус тайтла').find_next_sibling()
    chapters_tag = soup.find('div', text='Загружено глав').find_next_sibling()

    # Get main name
    main_name_tag = soup.find('div', {'class': 'media-name__main'})

    title_picture_tag = soup.find('div', {'class': 'media-sidebar__cover paper'}).find('img')
    if title_picture_tag:
        title_picture_url = title_picture_tag.get('src')
        P.title_picture = title_picture_url
    print("Title Picture:", title_picture_url)


    if main_name_tag:
        P.u_name = main_name_tag.text
        
    # Print results
    if description_tag:
        description = description_tag.get('content')
        P.description = description
        print("Description:", description)

    if media_tags:
        print("Media Tags:")
        k = []
        for tag in media_tags:
            
            k.append(tag.text)
            
        P.genres = k

    if release_year_tag:
        P.release_year = release_year_tag.text
        print("Release Year:", release_year_tag.text)

    if status_tag:
        P.manhwa_state = status_tag.text
        print("Status:", status_tag.text)

    if chapters_tag:
        P.number_of_chapters = chapters_tag.text
        print("Chapters:", chapters_tag.text)

    



