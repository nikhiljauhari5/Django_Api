from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import (StatusListAPIView,StatusAPIView,StatusMixinsAPIView)

s1 = StatusAPIView.as_view({
    'get':'list',
    'post':'create',
})
s2 = StatusAPIView.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})

urlpatterns = [
    path('list/',StatusListAPIView.as_view()),
    path('genericapiview/',s1),
    path('genericapiview/<int:pk>',s2),
    path('mixinsAPIView/',StatusMixinsAPIView.as_view())
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# api/status/list/  -> List
# api/status/Create/  -> Create
# api/status/Detail/  -> Detail
# api/status/Update/  -> Update
# api/status/Delete/  -> Delete
