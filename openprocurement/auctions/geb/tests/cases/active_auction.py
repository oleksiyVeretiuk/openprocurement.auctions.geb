# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.active_auction import (
    get_auction_auction,
    update_auction_urls,
    bring_auction_result
)


class StatusActiveAuctionTest(BaseWebTest):
    docservice = True
    test_get_auction_auction = snitch(get_auction_auction)
    test_update_auction_urls = snitch(update_auction_urls)
    test_bring_auction_result = snitch(bring_auction_result)

    def setUp(self):
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.auction')
        self.procedure = procedure

        entrypoints = {}

        self.ENTRYPOINTS = entrypoints
        self.app.authorization = ('Basic', ('auction', ''))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusActiveAuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
