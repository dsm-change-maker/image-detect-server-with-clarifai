# image-detect-server with clarifai

A simple server that returns whether or not there are people in the image.

- [clarifai](https://www.clarifai.com/)

```
# install this server
$ git clone https://github.com/dsm-change-maker/image-detect-server.git
$ cd image-detect-server

# install dependency
$ pip3 install -r requirements.txt

# set the value CLARIFAI_API_KEY
$ export CLARIFAI_API_KEY={YOUR_CLARIFAI_API_KEY}

# run this server
$ python3 wsgi.py
# test request
$ curl -F 'file=@./test.jpg' 127.0.0.1:5000/upload
{"is_there_anyone":true}
```
