## Create + activate virtual envirnment

1. `python3 -m venv venv`
1. `source venv/bin/activate`


## Running Locally

```sh
$ . venv/bin/activate
$ pip install -r requirements.txt
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku open
```

*Last info I got was*: `https://serene-caverns-82714.herokuapp.com/ | https://git.heroku.com/serene-caverns-82714.git`

or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
