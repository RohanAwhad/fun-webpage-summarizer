async function getReadableVersion(url) {
    if (url === undefined) {
        return "No URL found"
    }
    const res = await fetch ('http://localhost:50502/summarize?url='+url)
    const record = await res.json()
    return record['summary']
}


chrome.tabs.query({currentWindow: true, active: true}, async function(tabs) {
    document.getElementById('summary').innerHTML = await getReadableVersion(tabs[0].url)
});
