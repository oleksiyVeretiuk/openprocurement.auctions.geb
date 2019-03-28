from uuid import uuid4
from copy import deepcopy

from openprocurement.auctions.core.utils import (
    get_now,
    set_specific_hour
)

from openprocurement.auctions.geb.tests.fixtures.active_tendering import (
    END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS
)
from openprocurement.auctions.geb.tests.fixtures.questions import (
    QUESTION
)
from openprocurement.auctions.geb.tests.fixtures.cancellations import (
    CANCELLATION,
    CANCELLATION_WITH_DOCUMENTS
)
from openprocurement.auctions.geb.tests.fixtures.documents import (
    DOCUMENT,
    OFFLINE_DOCUMENT
)
from openprocurement.auctions.geb.tests.fixtures.bids import (
    BID_ACTIVE_FIRST,
    BID_ACTIVE_SECOND,
    BID_ACTIVE_FIRST_WITH_DOCUMENT,
    BID_DRAFT_WITH_DOCUMENT,
    BID_PENDING_FIRST,
    BID_PENDING_FIRST_WITH_DOCUMENT,
    BID_PENDING_SECOND,
)
from openprocurement.auctions.geb.tests.fixtures.calculator import (
    Calculator
)

now = get_now()
calculator = Calculator(now, 'enquiryPeriod', 'start')
auction = deepcopy(END_ACTIVE_TENDERING_AUCTION_WITH_TWO_BIDS)
auction['status'] = 'active.enquiry'
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["enquiryPeriod"] = {
                  "startDate": calculator.enquiryPeriod.startDate.isoformat(),
                  "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["next_check"] = calculator.enquiryPeriod.endDate.isoformat()
auction["date"] = calculator.auctionDate.date.isoformat()

# auction in 'active.enquiry' status.
# description:
# - has item
# - two bids in status 'active'
# - minNumberOfQualifiedBids = 2
# - value.amount = 100
# - minimalStep.amount = 42
# - owner = 'broker'
AUCTION = auction

# auction with questions fixture
auction = deepcopy(AUCTION)
auction['questions'] = [QUESTION]
AUCTION_WITH_QUESTIONS = auction

# auction with documents
auction = deepcopy(AUCTION)
auction['documents'] = [DOCUMENT]
AUCTION_WITH_DOCUMENTS = auction

# auction with offline_documents
auction = deepcopy(AUCTION)
auction['documents'] = [OFFLINE_DOCUMENT]
AUCTION_WITH_OFFLINE_DOCUMENTS = auction

# auction with bids

# auction with bid in 'pending'
auction = deepcopy(AUCTION)
auction['bids'] = [BID_PENDING_FIRST]
AUCTION_WITH_BID_PENDING = auction

# auction with bid in 'active'
auction = deepcopy(AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST]
AUCTION_WITH_BID_ACTIVE = auction

# auction with bid in 'draft' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_DRAFT_WITH_DOCUMENT]
AUCTION_WITH_BID_DRAFT_WITH_DOCUMENT = auction

# auction with bid in 'pending' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_PENDING_FIRST_WITH_DOCUMENT]
AUCTION_WITH_BID_PENDING_WITH_DOCUMENT = auction

# auction with bid in 'active' with document
auction = deepcopy(AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST_WITH_DOCUMENT]
AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT = auction

# auction in end 'active.enquiry' with two bid in status 'active'
enquiry_end = set_specific_hour(get_now(), 20)
calculator = Calculator(enquiry_end, 'enquiryPeriod', 'end')
auction = deepcopy(AUCTION)
auction['status'] = 'active.enquiry'
auction["rectificationPeriod"] = {
    "startDate": calculator.rectificationPeriod.startDate.isoformat(),
    "endDate": calculator.rectificationPeriod.endDate.isoformat()
}
auction["tenderPeriod"] = {
    "startDate": calculator.tenderPeriod.startDate.isoformat(),
    "endDate": calculator.tenderPeriod.endDate.isoformat()
}
auction["enquiryPeriod"] = {
    "startDate": calculator.enquiryPeriod.startDate.isoformat(),
    "endDate": calculator.enquiryPeriod.endDate.isoformat()
}
auction["auctionPeriod"] = {
    "startDate": calculator.auctionPeriod.startDate.isoformat()
}
auction["next_check"] = None
auction["date"] = calculator.auctionDate.date.isoformat()
END_ACTIVE_ENQUIRY_AUCTION = auction

# auction in end 'active.enquiry' with two bid in status 'pending'
# which will lead to the status 'unsuccessful' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_PENDING_FIRST, BID_PENDING_SECOND]
END_ACTIVE_ENQUIRY_UNSUCCESSFUL_NO_BIDS_ACTIVE = auction

# auction in end 'active.enquiry' with two bid in status 'pending'
# and minNumberOfQualifiedBids = 1
# which will lead to the status 'unsuccessful' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_PENDING_FIRST, BID_PENDING_SECOND]
auction['minNumberOfQualifiedBids'] = 1
END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_NO_ACTIVE_BIDS = auction

# auction in end 'active.enquiry' with two bid in status 'active'
# and minNumberOfQualifiedBids = 1
# which will lead to the status 'active.auction' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST, BID_ACTIVE_SECOND]
auction['minNumberOfQualifiedBids'] = 1
END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_1_WITH_2_ACTIVE_BIDS = auction

# auction in end 'active.enquiry' with 1 bid in status 'active'
# and minNumberOfQualifiedBids = 2
# which will lead to the status 'unsuccessful' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST]
auction['minNumberOfQualifiedBids'] = 2
END_ACTIVE_ENQUIRY_WITH_MIN_NUMBER_BID_2_WITH_1_ACTIVE_BID = auction

# auction in end 'active.enquiry' with two bid in status 'active'
# and minNumberOfQualifiedBids = 1
# which will lead to the status 'active.qualification' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_ACTIVE_FIRST]
auction['minNumberOfQualifiedBids'] = 1
END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION = auction

# auction in end 'active.enquiry' with first bid in status 'unsuccessful' and second bid in 'active'
# and minNumberOfQualifiedBids = 1
# which will lead to the status 'active.qualification' auction
auction = deepcopy(END_ACTIVE_ENQUIRY_AUCTION)
auction['bids'] = [BID_PENDING_FIRST, BID_ACTIVE_SECOND]
auction['minNumberOfQualifiedBids'] = 1
END_ACTIVE_ENQUIRY_AUCTION_QUALIFICATION_WITH_1_ACTIVE_AND_UNSUCCESSFUL = auction

# auction with cancellations fixture
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
AUCTION_WITH_CANCELLATION = auction

# auction with bid in status 'active' and cancellation
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION]
auction['bids'] = [BID_ACTIVE_FIRST]

AUCTION_WITH_BIDS_WITH_CANCELLATION = auction

# auction with cancellations with document
auction = deepcopy(AUCTION)
auction['_id'] = uuid4().hex
auction['cancellations'] = [CANCELLATION_WITH_DOCUMENTS]
AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS = auction
