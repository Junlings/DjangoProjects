from django import forms 
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from models import PurchaseDoc, PurchaseRequest, Purchase_cost
from supply.models import ItemTemplate
from assets.models import assetgroup, asset

#class purchase_search_form(forms.Form):
#    keywords = 


class PurchaseRequestForm(forms.Form):
    item = forms.ModelChoiceField(queryset=ItemTemplate.objects.all(), empty_label="(Nothing)")
    quantity = forms.IntegerField()
    def __unicode__(self):
        return _(u"Purchase Report Form") % {}
        
    def save(self, person=None,cost=None,docs=None,commit=True):
        # create purchase reques
        purchase_instance = PurchaseRequest(person=person,quantity=self.cleaned_data['quantity'],cost=cost)
        purchase_instance.save()
        
        # add document if possible
        if docs != None:
            purchase_instance.docs.add(docs)
        # get purchase item
        item = self.cleaned_data['item'] #ItemTemplate.objects.get(id=self.cleaned_data['item'])
        
        # create asset_group
        asset_g_instance = assetgroup(name='Purchase_'+str(purchase_instance.id))
        asset_g_instance.save()  # need to save first to add many-to-many 
        
        # create asets and asset group
        for i in range(0,self.cleaned_data['quantity']):
            FSIN = '%s_%s' % (str(purchase_instance.id).zfill(5),
                                       str(i).zfill(5)) 
            asset_instance = asset(item=item,FSIN=FSIN)
            asset_instance.save()
            asset_g_instance.assets.add(asset_instance)
        
        asset_g_instance.save()
        return asset_g_instance           
        
class PurchaseDocForm(forms.ModelForm):
    class Meta:
        model = PurchaseDoc
    def __unicode__(self):
        return _(u"Purchase Document Form") % {}
        
class PurchaseDocSelectForm(forms.Form):
    docs = forms.ModelChoiceField(queryset=PurchaseDoc.objects.all(), empty_label="(Nothing)")   

    class Meta:
        model = PurchaseDoc
    def __unicode__(self):
        return _(u"Purchase Documents Select Form") % {}

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

YEAR_CHOICES = (
    ('2012','2012'),
)
     
        
class Purchase_costForm(forms.ModelForm):
    class Meta:
        model = Purchase_cost
        
    def __unicode__(self):
        return _(u"Purchase Cost Form") % {}
        
class PurchaseSelectForm(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    
    CHOICES = MONTH_CHOICES # (('Year Upto Date','Year Upto Date'),) + MONTH_CHOICES
    month = forms.ChoiceField(choices=CHOICES)
    
    def __unicode__(self):
        return _(u"Purchase Monthly Select Form") % {}  

    
        
"""
def create_items_from_purchase(newpurchase):
    
    Person = newpurchase.Person
    Itemtemplate = newpurchase.Itemtemplate
    Quantity = newpurchase.Quantity
    TotalReceiptPrice = newpurchase.TotalReceiptPrice
    TotalCost = newpurchase.TotalCost
    
    property_number = newpurchase.id
    
    # to prevent the overload of server
    if Quantity > 100:
        raise Error
    
    for i in range(0,Quantity):
        # first create prices instance
        new_price = Prices(receipt_price=TotalReceiptPrice/Quantity,
                           purchase_price=TotalCost/Quantity)
        new_price.save()
        new_item = Item(item_template=Itemtemplate,
                        item_price = new_price,
                        property_number=str(property_number)+'_'+str(i),
                        )
        new_item.save()
        new_price.save()
    return 1
    #item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u"item template"))
    #property_number = models.CharField(verbose_name=_(u"asset number"), max_length=48)
    #notes = models.TextField(verbose_name=_(u"notes"), null=True, blank=True)	
    #serial_number = models.CharField(verbose_name=_(u"serial number"), max_length=48, null=True, blank=True)
    #location = models.ForeignKey(Location, verbose_name=_(u"location"), null=True, blank=True)
    #active = models.BooleanField(default=True)
    
def create_transaction_from_purchase(newpurchase,user):
    # first create prices instance
    
    notes = 'Purchaseid %(id)s for %(Quantity)s of item %(name)s' % {'id':newpurchase.id,
                                                                     'Quantity':newpurchase.Quantity,
                                                                     'name':newpurchase.Itemtemplate.description}
    
    new_state = Transaction(user = user,debit=newpurchase.TotalCost,
                                  notes=notes)
    return new_state.save()
    
def create_state_from_purchase(newpurchase):
    new_state = PurchaseState(purchase = newpurchase,
                                  state='Placed')
    return new_state.save()    
    
class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.Person = kwargs.pop("Person",None)
        super(PurchaseForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super(PurchaseForm, self).save(commit=False)
        if self.Person:
            instance.Person = self.Person
        
        new_purchase = instance.save()
        # add item based on the purchase
        success1 = create_items_from_purchase(instance)
        success2 = create_state_from_purchase(instance)
        success3 = create_transaction_from_purchase(instance,self.Person)
        return instance
        
    class Meta:
        model = Purchase
        exclude = ('Person')
        
    def __unicode__(self):
        return _(u"Purchase Report Form") % {}



class PurchaseDocForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.pop("purchase",None)
        self.person = kwargs.pop("user",None)
        self.files = kwargs.pop("files",None)
        super(PurchaseDocForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super(PurchaseDocForm, self).save(commit=False)
        if self.purchase:
            instance.content_object = self.purchase
        if self.person:
            instance.person = self.person
        instance.doc = self.files
        
        new_purchasedoc = instance.save()
        return instance
        
    class Meta:
        model = CollDoc
        exclude = ('person','content_type','object_id')
       
    def __unicode__(self):
        return _(u"Purchase Document  Report Form") % {}       
'''
class ItemTemplateForm_view(DetailForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos',)

    
class LogForm(forms.ModelForm):
    class Meta:
        model = Log


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory


class InventoryForm_view(DetailForm):
    class Meta:
        model = Inventory

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
'''

"""