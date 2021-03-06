"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('apps.user.urls')),
    path('api/rbac/', include('apps.rbac.urls')),
    path('api/cmdb/', include('apps.cmdb.urls')),
    path('api/cmdb-api/', include('apps.api.urls')),
    path('api/ansible/', include('apps.ansible.urls')),
    path('api/settings/', include('apps.system.urls')),
    # path('api/task/', include('apps.task.urls')),
    path('api/tasks/', include('apps.task_platform.urls')),
    path('docs/', include_docs_urls(title='自动化运维平台!'))
]
