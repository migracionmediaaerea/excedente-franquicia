from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse

class PermissionDeniedErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # This is the method that responsible for the safe-exception handling
        if isinstance(exception, PermissionDenied):
            return render(
                request=request,
                template_name="403.html",
                status=403
            )
        return None