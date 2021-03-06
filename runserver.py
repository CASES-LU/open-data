#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Stats service API for MONARC
# Copyright (C) 2020-2021 Cédric Bonhomme - https://www.cedricbonhomme.org
# Copyright (C) 2020-2021 SMILE gie securitymadein.lu
#
# For more information: https://github.com/monarc-project/stats-api/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from statsservice.bootstrap import application
from statsservice.commands import (
    db_empty,
    db_create,
    db_init,
    client_create,
    stats_pull
)


def register_commands(app):
    """Register Click commands."""
    # database
    app.cli.add_command(db_empty)
    app.cli.add_command(db_create)
    app.cli.add_command(db_init)
    # client
    app.cli.add_command(client_create)
    app.cli.add_command(stats_pull)


with application.app_context():

    register_commands(application)


def run():
    application.run(
        host=application.config["HOST"],
        port=application.config["PORT"],
        debug=application.config["DEBUG"],
    )


if __name__ == "__main__":
    run()
