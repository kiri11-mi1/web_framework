from web_framework import WebFramework
import json


'''Реализация простого TODO сервиса'''


# Подключаем наш супер фреймворк
app = WebFramework()

# Извлекаем данные в нашу базу данных(словарь)
db = json.load( open('db.json', 'r') )


def find_task(task_id):
    '''Нахождение таска по id из словаря db'''
    for task in db:
        if task['id'] == task_id:
            return task


@app.route('/tasks/get')
def get_tasks(request):
    # Берём из базы все таски
    tasks = db

    # Отправляем таски
    return json.dumps(db), 'application/json'


@app.route('/tasks/get/{task_id:d}')
def get_task_by_id(request, task_id):

    # Находим таск проверяем на существование
    task = find_task(task_id)
    if task is None:
        return json.dumps({'error': 'Not found'}), 'application/json'
    return json.dumps(task), 'application/json'


@app.route('/tasks/update/{task_id:d}')
def put(request, task_id):

    # Для дальнейших изменений нам понадобится таск с нужным id
    task = find_task(task_id)
    if task is None:
        return json.dumps({'error': 'Not found'}), 'application/json'
    
    if not request.params:
        return json.dumps({'error': 'Bad Request'}), 'application/json'
    
    task['title'] = request.params.get('title', task['title'])
    task['description'] = request.params.get('description', task['description'])
    task['done'] = request.params.get('done', task['done'])

    return json.dumps(task), 'application/json'


@app.route('/tasks/add')
def add_task(request):

    # Сортируем базу по id
    tasks = sorted(db, key=lambda k: k['id'])

    # Получаем id последнего элемента
    last_id = tasks[-1]['id']

    # Если в задаче не будет названия или в запросе не будет данных, то лови ошибку
    if not request.params  or 'title' not in request.params:
        return json.dumps({'error': 'Bad Request'}), 'application/json'

    # Создаём таск из данных запроса
    task = {
        'id': last_id + 1,
        'title': request.params['title'],
        'description': request.params.get('description', ""),
        'done': False
    }

    db.append(task)

    return json.dumps(task), 'application/json'


@app.route('/tasks/delete/{task_id:d}')
def delete_task(request, task_id):
    # Находим и проверяем
    task = find_task(task_id)
    if task is None:
        return json.dumps({'error': 'Not found'}), 'application/json'
    
    # Удаляем
    db.remove(task)

    return json.dumps(task), 'application/json'


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        exit()