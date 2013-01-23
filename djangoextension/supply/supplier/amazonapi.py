from amazonproduct import *
from BeautifulSoup import BeautifulSoup

CHAR = type('text')
INTEGRAL = type(1L)
nonNegativeInteger = 'nonNegativeInteger'

class response_e():
    def __init__(self,type,Ancestry=None,default=None):
        self.type = type
        self.default = default
        self.Ancestry = Ancestry

# define response element
About = response_e(CHAR)
ASIN = response_e(CHAR)
Title  = response_e(CHAR)
TotalPages = response_e(nonNegativeInteger)
TotalResults = response_e(nonNegativeInteger)



class response_g():
    def __init__(self,*args,**kargs):
        self.elements = kargs['elements']
        self.operations = kargs['operations']
        
    



# response groups
Accessories = response_g(
    {'elements':[
                ASIN,
                Title,
                TotalPages,
                TotalResults
                ],
     'operations':[
                SimilarityLookup,
                ItemLookup,
                ItemSearch
                  ]
    })

"""
AlternateVersions = [AlternateVersion,ASIN,Binding,Title]
BrowseNodeInfo = [BrowseNodeId,Name]
BrowseNodes = [BrowseNodeId,IsCategoryRoot,Name,TotalPages,TotalResults]



Cart =[Amount,ASIN,CartId,CartItem,CartItemId,CartItems,CurrencyCode,FormattedPrice,
       HMAC,ParentASIN,Price,ProductGroup,PurchaseURL,Quantity,SavedForLaterItem,SellerNickname,Title,URLEncodedHMAC]



CartNewReleases = [
    ASIN,
    Title,
]



CartTopSellers =[
    ASIN,
    Title,
]



CartSimilarities = [
    ASIN,
    OtherCategoriesSimilarProducts,
    SimilarProducts,
    SimilarViewedProducts,
    Title
]


Collections = [
    ASIN,
    Collection,
    CollectionItem,
    CollectionParent,
    Collections,
    Title,
]



EditorialReview = [
    Content,
    EditorialReviewIsLinkSuppressed,
    Source,  
]


Images = [
    Height,
    LargeImage,
    MediumImage,
    SmallImage,
    SwatchImage,
    ThumbnailImage,
    TinyImage,
    TotalPages,
    TotalResults,
    URL,
    Width, 
]




ItemAttributes = [
   Actor,
   Artist,
   AspectRatio,
   AudienceRating,
   AudioFormat,
   Author,
   Binding,
   Brand,
   CatalogNumberList,
   CatalogNumberListElement,
   Category,
   CEROAgeRating,
   ClothingSize,
   Color,
   Creator,
   Role,
   Department,
   Director,
   EAN,
   EANList,
   EANListElement,
   Edition,
   EISBN,
   EpisodeSequence,
   ESRBAgeRating,
   Feature,
   Format,
   Genre,
   HardwarePlatform,
   HazardousMaterialType,
   IsAdultProduct,
   IsAutographed,
   ISBN,
   IsEligibleForTradeIn,
   IsMemorabilia,
   IssuesPerYear,
   ItemDimensions,
       Height,
       Length,
       Weight,
       Width,
   ItemPartNumber,
   Label,
   Languages,
   Language,
   Name,
   Type,
   AudioFormat,
   LegalDisclaimer,
   ListPrice,
   MagazineType,
   Manufacturer,
   ManufacturerMaximumAge,
   ManufacturerMinimumAge,
   ManufacturerPartsWarrantyDescription,
   MediaType,
   Model,
   ModelYear,
   MPN,
   NumberOfDiscs,
   NumberOfIssues,
   NumberOfItems,
   NumberOfPages,
   NumberOfTracks,
   OperatingSystem,
   PackageDimensions,
       Height,
       Length,
       Weight,
       Width,
   PackageQuantity,
   PartNumber,
   PictureFormat,
   Platform,
   ProductGroup,
   ProductTypeName,
   ProductTypeSubcategory,
   PublicationDate,
   Publisher,
   RegionCode,
   ReleaseDate,
   RunningTime,
   SeikodoProductCode,
   ShoeSize,
   Size,
   SKU,
   Studio,
   SubscriptionLength,
   Title,
   TrackSequence,
   TradeInValue,
   UPC,
   UPCList,
       UPCListElement,
   Warranty,
   WEEETaxValue, 
]



ItemIds =[
    ASIN,
    CorrectedQuery,
    Keywords,
    Message,
    TotalPages,
    TotalResults,   
    ]


MostGifted = [
    actors,
    Artist,
    ASIN,
    Authors,
    ProductGroup,
    Title,
]



MostWishedFor = [
    Actors,
    Artist,
    ASIN,
    Authors,
    ProductGroup,
    Title, 
]



NewReleases =[
    Actors,
    Artist,
    ASIN,
    Authors,
    ProductGroup,
    Title,
    TopItemSet, 
]



OfferFull = [
    Amount,
    Availability,
    Condition,
    CurrencyCode,
    FormattedPrice,
    IsEligibleForSuperSaverShipping,
    MoreOffersURL,
    Name,
    OfferListingId,
    TotalCollectible,
    TotalNew,
    TotalOfferPages,
    TotalOffers,
    TotalRefurbished,
    TotalUsed,
]



OfferListings = [
    Amount,
    Availability,
    Code,
    Condition,
    CurrencyCode,
    FormattedPrice,
    IsEligibleForSuperSaverShipping,
    MoreOffersURL,
    Name,
    OfferListingId,
    TotalOfferPages,
    TotalOffers,
]


Offers = [
    Amount,
    Availability,
    Condition,
    CurrencyCode,
    FormattedPrice,
    IsEligibleForSuperSaverShipping,
    LoyaltyPoints,
    "???",
    Name,
    OfferListingId,
    TotalCollectible,
    TotalNew,
    TotalOfferPages,
    TotalOffers,
    TotalRefurbished,
    TotalUsed,
    ]


OfferSummary = [
    Amount,
    CurrencyCode,
    FormattedPrice,
    TotalCollectible,
    TotalNew,
    TotalRefurbished,
    TotalUsed,
]


PromotionSummary = [
    BenefitDescription,
    Category,
    EligibilityRequirementDescription,
    EndDate,
    Promotion,
    PromotionId,
    Promotions,
    StartDate,
    Summary,
    TermsAndConditions,  
]



RelatedItems =[
    ItemAttributes,
    RelatedItems,
]


Request =[
    Code,
    IsValid,
    Message,
    Name,
    RequestId,
    UserAgent,  
    
    ]


Reviews = [
    IFrameURL,
    
]


SalesRank = [
    ASIN,
    SalesRank,
    TotalPages,
    TotalResults,  
]


SearchBins = [
    BinItemCount,
    BinName,
    Name,
    SearchBinSets,
    
    
]


Similarities = [
    ASIN,
    Title,
    TotalPages,
    TotalResults,
]



TopSellers = [
    Actor,
    Artist,
    ASIN,
    Authors,
    ProductGroup,
    Title,
    TopItemSet,
    
    
]


Tracks = [
    Number,
    TotalPages,
    TotalResults,
    Track,  
]


Variations = [
    Amount,
    ASIN,
    CurrencyCode,
    FormattedPrice,
    GolfClubFlex,
    GolfClubLoft,
    
    
]


VariationImages = [
    Height,
    LargeImage,
    MediumImage,
    SmallImage,
    SwatchImage,
    ThumbnailImage,
    TinyImage,
    URL,
    Width,
]


VariationMatrix = [
    ClothingSize,
    Color,
    GemType,
    GolfClubFlex,
    GolfClubLoft,
    HardwarePlatform,
    ItemDimensions/Length,
    ItemDimensions/Width,
    MaterialType,
    MetalType,
    Model,
    OperatingSystem,
    PackageQuantity,
    ProductTypeSubcategory,
    Size,
    TotalDiamondWeight,
    TotalGemWeight,
    VariationDimension,
]


VariationOffers = [
    Amount,
    ASIN,
    Availability,
    AvailabilityAttributes,
    Condition,
    CurrencyCode,
    FormattedPrice,
    IsEligibleForSuperSaverShipping,
    LoyaltyPoints,
    MaximumHours,
    MinimumHours,
    Name,
    OfferListingId,
    TotalCollectible,
    TotalNew,
    TotalOfferPages,
    TotalOffers,
    
]


VariationSummary =[
    Amount,
    CurrencyCode,
    FormattedPrice,
    
]




# compond response group
Large = [
    Accessories,
    BrowseNodes,
    Medium,
    Offers,
    Reviews,
    Similarities,
    Tracks,
]

Medium = [
    EditorialReview,
    Images,
    ItemAttributes,
    OfferSummary,
    Request,
    SalesRank,
    Small,
]


Small = [
    Actor,
    Artist,
    ASIN,
    Author,
    CorrectedQuery,
    Creator,
    Director,
    Keywords,
    Manufacturer,
    Message,
    
    
]







class common_rp():
    def __self__(AssociateTag,AWSAccessKeyId,MarketplaceDomain='US'):
        self.AssociateTag = AssociateTag
        self.AWSAccessKeyId = AWSAccessKeyId
        self.ContentType = 'text/xml'
        
        self.MarketplaceDomain = MarketplaceDomain  # us market domain
        self.Operation = ''
        self.Service = 'AWSECommerceService'
        self.Style = 'XML'
        self.Validate = False   # if true only validation
        self.Version = '2011-08-01'
        self.XMLEscaping = 'single'
    
    def onlyamazon(self):
        self.MerchantId = 'Amazon'   # limit to amazon product only
    
class response_group(self)


def config():
    AWS_KEY = 'AKIAJ5WBUQP6NX3GEFOQ'
    SECRET_KEY = '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'
    AssociateTag='fprime-20'
    
    # call amazonproduct API wrapper
    api = API(AWS_KEY, SECRET_KEY, 'us',AssociateTag)
    
    return api    
    
def item_lookup(api,ASIN,**qargs):
    ''' Check amazon.com online inventory and price using the AWS service'''
    
    content = api.item_lookup(ASIN,ResponseGroup='Large',**qargs)
    item = content.Items.Item
    return item


def browse_node_lookup(nodeid):
    AWS_KEY = 'AKIAJ5WBUQP6NX3GEFOQ'
    SECRET_KEY = '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'
    AssociateTag='fprime-20'
    
    # call amazonproduct API wrapper
    api = API(AWS_KEY, SECRET_KEY, 'us',AssociateTag)
    

if __name__ == '__main__':
    ASIN = 'B004Z7H07K'
    api = config()
    
    qargs = {
        'Condition':'New',  #Used | Collectible | Refurbished, All
        'IdType':'ASIN',    #SKU | UPC | EAN | ISBN
        
        'ItemId':'B004Z7H07K',  # can be commoa separate list
        'MerchantId':'Amazon',  # use to limit results only by amazon
    }
    
    qargs['RelationshipType'] = 'epsolde'  #            //relation
    qargs['RelatedItemPage'] = 1           # 2,3,..etc  //page of related items
    
    qargs['IncludeReviewsSummary'] = True  #|False     // return review 
    qargs['ReviewPage'] = 1                # 2,3,..etc  //for second page , use 2
    qargs['ReviewSort'] = 'SubmissionDate'  #HelpfulVotes | HelpfulVotes | -OverallRating | OverallRating | SubmissionDate   // sort sequence
    qargs['TruncateReviewsAt'] = 1000       # 
    
    qargs['SearchIndex'] = 'shoes'  #    //can not use with the ASIN mode
    qargs['TagPage'] = 10          #     //result n perpage
    qargs['TagsPerPage'] = 2       #     //result perpage
    qargs['TagSort'] = 'Usages'    #
    
    
    qargs['VariationPage']  = 1    # 2,3  //
    
    """
if __name__ == '__main__':    
    
    print Accessories
    print 1