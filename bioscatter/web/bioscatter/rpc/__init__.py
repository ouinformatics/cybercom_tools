from rpc4django import rpcmethod

# The doc string supports reST if docutils is installed
@rpcmethod(signature=['int', 'int', 'int'])
def add(a, b):
    '''Adds two numbers together
    >>> add(1, 2)
    3
    '''

    return a+b
