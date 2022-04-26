# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Grafana integration views """

from revproxy.views import ProxyView

class GrafanaProxyView(ProxyView):
    upstream = 'http://127.0.0.1:3000/'

    def get_proxy_request_headers(self, request):
        headers = super().get_proxy_request_headers(request)
        headers['X-WEBAUTH-USER'] = request.user.email
        return headers

