def auth(func):
    def wrapper(*args, **kwargs):
        #print request
        print args
        print kwargs
        func(*args, **kwargs)
    return wrapper

@auth
def x(request):
    print request


x(5)