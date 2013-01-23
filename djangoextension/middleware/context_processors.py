from django.conf import settings # import the settings file

def Set_ROOTURL(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ROOT_URL': settings.ROOT_URL,
            'MEDIA_URL':settings.MEDIA_URL,
            'REGISTER_URL':settings.REGISTER_URL,}
