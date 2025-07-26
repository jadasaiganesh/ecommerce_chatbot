from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # ⬅️ Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot/', include('chatbot.urls')),
    path('', RedirectView.as_view(url='/chatbot/', permanent=False)),  # ⬅️ Add this line
]
