import requests
import time

from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger

import summarizer
from readability import Readable

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/summarize')
def summarize(url: str):
    logger.info(f'Summarizing : {url}')

    logger.info('Calling readability API')
    content = Readable(url)
    logger.info('Readability API call successful')

    article_content = content.article_content
    logger.debug(f'\nArticle content : {article_content}')
    soup = BeautifulSoup(article_content, 'lxml')
    text = soup.text
    logger.debug(f'\nArticle text : {text}')

    logger.info('Calling summarizer engine')
    summary = summarizer.summarize(text)
    '''
    summary = requests.get(SUMMARIZER_API, params={'text': text})
    if summary.status_code != 200:
        raise HTTPException(status_code=summary.status_code, detail=summary.text)
    '''
    logger.info('Summarizer engine call successful')
    logger.debug(f'\nSummary : {summary}')
    return {'summary': summary}


@app.get('/stream')
def _stream():
    def iter_text():
        text = '''A static library (also known as an archive) consists of routines that are compiled and linked directly into your program. When you compile a program that uses a static library, all the functionality of the static library that your program uses becomes part of your executable. On Windows, static libraries typically have a .lib extension, whereas on Linux, static libraries typically have an .a (archive) extension. One advantage of static libraries is that you only have to distribute the executable in order for users to run your program. Because the library becomes part of your program, this ensures that the right version of the library is always used with your program. Also, because static libraries become part of your program, you can use them just like functionality you’ve written for your own program. On the downside, because a copy of the library becomes part of every executable that uses it, this can cause a lot of wasted space. Static libraries also can not be upgraded easy -- to update the library, the entire executable needs to be replaced.'''

        for word in text.split():
            time.sleep(0.5)
            yield word

    return StreamingResponse(iter_text(), media_type='text/html')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=50501)
