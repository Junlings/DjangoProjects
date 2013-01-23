import csv
from django.http import HttpResponse

def read_css(filename,modelcls,excludes=None):
    """ read css file and then batch create the instance based on the input csv file
        The best is to use the model validation
    """
    
    fcsv = open(filename,'rb')
    Reader = csv.reader(fcsv, delimiter=',')
    header = Reader.next()
    #print header
    #field_names = set(header).difference(set(excludes))
    
    for row in Reader:
        #print row
        temp_dict = dict(zip(header, row))

        new_instance = modelcls.batch_create(temp_dict)

    return 1

def write_css(filename,field_names,queryset,header=True):
    """ write csv file based on the queryset and the field_names, with /o header"""
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename

    writer = csv.writer(response)
    if header:
        writer.writerow(list(field_names))
    for obj in queryset:
        writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
    return response    

def export_csv_template_action(description="Export objects import template as CSV file",
                         fields=None, exclude=None, header=True,fields_in_seq=None):
    """
    This function returns an export csv action
    with only one raw as column
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        filename = unicode(opts).replace('.', '_')
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        # set the sequence
        if fields_in_seq != None:
            field_names = fields_in_seq
        
        return write_css(filename,field_names,[],header=True)
    export_as_csv.short_description = description
    return export_as_csv