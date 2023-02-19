from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['OPTIONS', 'GET'],
    allow_headers=['*'],
)
READABLE_API = 'http://localhost:50501/convert'
SUMMARIZER_API = 'http://localhost:50507/summarize'

@app.get('/summarize')
def summarize(url: str):
    # Call the readable API and get article_content
    # Use beautiful soup lib to get the text from article_contanet
    # send the text to summarizer engine and get the summary
    # return the summary
    content = requests.get(READABLE_API, params={'url': url})
    if content.status_code != 200:
        raise HTTPException(status_code=content.status_code, detail=content.text)
    soup = BeautifulSoup(content.text, 'lxml')
    text = soup.get_text()
    summary = requests.get(SUMMARIZER_API, params={'text': text})
    if summary.status_code != 200:
        raise HTTPException(status_code=summary.status_code, detail=summary.text)
    return {'summary': summary.text}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=50502)