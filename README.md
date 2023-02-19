# Fun WebPage Summarizer

This will be a chrome extension that will summarize a webpage for you.


### ToDos

- [x] Add a popup to the chrome extension
- [x] On icon click 
  - [x] 1. Call the Readable API which takes in the URL to get the text
  - [x] 2. Call the Summarizer API which takes in the text from prev call as input to get the summary
- [x] Display the summary in the popup
- [ ] Stylize the output
- [ ] Host the backend engines on Cloud Run (Readable, Summarizer and the backend in this repo)
- [ ] Add caching and storage to the backend each individual engines can have their own DBs
