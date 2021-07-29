# noswear
A fast and simple library for detecting swear words

## Usage

`difficulty` and `path` are optional values.
`difficulty` is an int between `1` and `100`, the higer the value the harder to match the word.
```python
from noswear import noswear
noswear("string for checking", difficulty, path).getresult
```

## Full result
If the word is not detected the value from `fullresult` will be `None`.
```python
from noswear import noswear
noswear("string for checking", difficulty, path).fullresult
```
