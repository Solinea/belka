# Copyright (c) 2013 Solinea, Inc. (ken@solinea.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

import belka.token as token
import belka.exception as exception


class TestToken(unittest.TestCase):

    def test_happy_headers(self):
        tenant = "1234"
        auth_token = "4321"
        happy_header = {'Accept': 'application/json',
                        'User-Agent': 'belka',
                        'X-Auth-Project-Id': '1234',
                        'X-Auth-Token': '4321'}
        self.assertEqual(happy_header, token.headers(auth_token, tenant))

    def test_none_headers_raise_error(self):
        self.assertRaises(exception.MissingTokenError,
                          token.headers, None, None)

    def test_environ_credentials(self):
        os.environ.update(dict(OS_USERNAME="billy"))
        os.environ.update(dict(OS_PASSWORD="12345"))
        os.environ.update(dict(OS_TENANT_NAME="openstack"))
        os.environ.update(dict(OS_AUTH_URL="http://example.com:5000/"))
        happy_creds = dict(username="billy", password="12345",
                           tenant_name="openstack",
                           auth_url="http://example.com:5000/")
        self.assertEqual(happy_creds, token.get_credentials(None))
