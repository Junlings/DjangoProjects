# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import single_file_upload_form
from fileuploadbackend import default

def single_file_upload(request,handle_uploaded_file):
    if request.method == 'POST':
        form = single_file_upload_form(request.POST, request.FILES)
        if form.is_valid():
            filename = default(request.FILES['file'])
            msg = handle_uploaded_file(filename)
            return  render_to_response('generic_create_confirm.html', msg,
                                                                context_instance=RequestContext(request))

    else:
        form = single_file_upload_form()

    return render_to_response('generic_create_form.html', {'form_list':[form],
                                                               'form_display_mode_table':True,
                                                               'form_is_multipart':True},
             context_instance=RequestContext(request)) 


def dojo_list_view(request,fields,fields_set,grid=None,target='api/'):
    fields_input = []
    for name in fields:
        fields_input_temp = {}
        fields_input_temp['field'] = name
        if name in fields_set.keys():
            fields_input_temp.update(fields_set[name])
        else:
            fields_input_temp.update({'name':name,'width':'10%'})
        fields_input.append(fields_input_temp)
    
    grid_default = {'width':'65em','height':'65em','padding':'1px','structure':fields_input}
    
    # apply custom defaults
    if grid != None:
        grid_default.update(grid)
    
    return render_to_response('dojo/rest_datagrid/dojo_generic_list.html',{'grid':grid_default,'target':target},context_instance=RequestContext(request))