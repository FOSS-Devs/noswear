# noswear
A fast and simple library for detecting swear words

## Usage
`similarity` and `path` are optional values.
```python
from noswear import noswear
noswear("string for checking", similarity, path).getresult
```

## Full result
If the word is not detected the value from `fullresult` will be `None`.
```python
from noswear import noswear
noswear("string for checking", similarity, path).fullresult
```
