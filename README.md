# Deepgram
Simple API Server handling user audio projects

Assignment Details:

Build a simple API server to handle user audio projects. 
Your server should provide endpoints that allow a user to perform the following actions: 

1. POST raw audio data and store it
-- e.g. $ curl -X POST --data-binary @myfile.wav http://localhost/post

2. GET a list of stored files, GET the contet of stored files, and GET metadata of stored files, such as the duration of the audio
-- The GET endpoint(s) should accept a query parameter that allows the user to filter results. Results should be returned as JSON
-- e.g. $ curl http://localhost/download?name=myfile.wav
        $ curl http://localhost/list?maxduration=300
        # curl http://localhost/info?name=myfile.wav

When you arrive for your interview, we will ask you to present your code and elaborate on some of the design choices you've made, some of the things you would have done differently if you had more time, and some things you learned about libraries you used

Your code should MINIMALLY be able to handle the GET and POST requests described above. Additionally, here are some features and questions you might want to think about:

Features/Questions to think about:
-- How to handle user authenticaiton and data security?
-- How to build a simple browser UI to interfact with your API?
-- How do you want to store audio data? For the purposes of this interview, just keeping them in memory is fine, but how else would you want to keep and serve audio data?
-- How to handle data integrity? How to make sure that users can't break your API by uploading rogue text data? How to make sure the metadata you calculate is correct and not thrown off by unmet expectations on the backend?