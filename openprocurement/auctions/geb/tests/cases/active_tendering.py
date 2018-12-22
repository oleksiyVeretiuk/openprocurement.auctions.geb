# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import (
    BaseWebTest,
)

from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationDocumentsWorkFlowMixin,
    BaseAdministratorTestMixin
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    AUCTION_WITH_BIDS_WITH_CANCELLATION,
    AUCTION_WITH_BID_ACTIVE,
    AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT,
    AUCTION_WITH_BID_DRAFT,
    AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT,
    AUCTION_WITH_BID_PENDING,
    AUCTION_WITH_BID_PENDING_WITH_DOCUMENT,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS,
    AUCTION_WITH_DOCUMENTS,
    AUCTION_WITH_QUESTIONS
)

from openprocurement.auctions.geb.tests.blanks.active_tendering import (
    auction_auction_get,
    auction_document_patch,
    auction_document_put,
    auction_document_post,
    auction_document_download,
    auction_document_post_offline,
    add_invalid_bid,
    add_question,
    add_question_to_item,
    answer_question,
    auction_change_fields,
    bid_add,
    bid_add_document_in_active_status,
    bid_document_put_without_ds,
    bid_document_post_without_ds,
    bid_add_document_in_draft_status,
    bid_add_document_in_pending_status,
    bid_delete_in_active_status,
    bid_delete_in_draft_status,
    bid_delete_in_pending_status,
    bid_get_in_active_status,
    bid_get_in_draft_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_make_pending,
    bid_patch_in_active_status,
    bid_patch_in_draft_status,
    bid_patch_in_pending_status,
    bid_patch_bid_number_invalid,
    bid_draft_get_document,
    bid_draft_patch_document,
    bid_pending_patch_document,
    bid_pending_get_document,
    bid_active_patch_document,
    bid_active_get_document,
    get_question,
    auction_document_post_without_ds,
    auction_document_put_without_ds
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class ActiveTenderingTest(BaseWebTest):
    docservice = True

    test_auction_document_post_offline = snitch(auction_document_post_offline)
    test_auction_document_post = snitch(auction_document_post)
    test_add_question = snitch(add_question)
    test_add_question_to_item = snitch(add_question_to_item)
    test_bid_add = snitch(bid_add)
    test_auction_auction_get = snitch(auction_auction_get)
    test_auction_change_fields = snitch(auction_change_fields)
    test_add_invalid_bid = snitch(add_invalid_bid)

    def setUp(self):
        super(ActiveTenderingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                          self.auction['access']['token'])
        entrypoints['get_auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


class ActiveTenderingDocumentWithoutDSTest(BaseWebTest):
    docservice = False
    test_auction_document_post_without_ds = snitch(auction_document_post_without_ds)
    test_auction_document_put_without_ds = snitch(auction_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                auction['access']['token'])

        entrypoints['document_patch'] = '/auctions/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                        document['data']['id'],
                                                                                        auction['access']['token'])

        entrypoints['document_get'] = '/auctions/{}/documents/{}'.format(auction['data']['id'],
                                                                         document['data']['id'])
        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingQuestionsTest(BaseWebTest):

    test_answer_question = snitch(answer_question)
    test_get_question = snitch(get_question)

    def setUp(self):
        super(ActiveTenderingQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_QUESTIONS)

        self.auction = context['auction']
        self.question = context['questions'][0]

        entrypoints = {}

        entrypoints['patch_question'] = '/auctions/{}/questions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                                        self.question['data']['id'],
                                                                                        self.auction['access']['token'])

        entrypoints['get_question'] = '/auctions/{}/questions/{}'.format(self.auction['data']['id'],
                                                                         self.question['data']['id'])

        self.ENTRYPOINTS = entrypoints


class ActiveTenderingDraftBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)
    test_bid_make_pending = snitch(bid_make_pending)
    test_bid_add_document_in_draft_status = snitch(bid_add_document_in_draft_status)
    test_bid_delete_in_draft_status = snitch(bid_delete_in_draft_status)
    test_bid_get_in_draft_status = snitch(bid_get_in_draft_status)
    test_bid_patch_in_draft_status = snitch(bid_patch_in_draft_status)

    def setUp(self):
        super(ActiveTenderingDraftBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingPendingBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_patch_bidNumber_invalid = snitch(bid_patch_bid_number_invalid)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_add_document_in_pending_status = snitch(bid_add_document_in_pending_status)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(ActiveTenderingPendingBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids'
        entrypoints['bid_post'] = pattern.format(auction=auction['data']['id'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingActiveBidsTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_add_document_in_active_status = snitch(bid_add_document_in_active_status)
    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(ActiveTenderingActiveBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingDraftBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_draft_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_draft_patch_document)
    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingDraftBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingPendingBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_pending_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_pending_patch_document)
    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveTenderingPendingBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingActiveBidsWithDocumentTest(BaseWebTest):

    test_bid_get_document_in_active_status = snitch(bid_active_get_document)
    test_bid_patch_document_in_active_status = snitch(bid_active_patch_document)

    def setUp(self):
        super(ActiveTenderingActiveBidsWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveTenderingDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_document_put = snitch(auction_document_put)
    test_auction_document_download = snitch(auction_document_download)

    def setUp(self):
        super(ActiveTenderingDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoints['document_patch'] = '/auctions/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                        document['data']['id'],
                                                                                        auction['access']['token'])

        entrypoints['document_get'] = '/auctions/{}/documents/{}'.format(auction['data']['id'],
                                                                         document['data']['id'])
        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveTenderingCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION)

        auction = context['auction']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])

        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        entrypoints['get_cancellation'] = '/auctions/{}/cancellations/{}'.format(auction['data']['id'],
                                                                                 cancellation['data']['id'])

        entrypoints['cancellation_document_post'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                  cancellation['data']['id'],
                                                                                                                  auction['access']['token'])
        entrypoints['get_cancellations_listing'] = '/auctions/{}/cancellations'.format(auction['data']['id'])

        self.auction = auction
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingWithBidsCancellationsTest(BaseWebTest):
    test_cancellation_make_active_clean_bids = snitch(cancellation_make_clean_bids)

    def setUp(self):
        super(ActiveTenderingWithBidsCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BIDS_WITH_CANCELLATION)

        auction = context['auction']
        bids = context['bids']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        self.auction = auction
        self.bids = bids
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveTenderingCancellationsDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('draft')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS)

        auction = context['auction']
        cancellation = context['cancellations'][0]
        document = cancellation['data']['documents'][0]
        documents = cancellation['data']['documents']

        entrypoints = {}
        entrypoints['cancellation_document_listing'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                     cancellation['data']['id'],
                                                                                                                     auction['access']['token'])

        entrypoints['cancellation_document'] = '/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                                cancellation['data']['id'],
                                                                                                                document['id'],
                                                                                                                auction['access']['token'])

        self.auction = auction
        self.cancellation = cancellation
        self.documents = documents
        self.ENTRYPOINTS = entrypoints


class ActiveTenderingAdministratorTest(BaseWebTest, BaseAdministratorTestMixin):

    def setUp(self):
        super(ActiveTenderingAdministratorTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_auction'] = '/auctions/{}'.format(auction['data']['id'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ActiveTenderingActiveBidsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingActiveBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingAdministratorTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingCancellationsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingDraftBidsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingDraftBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingPendingBidsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingPendingBidsWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingQuestionsTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingDocumentWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveTenderingWithBidsCancellationsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
