from webob import Request, Response
from parse import parse
from wsgiref.simple_server import make_server

class WebFramework:
    def __init__(self):
        self.routes = {}


    def route(self, path):
        '''Обработка маршрутов'''
        def wrapper(handler):
            """Сохранение в словарь {'путь' : функция_бизнес_логики}"""
            self.routes[path] = handler
            return handler

        return wrapper


    def __call__(self, environ, start_response):
        '''Входная точка WSGI приложения'''
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)


    def handle_request(self, request):
        '''Обработка запроса и возвращение ответа'''
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            response.text, response.content_type = handler(request, **kwargs)
        else:
            return self.default_response(response)

        return response

    def find_handler(self, request_path):
        '''Нахождение функции бизнесс-логики для пути запроса'''
        for path, handler in self.routes.items():
            # Парсинг путей через готовую реализацию parse
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None


    def default_response(self, response):
        response.status_code = 404
        response.text = '<center>Page Not Found</center>'
        return response

    def run(self, host='127.0.0.1', port=5000):
        '''Запуск готовой реализации WSGI-сервера'''
        print(f'Сервер запущен--->http://{host}:{port}')
        server = make_server(host, port, self)
        server.serve_forever()
