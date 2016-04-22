from django.http import JsonResponse


def ajax_response(success=False, errors=[]):
    context_dic = {}
    context_dic['success'] = success
    context_dic['errors'] = errors
    return JsonResponse(context_dic, safe=False)