# recipe

Clone this repo: follow instructions on https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

Make sure you have python installed

Then install Flask:

```sh
pip install flask
```


In your browser navigate to 
```sh
http://127.0.0.1:5000
```

You Should see:

"Hello World!"


install recipe scrapers:
```sh
python3 -m pip install recipe-scrapers
```

if you get error about libressl
run 
```sh
brew install openssl@1.1
python3 -m pip install urllib3==1.26.6
```