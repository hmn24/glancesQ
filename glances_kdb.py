#
# Modified from https://github.com/nicolargo/glances/tree/develop/glances/exports
# for usage with kdb+ processes (publishing mechanism)
#
"""kdb+ interface class."""

import sys
from numbers import Number

from glances.logger import logger
from glances.exports.glances_export import GlancesExport
from glances.compat import iteritems, listkeys, listvalues

import numpy as np

from qpython import qconnection
from qpython.qcollection import QDictionary, qlist
from qpython.qtype import QSYMBOL_LIST, QDOUBLE_LIST


class Export(GlancesExport):

    """This class manages the kdb+ export module."""

    def __init__(self, config=None, args=None):
        
        """Init the kdb+ export IF."""

        super(Export, self).__init__(config=config, args=args)

        # Mandatories configuration keys (additional to host and port)
        # Add config to /etc/glances/glances.conf
        # N/A

        # Optionals configuration keys
        self.prefix = None        
        self.username = None
        self.password = None

        # Load the kdb+ configuration file
        # Optional username/password
        self.export_enable = self.load_conf(
            "kdb", mandatories=["host", "port"], options=["username", "password"]
        )

        if not self.export_enable:
            sys.exit(2)

        # Default prefix for stats is 'glances'
        if self.prefix is None:
            self.prefix = "glances"

        # Init the kdb+ client
        self.client = self.init()

    def init(self):
        
        """Init the connection to the kdb+ server."""
        
        if not self.export_enable:
            return None

        try:
            q = qconnection.QConnection(
                host=self.host,
                port=int(self.port),
                username=self.username,
                password=self.password,
            )
            q.open()

        except Exception as e:
            logger.critical(
                f"Cannot connect to kdb+ server <{self.host}:{self.port}> ({e})"
            )
            sys.exit(2)

        return q

    def export(self, name, columns, points):

        """Export the stats to the kdb+ host/port."""

        # Remove non number stats and convert all numbers to float like prometheus
        data = {
            k:v
            for (k, v) in iteritems(dict(zip(columns, points)))
            if isinstance(v, Number)
        }

        # Append all tables name with self.prefix
        try:
            self.client.sendAsync(
                "{if[count z; x insert flip (`time, y)! .z.t, (),/: z]}",
                np.string_(f"{self.prefix}{name.capitalize()}"),
                qlist(listkeys(data), qtype=QSYMBOL_LIST),
                qlist(listvalues(data), qtype=QDOUBLE_LIST),
            )
        except Exception as e:
            logger.error(f"Cannot export stats <{name}> to kdb+ ({e})")

        logger.debug(f"Exported <{name}> stats to kdb+")

    def exit(self):
        
        """Close the kdb+ export module."""
        
        # Waits for all outstanding metrics to be sent and background thread closes
        self.client.close()
        
        # Call the father method
        super(Export, self).exit()
