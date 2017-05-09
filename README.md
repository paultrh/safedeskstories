# safedesk-stories
Stories generation

## Requirements
- Python 3
- pip3

## Dependencies

- Faker, used to generate fake data

```sh
$ pip install faker
$ pip install graphviz
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
$ python3 csv_parser.py
```

## Information

### csv_parser
The script parse all the csv file under the inputs directory and analyse.
If their are suitable to generate stories they will be integrated to the scenario.

## TODO

- More modular
- Link generation to stories
- Verify stories dependance
- Add image in generation
- Generate quest that will generate stories with from a complexity indicator
- Generation from csv file
