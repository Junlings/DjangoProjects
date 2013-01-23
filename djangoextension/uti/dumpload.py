import cPickle as pickle
import os
from django.conf import settings

def check_folder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

def dump_data(filename,data,folder=None):
    if folder != None:
        fout_folder = os.path.join(settings.PROJECT_ROOT,folder)
    else:
        fout_folder = settings.PROJECT_ROOT
    check_folder(fout_folder)
    
    fout_name = os.path.join(fout_folder,filename)
    print fout_name
    fout = open(fout_name,'wb')
    
    pickle.dump(data,fout)
    
    fout.close()
    msg = 'dump date to %s' % fout_name
    
    print msg
def load_data(filename,folder=None):
    if folder != None:
        fout_folder = os.path.join(settings.PROJECT_ROOT,folder)
    else:
        fout_folder = settings.PROJECT_ROOT
    check_folder(fout_folder)
    
    fout_name = os.path.join(fout_folder,filename)
    print fout_name
    fout = open(fout_name,'rb')
    
    return pickle.load(fout)
    msg = 'load date from %s' % fout_name
    print msg