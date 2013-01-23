from django.core.urlresolvers import reverse
from djangoextension.djangorestframework.resources import ModelResource
from models import accounts, transactions
from forms import AccountForm

class AccountsResource(ModelResource):
    """
    A test resource has field name of nickname
    """
    model = accounts
    form = AccountForm
    fields = ('id','nickname','get_owner','type','endwith')

    ordering = ('id',)
    
class TransactionsResource(ModelResource):
    """
    Address model
    """
    model = transactions
    fields = ('id','get_credit_account','get_debit_account','amount','get_request_info','get_response_info')
    ordering = ('id',)
    
    '''
    credit_account = models.ForeignKey(accounts, verbose_name=_(u"credit account"),related_name='credit')
    debit_account = models.ForeignKey(accounts, verbose_name=_(u"debit account"),related_name='debit')
    amount = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"amount"))
    
    submit = models.BooleanField(verbose_name=_(u"Sumitted?"), default=False)
    submit_by = models.ForeignKey(User, verbose_name=_(u"submit by"),related_name='submit')
    submit_on = models.DateTimeField(verbose_name=_(u"Submit date"),editable=False,blank=True,default=datetime.datetime.now())
    
    approve = models.BooleanField(verbose_name=_(u"Approved?"), default=False, blank=True)
    approve_by = models.ForeignKey(User, verbose_name=_(u"approve by"),related_name='approve') 
    approve_on = models.DateTimeField(verbose_name=_(u"Approve date"),editable=False,blank=True,default=datetime.datetime.now())
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    '''