# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    response.flash = T("Welcome to the NailIt Hardware Store!")
    return dict(message=T('Hello World'))
    
@auth.requires_login()
def placeOrder():
    userid = auth.user.id
    datime = request.now
    amount = 0
    get_sendLine_url = URL('sendLine')
    get_placeOrder_url = URL('placeMyOrder')
    purchaseId = db.purchases.insert(customerID=userid, 
	datePurchased=datime,total=amount)
	
    form = SQLFORM(db.itemsBought, 
	submit_button='d',
	buttons=[])
    get_price_url = URL('get_price')
    productNames = db().select(db.product.name)  
    return locals()
    
def sendLine():
    #Add code to add stuff to the database!
    purchase_id = request.vars.id or 2000
    in_price = request.vars.price or ''
    in_quant = request.vars.quantity or ''
    in_product = db(db.product.name == request.vars.product).select()[0] or ''
    in_quantity = request.vars.quantity or ''
    
    try: msg=db.itemsBought.insert(purchaseID=purchase_id, price=in_price,
	quantity=in_quantity, product=in_product) or "not"
    except: msg = "ex" + purchase_id
    else:msg = "else"
    quant_left = update_inventory(in_product, in_quant)
    return response.json(quant_left)
    
def placeMyOrder():
    purchase_id = request.vars.id or 2000
    in_total = request.vars.total or 0
    
    purchase = db(db.purchases.id == purchase_id).select()[0]
    purchase.total = in_total
    purchase.update_record()
    
    redirect(URL('index'))
    return response.json(dict(my_msg=in_total))
    
def get_price():
    """
    URI targeted by ajax request to retrieve price for selected product
    """
    print("get_price called for: ")
    productName  = request.vars.product
    print(productName)
    # get price from data base
    price = db(db.product.name == productName).select(db.product.price)[0].price
    print ("price retrieved from db:")
    print(price)
    return (price)
    
def update_inventory(product, requestedQu):
    #productName = request.vars.product
    #requestedQu = request.vars.quantity
    
    inventoryLeft = product.inStock - int(requestedQu)
    if inventoryLeft >= 0:
        # enough inventory 
        # update DAL object productInventory
        product.inStock = inventoryLeft
        # record updated DAL object in db
        product.update_record()
    return (inventoryLeft)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
