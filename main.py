__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from peewee import *

# Search for products based on a term
def search(term):
    
    
    lower_term = term.lower()
    search_list=[]
    q = (models.Product.select()
        .where ((models.Product.name.contains(lower_term)) | (models.Product.description.contains(lower_term))))
    if q:
        for product in q: 
            search_list.append(product.name)            
          # return f'Product: {product.name} found'
    else:
            return "No products found"
    return search_list

#View the products of a given user
def list_user_products(user_id):
    q = (models.Product.select()
    .join(models.UserProduct).join(models.User) 
    .where (models.UserProduct.user_id == user_id))

    username = models.User.get(user_id).name
  
    user_products=[]

    if q:
        print(f"User {username} has the following products: ")
        for product in q:
            #return f"- {product.name}"
            user_products.append(product.name)
    else:
        return f"No user found for: {username}"
    return user_products

#View all products for a given tag
def list_products_per_tag(tag_id):

    q = (
        models.Product.select(models.Product, models.Product_Tag, models.Tag)
        .join(models.Product_Tag, on=(models.Product_Tag.product_id == models.Product.id))
        .join(models.Tag, on=(models.Product_Tag.tag == models.Tag.id))
        .where(models.Tag.id == tag_id)
    )
      
    products_per_tag=[]
    if q:
        print(f'Tag_id: {tag_id} has the following products:')
        for product in q:
            #return f"- {product.name}"
            products_per_tag.append(product.name)
    else:
        return f"No tag found for Tag id: {tag_id}"
       
    return products_per_tag

#Add a product to a user
def add_product_to_catalog(user_id, product):
    try:
        get_product = models.Product.get(models.Product.name == product)
        get_user = models.User.get(user_id).name

    
    # Check If the product is already connected to the user
        user_product = models.UserProduct.select().where(
            models.UserProduct.user_id == user_id,
            models.UserProduct.product_id == get_product.id
            )

    
          
        if user_product:
            get_user_product =  models.UserProduct.get(
            models.UserProduct.user_id == user_id,
            models.UserProduct.product_id == get_product.id
            )
                    # Increment the quantity
            get_user_product.quantity += 1
            # print(user_product.quantity)
            get_user_product.save()
        else:
                    # Create a new UserProduct instance and save it
            models.UserProduct.create(
                user_id=user_id,
                product_id=get_product.id,
                quantity=1
            )
         
        return(f"{product} is now added to user: {get_user}.")
         
        
    except: return("No user of product are found.")


#Update stock the stock quantity of a product
def update_stock(product_id, new_quantity):
    try:
        product = models.Product.get(models.Product.id==product_id)
        models.Product.update(quantity=new_quantity).where(models.Product.id==product_id).execute()
        return f'{product.name} quantity is updated to {new_quantity}'
    except: return 'Something went wrong, stock did not update'
    

#Purchase a product. A transaction is added and the stock is updated. 
def purchase_product(product_id, buyer_id, quantity):

    try:
        product = models.Product.get(models.Product.id==product_id)
        buyer = models.User.get( models.User.id==buyer_id)
        
        models.Transaction.create(
                product = product.id,
                quantity = quantity,
                user_id = buyer.id
        )
        new_quantity = product.quantity - quantity
        update_stock(product_id, new_quantity)
      
        return f'{buyer.name} has  bought the product: {product.name} '
    except: return 'Something went wrong, transaction didnt go through'


   

#Remove product from user
def remove_product(product_id, user_id):

    try:
        user= models.User.get( models.User.id==user_id)
        product = models.Product.get(models.Product.id == product_id)
        user_product = models.UserProduct.get(
        models.UserProduct.user_id == user_id,
        models.UserProduct.product_id == product_id
        )

        # If the quantity is greater than 1
        if user_product.quantity > 1:
            # Decrement the quantity
            user_product.quantity -= 1
            user_product.save()
        else:
            # Otherwise, delete the UserProduct instance
            user_product.delete_instance()
           # product.delete_instance()
        return f'Product: {product.name} has been removed from {user.name}'

    except: return 'Something went wrong, product was not deleted'



#print(search('Phone'))
#print(search('cool'))

#print(list_user_products(3))
#print(list_products_per_tag(2))
#print(add_product_to_catalog(3,'Iphone'))
#print(update_stock(3, 4))
#print(purchase_product(4, 2, 5))
#print(remove_product(3,4))