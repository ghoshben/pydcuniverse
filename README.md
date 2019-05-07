# pydcuniverse
Python library for interacting with DC Universe API

# Usage

Initialize DCUClient class with an e-mail, password, device ID and proxies (optional):

`client = pydcuniverse.DCUClient(email, password, dev, proxies)`

Using initialized class, request product information with:

`info = client.get_product_info(product_id)`

Product ID can be found in the video URL. 
For example, product ID for `https://www.dcuniverse.com/videos/watch/house-of-el/e949dde5-400f-4aba-ac70-42d1bb009309` is `e949dde5-400f-4aba-ac70-42d1bb009309`.

## Example output
```
{
    'asset_key': '5c993765',
    'description': 'Seg adjusts to a new life, a new rank, and a new threat.',
    'duration': '00:42:57',
    'episode': 2,
    'episode_title': 'House of El',
    'manifest': 'https://dc-c.dramafever.com/v11/e949dde5-400f-4aba-ac70-42d1bb009309/4382088986/dash/widevine/index.mpd',
    'name': 'Krypton',
    'season': 1
}
```

# Device IDs
- `DA59dtVXYLxajktV`

# TODO
- [X] create setup.py
- [ ] write unit tests
- [X] add to PyPI
