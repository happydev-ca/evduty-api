# evduty-api
Library to communicate with EVduty REST API.

## Usage
```python
todo
```

## Development

### Setup
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Test
```bash
python3 -m unittest discover tests
```

### Build lib
```shell
python3 -m build
```

### Release version
```shell
#sed -i '' 's/z.z.z/x.x.x/g' pyproject.toml
#git tag x.x.x -a -m "x.x.x"
#git push --tags
```