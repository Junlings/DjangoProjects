#import pycurl
from celery.task import Task
from celery.registry import tasks


from celery.task import PeriodicTask
from datetime import timedelta
from models import Messages

class check_feeds(PeriodicTask):
    run_every = timedelta(seconds=60*5)
    def run(self, **kwargs):
        obj_list = Messages.objects.process()
        #logger = self.get_logger(**kwargs)
        #logger.info("Execute every 30 seconds")
        print("Execute feeds collect")

class CheckWebsiteTask(Task):

    def run(self, ip, **kwargs):
        return ip
        
        """
            p, created = Website.objects.get_or_create(ip=ip)

            try:
                    c = pycurl.Curl()
                    c.setopt(pycurl.URL, ip)
                    c.setopt(pycurl.TIMEOUT, 10)

                    c.perform()

                    p.alive = True

            except Exception, e:
                    print e
                    p.alive = False

            p.save()
        """

tasks.register(CheckWebsiteTask)
tasks.register(check_feeds)