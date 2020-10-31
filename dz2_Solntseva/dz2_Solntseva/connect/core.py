import os


class Application:

    def parse_data(self, data: str):
        res = {}
        if data:
            # разделение параметров через &
            params = data.split('&')
            for item in params:
                # разделение ключа и значения через =
                k, v = item.split('=')
                res[k] = v
        return res

    def get_wsgi_data(self, env):
        # получить длину тела
        length_data = env.get('CONTENT_LENGTH')
        # привести к int
        if length_data:
            length = int(length_data)
        else:
            length = 0
        # считать данные, если они есть
        if length > 0:
            data = env['wsgi.input'].read(length)
        else:
            data = b''
        return data

    def parse_wsgi_decode_data(self, data: bytes):
        res = {}
        if data:
            # декодирование данных
            data_str = data.decode(encoding='utf-8')
            # сбор данных в словарь
            res = self.parse_data(data_str)
        return res

    def __init__(self, urls: dict, fronts: list):
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """ environ: словарь данных от сервера
            start_response: функция для ответа серверу"""
        path = environ['PATH_INFO']
        if not path.endswith(os.path.sep):
            path += os.path.sep
        # получение всех данных о запросе
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_decode_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_data(query_string)

        if path in self.urls:
            view = self.urls[path]
            request = {}
            # добавление параметров запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
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
