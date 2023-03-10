import argparse
import os
import re
import torch

from nltk.tokenize import sent_tokenize
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


MAX_LEN_CHARS = int(os.environ['MAX_LEN_CHARS'])
MAX_NEW_TOKENS = int(os.environ['MAX_NEW_TOKENS'])
model_path = os.environ["MODEL_PATH"]

logger.info(f'Max Len Chars: {MAX_LEN_CHARS}')
logger.info(f'Max New Tokens: {MAX_NEW_TOKENS}')
logger.info(f'Model Path: {model_path}')

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
model.eval()
logger.info('Model loaded')
# summarizer_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)

app = FastAPI()

@app.get('/summarize')
def summarize_endpoint(text:str):
    try:
        return summarize(text)
    except IndexError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail='Index error while summarizing. In TODO to solve this.')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


def summarize(text: str):
    logger.info(f'Summarizing : {text}')
    preprocessed_text = preprocess(text)
    # The following code runs fine for most of the text but fails where we have one token per character and that seems to be the case for websites with lot of code. Because then it uses each space and new line and delimiter, everything as a separate token. This leads to an Index error while summarizing. So still need to solve that error. It depends on MAX_LEN_CHARS. The website content for which it fails is this:https://www.freecodecamp.org/news/building-chrome-extension/
    summary = []
    for chunk in get_chunks(preprocessed_text):
        summary.append(summarize_chunk(chunk))

    summary = ' '.join(summary)
    logger.info(f'Summary : {summary}')
    return summary


def preprocess(text: str):
    logger.info(f'Preprocessing text')
    # Using re replace all consecutive spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Using re replace all consecutive new lines with single new line
    text = re.sub(r'\n+', '\n', text)

    logger.info(f'Preprocessed text : {text}')
    return text



def summarize_chunk(text: str):
    inp = tokenizer(text, truncation=False, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(
            input_ids=inp['input_ids'],
            attention_mask=inp['attention_mask'],
            do_sample=False,
            num_beams=3,
            temperature=0.9,
            max_new_tokens=MAX_NEW_TOKENS,
        )
    return tokenizer.decode(out[0], skip_special_tokens=True)


def get_chunks(text: str):
    assert len(text) > 0, 'Text is empty'
    curr_size = 0
    chunks = [[]]
    for sent in sent_tokenize(text):
        if curr_size < MAX_LEN_CHARS:
            chunks[-1].append(sent)
            curr_size += len(sent)
        else:
            chunks[-1] = ' '.join(chunks[-1])
            chunks.append([])
            curr_size = 0
            
    if curr_size: chunks[-1] = ' '.join(chunks[-1])
    chunks = [c for c in chunks if len(c) > 0 and isinstance(c, str)]

    logger.info(f'Created {len(chunks)} chunks')
    return chunks


if __name__ == '__main__':
    logger.add('summarizer_engine.logs', format='{time} {level} {message}', level='INFO', rotation='1 MB')
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument('--reload', action='store_true')
    args = parser.parse_args()

    if args.reload:
        uvicorn.run('summarizer:app', host='127.0.0.1', port=50507, reload=True)
    else:
        uvicorn.run(app, host='0.0.0.0', port=int(os.environ['API_PORT']))
