# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    json_view,
    context_unpack,
    opresource,
)
from openprocurement.auctions.core.validation import (
    validate_file_upload,
    validate_patch_document_data,
)
from openprocurement.auctions.core.views.mixins import AuctionDocumentResource

from openprocurement.auctions.core.interfaces import (
    IAuctionManager,
    IDocumentManager
)

from openprocurement.auctions.geb.utils import (
    get_file
)


@opresource(name='geb:Auction Documents',
            collection_path='/auctions/{auction_id}/documents',
            path='/auctions/{auction_id}/documents/{document_id}',
            auctionsprocurementMethodType="geb",
            description="Auction related binary files (PDFs, etc.)")
class AuctionDocumentResource(AuctionDocumentResource):

    @json_view(permission='upload_auction_documents', validators=(validate_file_upload,))
    def collection_post(self):
        """Auction Document Upload"""
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IAuctionManager)

        document = manager.upload_document()

        if document:
            save = manager.save()

        if save:
            msg = 'Created auction document {}'.format(document.id)
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_document_create'}, {'document_id': document['id']})
            self.LOGGER.info(msg, extra=extra)

            self.request.response.status = 201

            route = self.request.matched_route.name.replace("collection_", "")
            locations = self.request.current_route_url(_route_name=route, document_id=document.id, _query={})
            self.request.response.headers['Location'] = locations
            return {'data': document.serialize("view")}

    @json_view(permission='view_auction')
    def get(self):
        """Auction Document Read"""                                             # TODO rm black box
        document = self.request.validated['document']
        offline = bool(document.get('documentType') == 'x_dgfAssetFamiliarization')
        if self.request.params.get('download') and not offline:
            return get_file(self.request)
        document_data = document.serialize("view")
        document_data['previousVersions'] = [
            i.serialize("view")
            for i in self.request.validated['documents']
            if i.url != document.url or
            (offline and i.dateModified != document.dateModified)
        ]
        return {'data': document_data}

    @json_view(content_type="application/json", permission='upload_auction_documents', validators=(validate_patch_document_data,))
    def patch(self):
        """Auction Document Update"""
        save = None

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IDocumentManager)

        manager.change()
        save = manager.save()

        if save:
            extra = context_unpack(self.request, {'MESSAGE_ID': 'auction_document_patch'})
            msg = 'Updated auction document {}'.format(self.request.context.id)
            self.LOGGER.info(msg, extra=extra)
            return {'data': self.request.context.serialize("view")}
