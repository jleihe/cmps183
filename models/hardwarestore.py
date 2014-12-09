#Supplier
db.define_table('supplier',
    Field('name', 'string', requires=(IS_NOT_EMPTY(),
	IS_NOT_IN_DB(db, 'supplier.name'))),
    Field('address', 'string', requires=IS_NOT_EMPTY()),
    format='%(name)s')

#Products
#Referse to supplier
db.define_table('product',
    Field('name', 'string',
	requires=(IS_NOT_IN_DB(db, 'product.name'))),
    Field('inStock', 'integer', requires=IS_NOT_EMPTY()),
    Field('price', 'double', requires=IS_NOT_EMPTY()),
    Field('onOrder', 'integer'),
    Field('supplier', db.supplier),
    format='%(name)s')

#Contacts
#Access a suppliers contacts by selecting all contacts for which the
#supplierID is a match
db.define_table('contact',
    Field('name', 'string', requires=(IS_NOT_EMPTY(),
	IS_NOT_IN_DB(db, 'contact.name'))),
    Field('supplierID', 'integer', requires=(IS_NOT_EMPTY(),
	IS_IN_DB(db, 'supplier.id'))),
    Field('phone', 'string'),
    Field('email', 'string', requires=(IS_EMPTY_OR(IS_EMAIL()))),
    Field('description', 'string'),
    format='%(name)s')

#Costomer
#Purchases that a "costomer" makes are stored in purchases under the 
#customerID
db.define_table('customer',
    Field('name', 'string', requires=(IS_NOT_EMPTY(),
	IS_NOT_IN_DB(db, 'customer.name'))),
    Field('phone', 'string'),
    Field('email', 'string', requires=(IS_EMPTY_OR(IS_EMAIL()))),
    format='%(name)s')

#Purchases
#Access a customer's purchases by selecting all purchases for which the
#customerID is a match
db.define_table('purchases',
    Field('customerID', 'integer', requires=(IS_NOT_EMPTY(),
	IS_IN_DB(db, 'customer.id'))),
    Field('datePurchased', 'date', requires=IS_NOT_EMPTY()),
    Field('total', 'double'),
    format='%(name)s')

#Items Bought
#Referse to product
#Access all items in a purchase by selecting itemsBought for which the
#purchaseID is a match
db.define_table('itemsBought',
    Field('purchaseID', 'integer', IS_IN_DB(db, 'purchases.id')),
    Field('price', 'double', requires=IS_NOT_EMPTY()),
    Field('quantity', 'integer', requires=IS_NOT_EMPTY()),
    Field('product', db.product),
    format='%(name)s')
db.itemsBought.purchaseID.writable = False
db.itemsBought.purchaseID.readable = False
