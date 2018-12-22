from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_get_listing,
    cancellation_get,
    cancellation_patch,
    cancellation_make_active,
    cancellation_document_post,
    cancellation_document_listing,
    cancellation_document_get,
    cancellation_document_patch,
    cancellation_document_put,
    cancellation_document_post_without_ds,
    cancellation_document_put_without_ds
)

from openprocurement.auctions.geb.tests.blanks.administrator import (
    auction_patch_field_mode,
    auction_patch_field_auction_period
)


class CancellationWorkFlowMixin(object):
    test_cancellation_get_listing = snitch(cancellation_get_listing)
    test_cancellation_get = snitch(cancellation_get)
    test_cancellation_patch = snitch(cancellation_patch)
    test_cancellation_make_active = snitch(cancellation_make_active)
    test_cancellation_document_post = snitch(cancellation_document_post)
    test_cancellation_document_post_without_ds = snitch(cancellation_document_post_without_ds)


class CancellationDocumentsWorkFlowMixin(object):
    test_cancellation_document_listing = snitch(cancellation_document_listing)
    test_cancellation_document_get = snitch(cancellation_document_get)
    test_cancellation_document_patch = snitch(cancellation_document_patch)
    test_cancellation_document_put = snitch(cancellation_document_put)
    test_cancellation_document_put_without_ds = snitch(cancellation_document_put_without_ds)


class BaseAdministratorTestMixin(object):
    test_auction_patch_field_mode = snitch(auction_patch_field_mode)
    test_auction_patch_field_auction_period = snitch(auction_patch_field_auction_period)
