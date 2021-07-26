# noswear
A fast and simple library for detecting swear words

## Usage

`sensitivity` and `path` are optional values.
`sensitivity` is an int between `1` and `100`
```python
from noswear import noswear
noswear("string for checking", sensitivity, path).getresult
```

## Full result
If the word is not detected the value from `fullresult` will be `None`.
```python
from noswear import noswear
noswear("string for checking", sensitivity, path).fullresult
```
