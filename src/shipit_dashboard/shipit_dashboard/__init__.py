# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import os

from releng_common import auth, db, create_app
from shipit_dashboard.workflow import run_workflow
from shipit_dashboard.encoder import ShipitJSONEncoder


DEBUG = os.environ.get('DEBUG') == 'true' or __name__ == '__main__'
HERE = os.path.dirname(os.path.abspath(__file__))
APP_SETTINGS = os.path.abspath(os.path.join(HERE, '..', 'settings.py'))

import logging

if DEBUG:
    # Debug logging
    logging.basicConfig(level=logging.DEBUG)

def init_app(app):

    # Register extra commands
    app.cli.add_command(run_workflow)

    # Use custom json encoder
    app.json_encoder = ShipitJSONEncoder

    # Register swagger api
    return app.api.register(
        os.path.join(os.path.dirname(__file__), 'swagger.yml'))


if DEBUG and not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///%s' % (
        os.path.abspath(os.path.join(HERE, '..', 'app.db')))

if not os.environ.get('APP_SETTINGS') and \
       os.path.isfile(APP_SETTINGS):
    os.environ['APP_SETTINGS'] = APP_SETTINGS


app = create_app(
    "shipit_dashboard",
    extensions=[init_app, db, auth],
    debug=DEBUG,
    debug_src=HERE,
)

if __name__ == "__main__":
    app.run(**app.run_options())
