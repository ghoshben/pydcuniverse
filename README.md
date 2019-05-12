# pydcuniverse
Python library for interacting with DC Universe API

- [pydcuniverse](#pydcuniverse)
- [Usage](#usage)
  * [Getting product information](#getting-product-information)
    + [Example output](#example-output)
  * [Acquiring Widevine license](#acquiring-widevine-license)
- [Device IDs](#device-ids)
- [TODO](#todo)

# Usage

Initialize DCUClient class with an e-mail, password, device ID and proxies (optional):

```python
client = pydcuniverse.DCUClient(email, password, device_id, proxies)
```

## Getting product information

Using initialized class, request product information with:

```python
info = client.get_product_info(product_id)
```

Product ID can be found in the video URL. 
For example, product ID for `https://www.dcuniverse.com/videos/watch/house-of-el/e949dde5-400f-4aba-ac70-42d1bb009309` is `e949dde5-400f-4aba-ac70-42d1bb009309`.

### Example output
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

## Acquiring Widevine license

You can use this function to request an EME license for Widevine.

```python
license = client.acquire_license(challenge)
```

License and challenge are both base64 encoded strings.

# Device IDs
- `DA59dtVXYLxajktV`

# TODO
- [X] create setup.py
- [X] add to PyPI
- [ ] write unit tests
