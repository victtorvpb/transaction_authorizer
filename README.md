## Requirements

- [docker](https://docs.docker.com/get-docker/)
- [GNU make](https://www.gnu.org/software/make/)

or 
- [python 3.9](https://www.python.org/downloads/)

## Run with docker
1. ```make build```
2. ```make run input_file='input_file_path'```

## Run with python
```python transaction_authorizer.py < input_file_path```

## Run tests
1. ```make build```
2. ```make test ```

or  

``` python -m unittest discover -v -b```
