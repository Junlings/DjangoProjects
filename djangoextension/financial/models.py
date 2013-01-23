import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from djangoextension.action.models import crequests, cresponses
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Q
from decimal import Decimal
ACCOUNT_TYPE = (
    ('paypal account','paypal account'),
    ('amazon account','amazon payment account'),
    ('credit card','credit card account'),
    ('debit card','debit card account'),
    ('checking account','checking account'),
    ('saving account','saving account'),
    ('generic','generic')
)

ASSOCIATE_PARTY = (
    ('BOA','BOA'),
    ('Chase','Chase'),
    ('Citi','Citi'),
    ('Paypal','Paypal'),
    ('Other','Other'),
    
    
)

TRANSACTION_MODE = (
    ('debit','debit'),
    ('credit','credit'),
    
)

class accounts(models.Model):
    ''' The payment model '''
    owner = models.ForeignKey(User, verbose_name=_(u"owner"))
    nickname = models.CharField(max_length=100,verbose_name=_(u"nickname"))
    type = models.CharField(max_length=100,choices=ACCOUNT_TYPE,verbose_name=_(u"type"))
    endwith = models.CharField(max_length=20,verbose_name=_(u"account endwith"), null=True, blank=True)
    associate = models.CharField(max_length=40,choices=ASSOCIATE_PARTY,verbose_name=_(u"associate party"), null=True, blank=True)
    expire = models.CharField(max_length=20,verbose_name=_(u"Expiration Date"), null=True, blank=True)
    verify = models.CharField(max_length=20,verbose_name=_(u"Verification Key"), null=True, blank=True)
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"account")
        verbose_name_plural = _(u"accounts")
    
    def __unicode__(self):
        return "%(owner)s | %(nickname)s | %(endwith)s" % {'nickname':self.nickname,'owner':self.owner,'endwith':self.endwith}        

    def get_owner(self):
        return self.owner.username
    
    def generate_summary(self,year):
        for month in range(1,13):
            newobj = AccountMonthlySummary(year=year,month=month,account=self)
            newobj.save()
    
    def YTD_balance(self):
        now = datetime.datetime.now()
        summaries = AccountMonthlySummary.objects.filter(year=now.year,month__lte=now.month,account=self)
        total = {'credit':Decimal('0.0'),'debit':Decimal('0.0'),'balance':Decimal('0.0')}
        
        for summary in summaries:
            total['credit'] += summary.total_credit
            total['debit'] += summary.total_debit
            total['balance'] += summary.total_credit - summary.total_debit
        return total

class transactionmanager(models.Manager):
    
    def summary(self,accountobj):
        temp = {'amountplus':Decimal('0.0'),'amountminus':Decimal('0.0')}
        for record in self.all():
            if record.accountA == accountobj:
                if record.modeA == 'credit':
                    temp['amountplus'] += record.amount
                else:
                    temp['amountminus'] += record.amount
            elif record.accountB == accountobj:
                if record.modeB == 'credit':
                    temp['amountplus'] += record.amount
                else:
                    temp['amountminus'] += record.amount        
        return temp
    
    def summary_general(self,queryset,accountobj,fieldname=None):
        temp = {'amountplus':Decimal('0.0'),'amountminus':Decimal('0.0')}
          
        for record in queryset:
            if fieldname != None and record.fieldname != fieldname:
                continue
            else:
                
                if record.accountA == accountobj:
                    if record.modeA == 'credit':
                        temp['amountplus'] += record.amount
                    else:
                        temp['amountminus'] += record.amount
                elif record.accountB == accountobj:
                    if record.modeB == 'credit':
                        temp['amountplus'] += record.amount
                    else:
                        temp['amountminus'] += record.amount        
        return temp    

class transactions(models.Model):
    accountA = models.ForeignKey(accounts, verbose_name=_(u"Account A"),related_name='account_A')
    accountB = models.ForeignKey(accounts, verbose_name=_(u"Account B"),related_name='account_B')
    modeA = models.CharField(max_length=10,choices=TRANSACTION_MODE,verbose_name=_(u"Account A mode"))
    modeB = models.CharField(max_length=10,choices=TRANSACTION_MODE,verbose_name=_(u"Account B mode"))
    amount = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"amount"))
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    
    # record which type of instance and which field generate this transaction
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    fieldname = models.CharField(max_length=100,verbose_name=_("related field"),default='id', null=True, blank=True)
    fullfilled = models.BooleanField(verbose_name=_("Fullfilled?"),default=False, blank=True)
    lastmodified = models.DateTimeField(verbose_name=_(u"Last Modified"),default=datetime.datetime.now(), blank=True)
    
    objects = transactionmanager()
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"transaction")
        verbose_name_plural = _(u"transactions")
    
    def __unicode__(self):
        return "Transaction_%s" % (self.id)    
    
    def get_credit_account(self):
        return self.credit_account.__unicode__
    def get_debit_account(self):
        return self.debit_account.__unicode__
    
    def related_purchase(self):
        ct  = ContentType.objects.get(app_label="vending", model="Purchase_cost")
        obj = ct.get_object_for_this_type(pk=self.object_id)

        return obj.request
        
    def get_request_info(self):
        try:
            obj = transaction_requests.objects.get(transaction=self)
            return obj.__unicode__
        except:
            return []
            
        
    
    def get_response_info(self):
        try:
            obj = transaction_responses.objects.get(transaction=self)
            return obj.__unicode__
        except:
            return []


