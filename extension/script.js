async function getReadableVersion(url) {
    if (url === undefined) {
        return "No URL found"
    }
    const res = await fetch ('http://localhost:50501/summarize?url='+url)
    const record = await res.json()
    return record['summary']
}

async function* streamAsyncIterator(stream) {
    const reader = stream.getReader();

    try {
        while (true) {
            const {done, value} = await reader.read();
            if (done) return;
            let word = '';
            await value.forEach( x => { word += String.fromCharCode(parseInt(x)) });
            word += ' ';
            console.log(value);
            console.log(word);
            yield word
            //yield String.fromCharCode(value);
        }
    } finally {
        reader.releaseLock();
    }
}

async function getStream(url) {
    const res = await fetch ('http://localhost:50501/stream')
    for await (const chunk of streamAsyncIterator(res.body)) {
        document.getElementById('summary').innerHTML += chunk;
        //console.log(chunk)
    }
}


chrome.tabs.query({currentWindow: true, active: true}, async function(tabs) {
    await getStream(tabs[0].url)
    //document.getElementById('summary').innerHTML = await getReadableVersion(tabs[0].url)
});
