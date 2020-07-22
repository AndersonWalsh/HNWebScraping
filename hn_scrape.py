import requests
from bs4 import BeautifulSoup
import pprint
import sys


def getPages(numpages):
    html = list()
    res = requests.get(('https://news.ycombinator.com/'))
    html.append(BeautifulSoup(res.text, 'html.parser'))
    for pagenum in range(2, numpages+1):
        res = requests.get(
            'https://news.ycombinator.com/news?p=' + f'{pagenum}')
        html.append(BeautifulSoup(res.text, 'html.parser'))
    return html


def sortStories(hn):
    return sorted(hn, key=lambda k: k['votes'], reverse=True)


def customHN(links, subtext, req_upvotes):
    hn = list()
    for i, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[i].select('.score')
        if len(vote):
            upvotes = int(vote[0].getText().replace(' points', ''))
            if upvotes >= req_upvotes:
                hn.append({'title': title, 'link': href, 'votes': upvotes})
    return hn


def main():
    try:
        html = getPages(int(sys.argv[1]))
        stories = list()
        links = [link.select('.storylink') for link in html]
        subtexts = [subtext.select('.subtext') for subtext in html]
        for i in range(len(links)):
            stories.append(customHN(links[i], subtexts[i], int(sys.argv[2])))
        flat_stories = [links for page in stories for links in page]
        pprint.pprint(sortStories(flat_stories))
    except IndexError as err:
        print(
            'Need num pages and requisite upvotes as command line arguments, in that order')
        raise err


if __name__ == '__main__':
    main()
