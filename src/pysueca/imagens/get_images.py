import contextlib
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

from rich.pretty import pprint

naipes = ('club', 'heart', 'spade', 'diamond',)
cartas = ('A', '7', 'K', 'J', 'Q', '6', '5', '4', '3', '2')


def make_request(url, headers=None):
    """
    https://realpython.com/urllib-request/
    :param url:
    :return:
    """
    request = Request(url, headers=headers or {})
    try:
        with urlopen(request, timeout=10) as response:
            return response.read()
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")


class URLImagesHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.images = []
        self.erro = 0

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        for attr in attrs:
            if attr[0] == 'src':
                url = attr[1]
                if 'upload' in url:
                    with contextlib.suppress(IndexError):
                        carta = url.split('_')[-1].split('.')[0]
                        naipe = url.split('_')[-2]
                        # if naipe == 'heart' and self.erro == 1:
                        #     url = url.replace(naipe, 'diamond')
                        #     naipe = 'diamond'
                        #     # https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Playing_card_diamond_A.svg/60px-Playing_card_diamond_A.svg.png
                        #     if carta == 'A':
                        #         url = url.replace('/5/', '/d/').replace('/57/', '/d3/')
                        #     elif carta == 'K':
                        #         url = url.replace('/5/', '/7/').replace('/8/', '/78/')
                        #     else:
                        #         url = url.replace('/5/', '/8/').replace('/57/', '/80/')
                        #     self.erro = 0
                        # elif naipe == 'heart' and self.erro == 0:
                        #     self.erro += 1
                        self.images.append( (carta, naipe, f'https:{url}') )

    def get_images(self):
        return self.images


def main():

    url_base = 'https://pt.wikibooks.org'
    url_jogo = '/wiki/Jogos_de_cartas/Sueca'

    body = make_request(f'{url_base}{url_jogo}')
    html = body.decode('utf-8')

    parser = URLImagesHTMLParser()
    parser.feed(html)

    url_imagens = parser.get_images()

    for url_imagem in url_imagens:
        naipe = url_imagem[0]
        carta = url_imagem[1]
        url = url_imagem[2]
        pprint([naipe, carta, url])
        response = make_request(url)

        with open(f'{naipe}_{carta}.png', 'wb') as imagem:
            if response:
                imagem.write(response)


if __name__ == '__main__':
    main()
