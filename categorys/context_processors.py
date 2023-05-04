from .models import Category

"""context_processors is a list of dotted Python paths to callables that are used to 
populate the context when a template is rendered with a request. 
These callables take a request object as their argument and return a dict of items 
to be merged into the context."""
''' context processors là các hàm được sử dụng để đưa các biến toàn cục vào 
các context processors mặc định của Django. Context processors là các hàm Python 
nhận một request object làm tham số và trả về một dictionary chứa các biến context 
để sử dụng trong các template.'''
#new context processors must be sign up in settings.py to be use in template

def menu_links(request):
    #store all object of Category in variable links
    links = Category.objects.all()
    return dict(links=links)