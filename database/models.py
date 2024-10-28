# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 28, 2024 05:38:51
# Database: sqlite:////tmp/tmp.uUGSzp95b9/thos_idea/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Category(SAFRSBaseX, Base):
    """
    description: Represents categories for products.
    """
    __tablename__ = 'category'
    _s_collection_name = 'Category'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="category")



class Customer(SAFRSBaseX, Base):
    """
    description: Stores information about customers.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    credit_limit = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Employee(SAFRSBaseX, Base):
    """
    description: Contains employee details.
    """
    __tablename__ = 'employee'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Product(SAFRSBaseX, Base):
    """
    description: Contains information about products available for orders.
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="product")
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="product")
    ItemList : Mapped[List["Item"]] = relationship(back_populates="product")



class Store(SAFRSBaseX, Base):
    """
    description: Represents physical store locations.
    """
    __tablename__ = 'store'
    _s_collection_name = 'Store'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="store")



class Supplier(SAFRSBaseX, Base):
    """
    description: Stores supplier details for products.
    """
    __tablename__ = 'supplier'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="supplier")



class Inventory(SAFRSBaseX, Base):
    """
    description: Tracks inventory levels for products at different store locations.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    store_id = Column(ForeignKey('store.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))
    store : Mapped["Store"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Represents orders placed by customers.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    order_date = Column(DateTime)
    notes = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    ItemList : Mapped[List["Item"]] = relationship(back_populates="order")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="order")



class ProductCategory(SAFRSBaseX, Base):
    """
    description: Links products with categories.
    """
    __tablename__ = 'product_category'
    _s_collection_name = 'ProductCategory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    category_id = Column(ForeignKey('category.id'))

    # parent relationships (access parent)
    category : Mapped["Category"] = relationship(back_populates=("ProductCategoryList"))
    product : Mapped["Product"] = relationship(back_populates=("ProductCategoryList"))

    # child relationships (access children)



class ProductSupplier(SAFRSBaseX, Base):
    """
    description: Links products with suppliers.
    """
    __tablename__ = 'product_supplier'
    _s_collection_name = 'ProductSupplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    supplier_id = Column(ForeignKey('supplier.id'))
    supply_price = Column(Float)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductSupplierList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("ProductSupplierList"))

    # child relationships (access children)



class Item(SAFRSBaseX, Base):
    """
    description: Represents items included in orders.
    """
    __tablename__ = 'item'
    _s_collection_name = 'Item'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ItemList"))
    product : Mapped["Product"] = relationship(back_populates=("ItemList"))

    # child relationships (access children)



class Shipment(SAFRSBaseX, Base):
    """
    description: Details shipments for orders.
    """
    __tablename__ = 'shipment'
    _s_collection_name = 'Shipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    shipment_date = Column(DateTime)
    tracking_number = Column(String)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShipmentList"))

    # child relationships (access children)
