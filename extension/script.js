async function getReadableVersion(url) {
    console.log(url)
    const res = await fetch ('http://localhost:50502/summarize?url='+url)
    const record = await res.json()
    console.log(record['summary'])

    document.getElementById('summary').innerHTML = record['summary']
}


chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
    await getReadableVersion(tabs[0].url)
});
