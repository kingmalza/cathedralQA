import urllib.request
import requests 

from tenant_schemas.middleware import BaseTenantMiddleware
from django.http import HttpResponse, HttpResponseRedirect
from tenant_schemas.utils import (get_tenant_model, remove_www,
                                  get_public_schema_name)

class XHeaderTenantMiddleware(BaseTenantMiddleware):
    """
    Determines tenant by the value of the ``X-DTS-SCHEMA`` HTTP header.
    """
    def get_tenant(self, model, hostname, request):
    
        schema_name = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
        #print('SCHEMA--->>',schema_name, 'SINGLE-->',request.META)
        return model.objects.get(schema_name=schema_name)