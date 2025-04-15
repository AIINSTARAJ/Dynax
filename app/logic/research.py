from bs4 import BeautifulSoup
import requests
import re
import base64
import json

def clean_categories(category_string):
    categories = category_string.split(';')
    
    clean_subjects = []
    for category in categories:
        if '(' in category:
            subject = category.split('(')[0].strip()
            clean_subjects.append(subject)
        else:
            clean_subjects.append(category.strip())

    return clean_subjects

def get_papers(topic:str,max=100,sort_by = ''):

    base_url = "https://arxiv.org/search/?"

    topic = topic.replace(" ","+")
    if sort_by == 'asc':
        sort = "announced_date_first"
    elif sort_by == 'desc':
        sort = "-announced_date_first"
    else:
        sort = ''

    param = f"searchtype=all&query={topic}&abstracts=show&size={max}&order={sort}"

    url = base_url + param

    response = requests.get(url)

    soup = BeautifulSoup(response.content,"html.parser")

    entries = soup.find_all('li',class_ = 'arxiv-result')

    Papers = []

    for entry in entries:
        abs_doi = entry.find("div", class_ = "is-marginless")

        field_attr = abs_doi.find('div', class_ = 'tags is-inline-block')
        fields = field_attr.find_all("span")
        field = [field.get("data-tooltip") for field in fields]

        doi_attr = abs_doi.find("a")
        doi:str = doi_attr.text.strip()

        url = doi_attr.get("href")
        pdf = f"https://arxiv.org/pdf/{doi.replace('arXiv:','')}"

        title = entry.find('p',class_ = "title is-5 mathjax").text.strip()

        auth_attr = entry.find_all('p', class_ = 'authors')
        authors = [author.find("a").text.strip() for author in auth_attr]

        abst_attr =  entry.find('p',class_ = "abstract mathjax")
        abst_elem = abst_attr.find('span', class_='abstract-full has-text-grey-dark mathjax')
        abstract = abst_elem.text.replace('△ Less', '').strip()

        date_elem = entry.find('p', class_='is-size-7')
        date_text = date_elem.text.strip()
        
        date_match = re.search(r'(\w+)\s+(\d{4})', date_text)
        if date_match:
            date = f"{date_match.group(1)} {date_match.group(2)}"
        else:
            date = date_text  
        
        paper = {
            'title' : title,
            'authors' : authors,
            'date' : date,
            'doi' : doi,
            'url': url,
            'pdf' : pdf,
            'abstract' : abstract,
            'field' : field
        }

        Papers.append(paper)
        
    return Papers

def get_doi(doi:str):
    
    base_url = "https://arxiv.org/search/?"

    param = f"searchtype=doi&query={doi}&abstracts=show"

    url = base_url + param

    response = requests.get(url)

    soup = BeautifulSoup(response.content,"html.parser")

    entry = soup.find("div",id = 'abs')

    date = entry.find('div',class_ = 'dateline').text.replace('Submitted on ','').replace('[','').replace(']','').strip()

    title = entry.find('h1',class_ = 'title mathjax').text.replace("Title:",'')

    url = f"'https://arxiv.org/abs/{doi.replace('arXiv:','')}"

    pdf = f"'https://arxiv.org/pdf/{doi.replace('arXiv:','')}"

    auth_attr = entry.find('div', class_ = 'authors')
    authors = [author.text.strip() for author in auth_attr.find_all('a')]

    abstract = entry.find('blockquote', class_ = 'abstract mathjax').text.replace('Abstract:','').strip()

    metadata = entry.find('div', class_= 'metatable')
    field = metadata.find('td', class_='tablecell subjects').text
    
    field = clean_categories(field)

    paper = {
        'title' : title,
        'authors' : authors,
        'date' : date,
        'url': url,
        'doi' : doi,
        'pdf' : pdf,
        'abstract' : abstract,
        'field' : field,
    }

    return paper

def encode_url(doi):
    encoded = base64.urlsafe_b64encode(doi.encode('utf-8')).decode('utf-8')
    encoded = encoded.rstrip('=')

    return encoded

def decode_url(encoded_doi):
    padding = len(encoded_doi) % 4
    
    if padding:
        encoded_doi += '=' * (4 - padding)
    
    try:
        decoded = base64.urlsafe_b64decode(encoded_doi).decode('utf-8')
        return decoded

    except Exception as e:
        return f"Error decoding: {str(e)}"

def add_link(papers_list, base_url="http://127.0.0.1:5425/paper/"):
    for paper in papers_list:
        if 'doi' in paper and paper['doi']:
            encoded_doi = encode_url(paper['doi'])
            paper['link'] = f"{base_url}{encoded_doi}"
    return papers_list
