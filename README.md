# safedesk-stories
Stories generation

## Requirements
- Python 3
- pip3

## Dependencies

- Faker, used to generate fake data
- graphviz, generate graph to visualize complexity
- wikipedia, fetch content from wikipedia

```sh
$ pip install faker
$ pip install graphviz
$ pip install wikipedia
```
or
```sh
$ pip install -r requirements.txt
```


## Usage

Usefull command

```sh
$ python3 init.py
$ python3 relaunch.py
```
## API.IA

Right now only the contact stories works with the API.
The needed generated file too train the api are under the /api folder

## Information

### csv_parser

The script parse all the csv file under the inputs directory and analyse.
If their are suitable to generate stories they will be integrated to the scenario.


### SPAM GENERATION

SPAM file are store under the SPAM/ directory.
They follow the same pattern as every others emails.
The users taht sends the mail must be referenced in the SpamUser.config file

## TODO

- Optimize csv generating system (currently rewritting each time doc content)
- Add more obfuscation startegy
- Verify stories dependance
- Generate quest that will generate stories with from a complexity indicator
