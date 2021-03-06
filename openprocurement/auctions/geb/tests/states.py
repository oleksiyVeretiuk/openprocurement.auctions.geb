from copy import deepcopy

from openprocurement.auctions.geb.tests.fixtures.create import (
    CREATE_AUCTION_DEFAULT_FIXTURE as CREATE_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.draft import (
    AUCTION as DRAFT_AUCTION
)
from openprocurement.auctions.geb.tests.fixtures.active_rectification import (
    ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE,
    END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE
)
from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE,
    END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE,
    END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE
)
from openprocurement.auctions.geb.tests.fixtures.active_auction import (
    ACTIVE_AUCTION_DEFAULT_FIXTURE,
    END_AUCTION_AUCTION_DEFAULT_FIXTURE
)


class State(object):

    def context(self, fixture):
        context = {}

        # add auction context
        context['auction'] = {}
        context['auction']['data'] = {'id': fixture['_id']}
        context['auction']['access'] = {'owner': fixture['owner'],
                                        'token': fixture['owner_token']}
        context['questions'] = []
        questions = fixture.get('questions', None)
        if questions:
            for question in questions:
                info = {}
                info['data'] = {'id': question['id']}
                context['questions'].append(info)

        # add bids context
        context['bids'] = []
        bids = fixture.get('bids', None)
        if bids:
            for bid in bids:
                info = {}
                info['data'] = {'id': bid['id'],
                                'status': bid['status']}
                info['access'] = {'token': bid['owner_token'],
                                  'owner': bid['owner']}
                context['bids'].append(info)

        # add documents context
        context['documents'] = []
        documents = fixture.get('documents', None)
        if documents:
            for document in documents:
                info = {}
                info['data'] = {'id': document['id']}
                context['documents'].append(info)

        # add items context
        context['items'] = []
        items = fixture.get('items', None)
        if items:
            for item in items:
                info = {}
                info['data'] = deepcopy(item)
                context['items'].append(info)
        return context

# Auction States


class EndActiveAuction(State):
    fixture = END_AUCTION_AUCTION_DEFAULT_FIXTURE
    status = 'active.auction'


class ActiveAuction(State):
    fixture = ACTIVE_AUCTION_DEFAULT_FIXTURE
    status = 'active.auction'

    def context(self, fixture):
        context = {}
        context['auction'] = {}
        context['auction']['data'] = {'id': fixture['_id'],
                                      'value': fixture['value'],
                                      'minimalStep': fixture['value']}
        context['auction']['access'] = {'owner': fixture['owner'],
                                        'token': fixture['owner_token']}

        context['bids'] = []
        bids = fixture.get('bids', None)
        if bids:
            for bid in bids:
                info = {}
                info['data'] = {'id': bid['id'],
                                'status': bid['status']}
                info['access'] = {'token': bid['owner_token'],
                                  'owner': bid['owner']}
                context['bids'].append(info)

        return context

# Enquiry States


class EndActiveEnquiry(State):
    fixture = END_ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE
    status = 'active.enquiry'


class ActiveEnquiry(State):
    fixture = ACTIVE_ENQUIRY_AUCTION_DEFAULT_FIXTURE
    status = 'active.enquiry'

    def _next(self, end=False):
        return ActiveAuction() if not end else EndActiveEnquiry()

# Tendering States


class EndActiveTendering(State):
    fixture = END_ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE
    status = 'active.tendering'


class ActiveTendering(State):
    fixture = ACTIVE_TENDERING_AUCTION_DEFAULT_FIXTURE
    status = 'active.tendering'

    def _next(self, end=False):
        return ActiveEnquiry() if not end else EndActiveTendering()

# Rectification States


class EndActiveRectification(State):
    fixture = END_ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE
    status = 'active.rectification'


class ActiveRetification(State):
    fixture = ACTIVE_RECTIFICATION_AUCTION_DEFAULT_FIXTURE
    status = 'active.rectification'

    def _next(self, end=False):
        return ActiveTendering() if not end else EndActiveRectification()

# Draft States


class Draft(State):
    fixture = DRAFT_AUCTION
    status = 'draft'

    def _next(self, end=False):
        return ActiveRetification()


class Create(State):
    fixture = CREATE_AUCTION
    status = 'create'

    def context(self, fixture):
        context = {}
        context['auction'] = {}
        context['auction']['data'] = fixture
        return context

    def _next(self, end=False):
        return Draft()

# Machine


class ProcedureMachine(object):

    def __init__(self):
        self.state = Create()

    def __iter__(self):
        return self

    def _snapshot(self, dump, fixture):
        if dump:
            self._db.save(fixture)
        return self.state.context(fixture)

    def _next(self, end=False):
        self.state = self.state._next(end=end)

    def snapshot(self, dump=True, fixture=False):
        fixture = self.state.fixture if not fixture else fixture
        return self._snapshot(dump, fixture)

    def set_db_connector(self, db):
        self._db = db

    def next(self, end=False):
        try:
            self._next(end=end)
        except AttributeError:
            raise StopIteration
        return self.state

    def toggle(self, status, end=False):
        if self.state.status == status:
            return
        for state in self:
            if state.status == status:
                break
        if end:
            self.next(end=True)
