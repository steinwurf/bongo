from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.

def show(request):
    template = loader.get_template('benchmarks/show.html')
    context = RequestContext(request, {
        'test': [1,2,3,4,5,6,7,8],
    })
    return HttpResponse(template.render(context))