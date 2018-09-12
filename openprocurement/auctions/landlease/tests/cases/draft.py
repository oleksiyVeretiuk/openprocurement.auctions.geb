# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.landlease.tests.base import (
    test_auction_data,
    BaseAuctionWebTest,
)

from openprocurement.auctions.landlease.tests.states import (
    Procedure
)

from openprocurement.auctions.landlease.tests.helpers import (
   get_procedure_state
)
from openprocurement.auctions.landlease.tests.blanks.draft import (
    phase_commit,
    change_forbidden_field_in_draft
)


class StatusDraftTest(BaseAuctionWebTest):
    initial_data = test_auction_data

    test_phase_commit = snitch(phase_commit)
    test_change_forbidden_field_in_draft = snitch(change_forbidden_field_in_draft)
    # TODO owners test

    def setUp(self):
        super(StatusDraftTest, self).setUp()

        procedure = Procedure(self.auction,
                              {"token": self.auction_token},
                              self)
        state = get_procedure_state(procedure, 'draft')
        self.auction = state.auction
        self.entrypoint = '/auctions/{}?acc_token={}'.format(self.auction_id,
                                                             self.auction_token)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StatusDraftTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')