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

# Import errors are expected from pylint here due to Django behaviour
# pylint: disable=import-error

"""Custom setup to add Google Oauth"""

import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from grafana_api.grafana_face import GrafanaFace

class Command(BaseCommand):
    """Custom setup to add google oauth"""

    help = "My custom startup command"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            type=str,
        )
        parser.add_argument(
            "email",
            type=str,
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", None)
        if not password:
            raise CommandError("Please set env var DJANGO_SUPERUSER_PASSWORD")

        try:
            # one-off user/admin initialisation
            api = GrafanaFace(auth=("admin", "admin"), host="localhost:3000")
            # Change password
            api.admin.change_user_password(1, password)
            api = GrafanaFace(auth=("admin", password), host="localhost:3000")
            user = api.admin.create_user(
                {
                    "name": username,
                    "email": email,
                    "login": username,
                    "password": password,
                    "OrgId": 1
                }
            )
            # Make user an admin
            api.admin.change_user_permissions(user.id, True)

            # Add Datasource for our own self
            api.datasource.create_datasource(
                {
                    "name": "default",
                    "type": "stackdriver",
                    "isDefault": True,
                    "access": "proxy",
                    "jsonData": {
                        "authenticationType": "gce",
                    }
                }
            )


        except Exception as err:
            raise CommandError("Initalization failed.") from err
