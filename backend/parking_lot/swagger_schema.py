from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Parking Lot API",
        default_version='v1',
        description="API doc for parking lot assignment from Toogethr",
        terms_of_service="https://www.toogethr.com/",
        contact=openapi.Contact(email="mh.abbasi2006@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf="parking_lot.urls",
)
