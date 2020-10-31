import os
from jinja2 import Template

def render(template_name, folder='templates', **kwargs):
    path = os.path.join(folder, template_name)
    #открыть по имени
    with open(path, encoding='utf-8') as f:
        #читаем
        template = Template(f.read())
    return template.render(**kwargs)
