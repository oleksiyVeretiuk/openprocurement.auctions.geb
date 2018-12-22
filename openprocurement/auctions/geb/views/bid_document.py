# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view,
    context_unpack,
    dgf_upload_file
)
from openprocurement.auctions.core.views.mixins import AuctionBidDocumentResource
from openprocurement.auctions.core.validation import (
    validate_file_upload
)
from openprocurement.auctions.core.validation import (
    validate_patch_document_data
)

from openprocurement.auctions.core.interfaces import (
    IBidManager,
    IBidDocumentManager
)


@opresource(name='geb:Auction Bid Documents',
            collection_path='/auctions/{auction_id}/bids/{bid_id}/documents',
            path='/auctions/{auction_id}/bids/{bid_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bidder documents")
class AuctionBidDocumentResource(AuctionBidDocumentResource):

    @json_view(validators=(validate_file_upload,), permission='edit_bid')
    def collection_post(self):
        """Auction Bid Document Upload
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidManager)

        applicant = self.request.validated['document'] if 'data' in self.request.validated else None

        if applicant:
            document = manager.create(applicant)
        else:
            document = dgf_upload_file(self.request)
            self.context.documents.append(document)
            manager._is_changed = True

        save = manager.save()

        if save:
            msg = 'Created auction bid document {}'.format(document.id)
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_document_create'}, {'document_id': document['id']})
            self.LOGGER.info(msg, extra=extra)

            self.request.response.status = 201

            route = self.request.matched_route.name.replace("collection_", "")
            locations = self.request.current_route_url(_route_name=route, document_id=document.id, _query={})
            self.request.response.headers['Location'] = locations
            return {'data': document.serialize("view")}

    @json_view(content_type="application/json", validators=(validate_patch_document_data), permission='edit_bid')
    def patch(self):
        """Auction Bid Document Update"""
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IBidDocumentManager)

        manager.change()
        save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_document_patch'})
            msg = 'Updated auction bid document {}'.format(self.request.context.id)
            self.LOGGER.info(msg, extra=extra)
            return {'data': self.request.context.serialize("view")}
