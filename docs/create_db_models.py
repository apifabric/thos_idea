# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    """description: Stores information about customers."""
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    credit_limit = Column(Float, nullable=True)

class Order(Base):
    """description: Represents orders placed by customers."""
    __tablename__ = 'order'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(String, nullable=True)

class Item(Base):
    """description: Represents items included in orders."""
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

class Product(Base):
    """description: Contains information about products available for orders."""
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

class Supplier(Base):
    """description: Stores supplier details for products."""
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_info = Column(String, nullable=True)

class ProductSupplier(Base):
    """description: Links products with suppliers."""
    __tablename__ = 'product_supplier'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    supply_price = Column(Float)

class Category(Base):
    """description: Represents categories for products."""
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)

class ProductCategory(Base):
    """description: Links products with categories."""
    __tablename__ = 'product_category'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

class Employee(Base):
    """description: Contains employee details."""
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)

class Store(Base):
    """description: Represents physical store locations."""
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)

class Inventory(Base):
    """description: Tracks inventory levels for products at different store locations."""
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

class Shipment(Base):
    """description: Details shipments for orders."""
    __tablename__ = 'shipment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    shipment_date = Column(DateTime, nullable=True)
    tracking_number = Column(String, nullable=True)

# Create the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Sample data
customer1 = Customer(name='John Doe', email='johndoe@example.com', phone='1234567890', address='123 Elm Street', credit_limit=5000.0)
customer2 = Customer(name='Jane Smith', email='janesmith@example.com', phone='0987654321', address='456 Oak Avenue', credit_limit=3000.0)

product1 = Product(name='Widget', description='A standard widget', price=10.0)
product2 = Product(name='Gadget', description='An advanced gadget', price=25.0)

order1 = Order(customer_id=1, notes='Please pack carefully.')
order2 = Order(customer_id=2)

item1 = Item(order_id=1, product_id=1, quantity=2, unit_price=10.0)
item2 = Item(order_id=1, product_id=2, quantity=1, unit_price=25.0)
item3 = Item(order_id=2, product_id=1, quantity=5, unit_price=10.0)

supplier1 = Supplier(name='ABC Supplies', contact_info='contact@abcsupplies.com')
supplier2 = Supplier(name='XYZ Industries', contact_info='info@xyzindustries.com')

product_supplier1 = ProductSupplier(product_id=1, supplier_id=1, supply_price=5.0)
product_supplier2 = ProductSupplier(product_id=2, supplier_id=2, supply_price=18.0)

category1 = Category(name='Home', description='Items for home use')
category2 = Category(name='Office', description='Office supplies and equipment')

product_category1 = ProductCategory(product_id=1, category_id=1)
product_category2 = ProductCategory(product_id=2, category_id=2)

employee1 = Employee(first_name='Alice', last_name='Brown', title='Manager')
employee2 = Employee(first_name='Bob', last_name='Smith', title='Sales Associate')

store1 = Store(name='Main Store', location='Downtown')
store2 = Store(name='Outlet Store', location='Airport')

inventory1 = Inventory(store_id=1, product_id=1, quantity=100)
inventory2 = Inventory(store_id=2, product_id=2, quantity=50)

shipment1 = Shipment(order_id=1, shipment_date=datetime.datetime.now(), tracking_number='TRACK12345')
shipment2 = Shipment(order_id=2, shipment_date=datetime.datetime.now(), tracking_number='TRACK67890')

# Add all instances to the session
session.add_all([customer1, customer2, product1, product2, order1, order2, item1, item2, item3, supplier1, supplier2, 
                 product_supplier1, product_supplier2, category1, category2, product_category1, product_category2, 
                 employee1, employee2, store1, store2, inventory1, inventory2, shipment1, shipment2])

# Commit the session
session.commit()
