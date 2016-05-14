from django.contrib import messages
from django.http import HttpResponseRedirect


class AppError(object):
    pass


class AppExceptionTrap:
    def process_exception(self, request, exception):
        if isinstance(exception, AppError):
            messages.error(request, str(exception))
            return HttpResponseRedirect('/')
        return None
