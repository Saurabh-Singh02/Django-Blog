from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urls.py
from django.http import JsonResponse

def chrome_devtools_stub(request):
    return JsonResponse({}, safe=False)

urlpatterns += [
    path(".well-known/appspecific/com.chrome.devtools.json", chrome_devtools_stub),
]    