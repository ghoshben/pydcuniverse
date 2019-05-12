"""
Client module
Main module for DC Universe API requests
"""

import requests
import jwt
import logging
import base64


class DCUClient(object):
    """
    DCUClient class
    Main class for DC Universe API requests
    __init__:
    @param email: E-mail used for logging in.
    @param password: Password used for logging in.
    @param device_key: Device key used for logging in.
    @param proxies: Proxies used for requests, default none.
    @return: DCUClient object
    """

    def __init__(self, email: str, password: str, device_key: str, proxies: dict = {}):
        self.logger = logging.getLogger(__name__)
        self.email = email
        self.password = password
        self.device_key = device_key
        self.proxies = proxies
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.27 Safari/537.36"
        self.jwtoken, self.headers = self.login()

    def login(self) -> tuple:
        """Performs logging in requests."""
        url = "https://www.dcuniverse.com/api/users/login"
        payload = {
            "username": self.email,
            "password": self.password
        }
        request_headers = {
            'cookie': "",
            'x-consumer-key': self.device_key
        }
        req = requests.post(url=url, json=payload, headers=request_headers)
        if req.status_code == 201:
            data = req.json()['result']
            bearer = data['session_id']
            jwtoken = data['jwt']
            self.logger.info(f"Authorization token: {bearer}")
            cookies_dict = requests.utils.dict_from_cookiejar(req.cookies)
            cookies_list = [f"{name}={value}" for name, value in cookies_dict.items()]
            cookies_formatted = '; '.join(cookies_list)
            headers = {
                'cookie': cookies_formatted,
                'authorization': f"Token {bearer}",
                'x-consumer-key': self.device_key,
                'User-Agent': self.user_agent
            }
        else:
            self.logger.error(f"Error logging in! {req.status_code}")

        return jwtoken, headers

    def get_product_info(self, product_id: str) -> dict:
        """Returns metadata and manifest for a given product id."""
        premium_status = self._is_premium()
        if premium_status is True:
            self.logger.info("Account is premium, continuing...")
        else:
            self.logger.info("Account is not premium, continuing anyway...")

        metadata = self._get_metadata(product_id)
        manifest = self._get_manifest_url(product_id)

        product_info = {
            "name": metadata['series_title'],
            "season": metadata['season'],
            "episode": metadata['season_position'],
            "episode_title": metadata['title'],
            "duration": metadata['duration'],
            "description": metadata['description'],
            "asset_key": metadata['asset_key'],
            "manifest": manifest
        }

        return product_info

    def acquire_license(self, request_b64: str) -> str:
        """Returns widevine license for provided request."""
        url = "https://www.dcuniverse.com/wvd/modlicense"
        request_bytes = base64.b64decode(request_b64)
        req = requests.post(url=url, data=request_bytes, headers=self.headers)
        license_bytes = req.content
        license_b64 = base64.b64encode(license_bytes).decode("utf-8")
        if req.status_code == 200:
            self.logger.info("License accquired!")
        else:
            self.logger.error(f"License accquisition failed! {req.status_code}, {req.content}")

        return license_b64

    def _get_metadata(self, product_id: str) -> dict:
        """Returns metadata for a given product id."""
        url = f"https://www.dcuniverse.com/api/5/episode/{product_id}/?trans=en"
        req = requests.get(url=url, headers=self.headers)
        if req.status_code == 200:
            self.logger.info("Metadata accquired.")
        else:
            self.logger.error(f"Metadata accquisition failed! {req.status_code}, {req.text}")

        return req.json()

    def _get_manifest_url(self, product_id: str) -> str:
        """Return manifest for a given product id."""
        rights = self._get_content_rights(product_id)

        url = f"https://www.dcuniverse.com/api/5/1/video_manifest_from_jwt/"
        params = {
            "cdn": "cloudfront",
            "drm": "widevine",
            "st": "dash",
            "subs": "en",
            "token": rights,
            "trans": "en"
        }
        req = requests.get(url=url, params=params, headers=self.headers)
        if req.status_code == 200:
            data = req.json()
            self.logger.debug(data)
        else:
            self.logger.error(f"Failure! {req.status_code} {req.text}")

        return data['stream_url']

    def _get_content_rights(self, product_id: str) -> str:
        """Returns rights if user is allowed to access given product id."""
        url = f"https://www.dcuniverse.com/api/5/1/rights/episode/{product_id}?trans=en"
        req = requests.get(url=url, headers=self.headers)
        if req.status_code == 200:
            self.logger.info("Rights accquired!")
            token = req.text[1:-1]
        else:
            self.logger.error("You do not have rights to this content!")

        return token

    def _is_premium(self) -> bool:
        """Returns whether logged in user account is premium."""
        data = jwt.decode(self.jwtoken, verify=False)

        return data["is_premium"]

    def __repr__(self) -> str:
        return f"<DcuClient email={self.email}>"
