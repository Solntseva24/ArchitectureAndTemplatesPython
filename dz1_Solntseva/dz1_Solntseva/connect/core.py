import os
class Application:

    def __init__(self, urls: dict, fronts: list):
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """ environ: словарь данных от сервера
            start_response: функция для ответа серверу"""
        path = environ['PATH_INFO']
        if not path.endswith(os.path.sep):
            path += os.path.sep
        if path in self.urls:
            view = self.urls[path]
            request = {}
            # front controller
            for front in self.fronts:
                front(request)

            code, body = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [body.encode('utf-8')]
        else:
            start_response('NOT FOUND 404', [('Content-Type', 'text/html')])
            return [b'NOT FOUND 404']
