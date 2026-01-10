from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core apps
    path("", include("main.urls", namespace="main")),
    path("accounts/", include("accounts.urls", namespace="accounts")),

    # Service apps (example namespacing; ensure each defines app_name)
    path("services/kmz-polygon-analysis/", include("services.kmz_polygon_analysis.urls", namespace="kmz_polygon_analysis")),
    path("services/kmz-to-excel/", include("services.kmz_to_excel.urls", namespace="kmz_to_excel")),
    path("services/kmz-to-shapefile/", include("services.kmz_to_shapefile.urls", namespace="kmz_to_shapefile")),
    path("services/shap-to-kmz/", include("services.shap_to_kmz.urls", namespace="shap_to_kmz")),
    path("services/pdf-to-word/", include("services.pdf_to_word.urls", namespace="pdf_to_word")),
    path(
        "services/trip-length-distribution/",
        include("services.trip_length_distribution.urls", namespace="trip_length_distribution"),
    ),
    path("services/outliers/", 
        include(("services.outlier.urls", "outLiers_Data"), namespace="outLiers_Data")),
    # Tip 
    path('services/trip_generation/', include('services.trip_generation.urls')),

]

# Static/media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

