from django.urls import path
from .views import  (
    PurchaseListCreateAPIView, PurchaseDetailAPIView,AddCommentAPIView,
    SpecificationListCreateAPIView,SpecificationRetrieveUpdateDestroyAPIView,
    ReadFirstColumnAPIView,PurchaseDataListCreateAPIView,
    PurchaseDataDetailAPIView,PurchasePaymentAPIView,ApprovePurchaseDataAPIView
)
from .views_for_download import (
    PurchasePdfDownloadView,
)

urlpatterns = [
    path('api/purchases/', PurchaseListCreateAPIView.as_view(), name='purchase-list-create'),
    path('api/purchases/<int:pk>/', PurchaseDetailAPIView.as_view(), name='purchase-detail'),
    path('api/purchases/pdf/download/<int:pk>/', PurchasePdfDownloadView.as_view(), name='purchase-detail-pdf-download'),
    path('api/purchases/add_comment/<int:purchase_id>/', AddCommentAPIView.as_view(), name='purchase-add-comment'),
    # Specification Endpoints
    path('api/specifications/', SpecificationListCreateAPIView.as_view(), name='specification-list-create'),
    path('api/specifications/<int:pk>/', SpecificationRetrieveUpdateDestroyAPIView.as_view(), name='specification-detail'),
    path('api/purchases/<int:purchase_id>/purchase_data/', PurchaseDataListCreateAPIView.as_view(), name='purchasedata-list-create'),
    path('api/purchases/<int:purchase_id>/purchase_data/<int:pk>/', PurchaseDataDetailAPIView.as_view(), name='purchasedata-detail'),
    path('api/purchases/<int:purchase_id>/purchase_payment/', PurchasePaymentAPIView.as_view(), name='purchase-payment'),
    path('api/purchases/excel', PurchaseListCreateAPIView.as_view(), name='purchase-list-create'),
     # New CSV Read Endpoint
    path('api/purchases/read_csv/', ReadFirstColumnAPIView.as_view(), name='read-csv'),
    path('api/purchases/approve_purchase_data/<int:purchase_data_id>/', ApprovePurchaseDataAPIView.as_view(), name='approve-purchase-data'),
    
]