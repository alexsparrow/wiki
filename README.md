# A simple filesystem-backed wiki using python3/aiohttp
I decided to use `python3`/`aiohttp` for this which turned out to be a bit of a waste of effort since Python's file operations are blocking.

To install the requirements:
```
pip install -r requirements.txt
```

To run the server:
```
PYTHONPATH=src python -m wiki.server
```

To run the tests:
```
PYTHONPATH=src pytest
```





