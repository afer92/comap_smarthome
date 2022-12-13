#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import httpx
import requests
from time import sleep
from datetime import datetime
import json
from threading import Lock
import asyncio
import logging

_CLIENT_ID = '56jcvrtejpracljtirq7qnob44'
_REGION_NAME = 'eu-west-3'
_BASE_URL = "https://api.comapsmarthome.com/"
_LOGGER = logging.getLogger(__name__)
_TOKEN_LOCK = Lock()


class ClientAuthx(object):
    client_id = _CLIENT_ID
    region_name = _REGION_NAME

    def __init__(self, username="", password=""):
        self._username = username
        self._password = password
        self._clientid = _CLIENT_ID
        self._login_headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "origin": "https://app.comapsmarthome.com",
            "referer": "https://app.comapsmarthome.com",
        }
        self._login_payload = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "AuthParameters": {
                "USERNAME": self._username,
                "PASSWORD": self._password,
            },
            "ClientId": self._clientid,
        }
        self._last_request = None
        self._token = None
        self._refresh_token = None
        self._token_expiration = None
        self._refresh_token_expiration = None
        self._login()

    @property
    def token(self):
        if time.time() > self._token_expires:
            self._refresh_current_token()
        return self._token

    def _login(self):
        try:
            url = "https://cognito-idp.eu-west-3.amazonaws.com"
            login_request = httpx.post(url, json=self._login_payload, headers=self._login_headers)
            login_request.raise_for_status()
            response = login_request.json()
            self._last_request = datetime.now()
            self._token = response.get("AuthenticationResult").get("AccessToken")
            self._refresh_token = response.get("AuthenticationResult").get("RefreshToken")
            self._token_expires = response.get("AuthenticationResult").get("ExpiresIn")

        except httpx.HTTPStatusError as err:
            _LOGGER.error('Could not set up COMAP client - %s status code. Check your credentials',
                          err.response.status_code)
            raise ComapClientAuthException("Client set up failed",
                                           err.response.status_code) from err

    def _get_new_token(self):
        self._login()

    def _refresh_current_token(self):
        url = "https://cognito-idp.eu-west-3.amazonaws.com"

        with _TOKEN_LOCK:
            headers = {
                "Content-Type": "application/x-amz-json-1.1",
                "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
                "origin": "https://app.comapsmarthome.com",
                "referer": "https://app.comapsmarthome.com",
            }
            payload = {
                "AuthFlow": "REFRESH_TOKEN_AUTH",
                "AuthParameters": {"REFRESH_TOKEN": self._refresh_token},
                "ClientId": self._clientid,
            }

            login_request = httpx.post(url, json=payload, headers=headers)
            if login_request.status_code == 200:
                response = login_request.json()
                self._last_request = datetime.now()
                self._token = response.get("AuthenticationResult").get("AccessToken")
                self._token_expires = response.get("AuthenticationResult").get("ExpiresIn")
            else:
                print(err)
                _LOGGER.error("Refresh token failed")


class ComapClientException(Exception):
    """Exception with ComapSmartHome client."""


class ComapClientAuthException(Exception):
    """Exception with ComapSmartHome client."""
