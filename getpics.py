import requests as req

def downloadImage(url):
    print(url)  
    try:    
        r = req.get(url, allow_redirects=True)
        open('%s'%url.split('/')[-1], 'wb').write(r.content)
    except Exception as e: print(e)


if __name__ == '__main__':
    downloadImage('https://www.tema.ru/crea-gif/go.gif')