class TransactionConfirm(models.Model):
    transaction = models.OneToOneField(transactions,verbose_name=_("Transaction"))
    confirmed = models.BooleanField(verbose_name=_("Confirmed?"),default=False, blank=True)
    lastmodified = models.DateTimeField(verbose_name=_(u"Last Modified"), auto_now=True)
    class Meta:
        abstract = True
        
        
class TransactionConfirmDebit(TransactionConfirm):
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Confirm Debit")
        verbose_name_plural = _(u"Confirm Debits")
        
    def __unicode__(self):
        return '%id' %(self.id)



class TransactionConfirmCredit(TransactionConfirm):
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Confirm Credit")
        verbose_name_plural = _(u"Confirm Credits")
        
    def __unicode__(self):
        return '%id' %(self.id)

YEAR_CHOICES = (
    ('2012','2012'),
)

MONTH_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
)


class AccountMonthlySummary(models.Model):
    account  = models.ForeignKey(accounts,verbose_name=_("account"))
    transaction = models.ManyToManyField(transactions,verbose_name=_("transactions"),blank=True,null=True)
    year = models.CharField(max_length=4,choices=YEAR_CHOICES,verbose_name=_("Year"))
    month = models.CharField(max_length=2,choices=MONTH_CHOICES,verbose_name=_("Month"))
    total_debit = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total debit"), blank=True,null=True,default='0.0')
    total_credit = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total Credit"), blank=True,null=True,default='0.0')
    balance = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Balance"), blank=True,null=True,default='0.0')
    
    class Meta:
        ordering = ['account','year','month']
        verbose_name = _(u"Account Monthly Summary")
        verbose_name_plural = _(u"Account Monthly Summary")
    
    def number_of_transaction(self):
        return self.transaction.all().count()
    
    def get_transactions(self):
        self.transaction.clear()
        transactionobjs = transactions.objects.filter((Q(accountA=self.account)|Q(accountB=self.account))&Q(lastmodified__year=self.year)&Q(lastmodified__month=self.month))
        if transactionobjs.all().count() != 0:
            self.transaction.add(*transactionobjs.all())
            self.save()
            return self
        else:
            return self
        
        
    def get_transaction_summary(self):


        summary = self.transaction.summary(self.account)
        self.total_credit = summary['amountplus']
        self.total_debit = summary['amountminus']
    
        #pre_balance = self.get_prev_balance()
        #self.balance = pre_balance + self.total_credit - self.total_debit
        self.save()            
       
        
        
    '''    
    def get_prev_balance(self,force_update=False):
        pre_month = int(self.month)-1
        
        if pre_month == 0:
            pre_month = 12
            pre_year = self.year -1
        else:
            pre_year = self.year
            
        try:
            pre_summary = AccountMonthlySummary.objects.get(Q(year=pre_year)&Q(month=pre_month))
            if not force_update:
                return pre_summary.balance
            
            else:
                pass 
            
        except:
            if not force_update:
                return 0.0
            else:
                pass   # for future use to create objects
        

    
    def update(self):
        transactionobjs = self.get_transactions()
        if transactionobjs != None:
            self.transaction.add(transactionobjs)
            summary = transactionobjs.summary()
            self.total_credit = summary['amountplus']
            self.total_debit = summary['amountminus']
        
            pre_balance = self.get_prev_balance()
            self.balance = pre_balance + self.total_credit - self.total_debit
            self.save()            
            
        else:
            pass
    '''
        
        
'''
class transaction_requests(crequests):
    transaction = models.OneToOneField(transactions, verbose_name=_(u"transactions"))
    

    class Meta:
        ordering = ['id']
        verbose_name = _(u"transaction request")
        verbose_name_plural = _(u"transaction requests")       
        
class transaction_responses(cresponses):
    transaction = models.OneToOneField(transactions, verbose_name=_(u"transactions"))
        
    class Meta:
        ordering = ['id']
        verbose_name = _(u"transaction response")
        verbose_name_plural = _(u"transaction responses")
'''