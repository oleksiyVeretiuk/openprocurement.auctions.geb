# -*- coding: utf-8 -*-
from zope.interface import implementedBy
from openprocurement.auctions.core.utils import (
    json_view
)
from openprocurement.auctions.core.validation import (
    validate_file_upload
)
from openprocurement.auctions.core.interfaces import (
    ICancellationManager
)
from openprocurement.auctions.core.utils import opresource, dgf_upload_file
from openprocurement.auctions.core.views.mixins import (
    AuctionCancellationDocumentResource
)


@opresource(name='geb:Auction Cancellation Documents',
            collection_path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction cancellation documents")
class AuctionCancellationDocumentResource(AuctionCancellationDocumentResource):

    @json_view(permission='view_auction')
    def collection_get(self):
        """Auction Cancellation Documents List"""

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)
        document_type = type(manager.context).documents.model_class
        return manager.represent_subresources_listing(implementedBy(document_type))

    @json_view(validators=(validate_file_upload,), permission='edit_auction')
    def collection_post(self):
        """
        Auction Cancellation Document Upload
        """
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), ICancellationManager)

        applicant = self.request.validated['document'] if 'data' in self.request.validated else None

        if applicant:
            document = manager.create(applicant)
        else:
            document = dgf_upload_file(self.request)
            self.context.documents.append(document)
            manager._is_changed = True

        save = manager.save()

        if save:
            msg = 'Create auction cancellation document {}'.format(document['id'])
            manager.log_action('auction_cancellation_document_create', msg)
            return manager.represent_subresource_created(document)
