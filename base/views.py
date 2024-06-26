from django.shortcuts import render


# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse_lazy('users:profile'))
    return render(request, 'main/index.html')
