from connect import render

def index_view(request):
    print(request)
    key_secret = request.get('secret_key', None)
    # возвращаем тело ответа
    return '200 OK', render('index.html', secret=key_secret)

def about_view(request):
    print(request)
    # возвращаем about
    return '200 OK', 'About'

def videofiles_view(request):
    print(request)
    key_secret = request.get('secret_key', None)
    # возвращаем тело ответа
    return '200 OK', render('videofiles.html', secret=key_secret)