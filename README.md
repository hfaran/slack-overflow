# slack-overflow

[![Build Status](https://travis-ci.org/hfaran/slack-overflow.svg?branch=develop)](https://travis-ci.org/hfaran/slack-overflow)
[![Coverage Status](https://coveralls.io/repos/hfaran/slack-overflow/badge.svg?branch=develop&service=github)](https://coveralls.io/github/hfaran/slack-overflow?branch=develop)

A programmer's best friend, now in Slack. Search StackOverflow right from Slack without coming off as dumb.

![](http://i.imgur.com/c9HuKw8.gif)


## Usage

### Top Questions

From any Slack channel, just type `/overflow [search terms]`. The questions will be shown on the same channel visible just to you.

### Top Answer

To get the top answer for a question, type `/soi [search terms]`. The answer
top answer for the top question will be fetched and rendered to you
in pristine\* Slack formatting.


## Integrate with your team

1. Go to your channel
2. Click on **Configure Integrations**.
3. Scroll all the way down to **DIY Integrations & Customizations section**.
4. Click on **Add** next to **Slash Commands**.
  - Command: `/overflow`
  - URL: `<URL of wherever you have deployed the app>`
  - Method: `POST`
  - For the **Autocomplete help text**, check to show the command in autocomplete list.
    - Description: `A programmer's best friend, now in Slack.`
    - Usage hint: `[search terms]`
  - Descriptive Label: `Search StackOverflow`

For integrating `/soi`, follow the same steps, but use `/soi` for the command
and URL route instead.

## Developing

* Grab your StackExchange key from http://stackapps.com/
* Provide the key by either setting the `SE_KEY` environment variable or
`--se-key` option

```python
# Install python dependencies
$ pip install -r requirements.txt

# Start the server
$ python app.py

# For more options:
$ python app.py --help
```

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

You will need to set the `SE_KEY` environment variable in your heroku app in order for this to work. You can read more about it [clicking here](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application)


## Contributing

- Please use the [issue tracker](https://github.com/hfaran/slack-overflow/issues) to report any bugs or file feature requests.
