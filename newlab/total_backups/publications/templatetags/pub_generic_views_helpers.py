import types
from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable, VariableDoesNotExist

from django.template.defaultfilters import register
from django.forms.models import model_to_dict


@register.filter(name='labellink')
def labellink(label):
    return '<a href="%spublications/lb/%s/"> %s </a>' % (settings.ROOT_URL,label,label)

@register.filter(name='deeplookup')
def deeplookup(obj, field):
    res = getattr(obj, field)
    
    
        


    if hasattr(res, '__call__'):
        return res()
    else:
        if field == 'LB':
            return labellink(res)
        else:
            return res

@register.filter(name='DetailUp')
def DetailUp(obj):
    keys = model_to_dict(obj).keys()
    return keys

@register.filter(name='ModelName')
def ModelName(obj):
    return obj.__class__.__name__
    
'''
register = Library()

class DynUrlNode(Node):
    def __init__(self, *args):
        self.name_var = Variable(args[0])
        if len(args)>1:
            #Process view arguments
            self.args = [Variable(a) for a in args[1].split(',')]
        else:
            self.args = []

    def render(self, context):
        name = self.name_var.resolve(context)
        args = [a.resolve(context) for a in self.args]
        try:
            return reverse(name, args = args)
        except:
            #Argument might be pointing to a context variable
            args = [Variable(a).resolve(context) for a in args]
            return reverse(name, args = args)


@register.tag
def dynurl(parser, token):
    args = token.split_contents()
    return DynUrlNode(*args[1:])


@register.filter
@stringfilter
def is_class(value, arg):
    return value[21:(value[21:].find(' ')+21)] == arg


def return_attrib(obj, attrib, arguments={}):
    try:
        if isinstance(obj, types.DictType) or isinstance(obj, types.DictionaryType):
            return obj[attrib]
        elif isinstance(attrib, types.FunctionType):
            return attrib(obj)
        else:
            result = reduce(getattr, attrib.split("."), obj)
            if isinstance(result, types.MethodType):
                if arguments:
                    return result(**arguments)
                else:
                    return result()
            else:
                return result
    except Exception, err:
        if settings.DEBUG:
            return "Error: %s; %s" % (attrib, err)
        else:
            pass

@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)
'''