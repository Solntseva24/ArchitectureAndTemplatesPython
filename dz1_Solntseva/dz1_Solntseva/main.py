import views
from connect import Application

urls = {
    '/': views.index_view,
    '/about/': views.about_view,
    '/videofiles/': views.videofiles_view,
}


def controller_secret(request):
    #front Controller
    request['secret_key'] = 'SECRET'

fronts = [controller_secret]

application = Application(urls, fronts)