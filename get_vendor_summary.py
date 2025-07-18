import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
import sqlite3
from ingestion_db import ingest_db

logging.basicConfig(
    filename = "logs/vendor_sales_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode ="a"
)

def create_vendor_summary(conn):
    vendor_sales_summary = pd.read_sql_query("""With FreightSummary as (
    select
        VendorNumber,
        sum(Freight) as FreightCost
    From vendor_invoice
    GROUP BY VendorNumber
),

PurchaseSummary as(
    select
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price as ActualPrice,
        pp.Volume,
        sum(p.Quantity) as TotalPurchaseQuantity,
        sum(p.Dollars) as TotalPurchaseDollars
    From purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    where p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
        
),

SalesSummary as (
    select
        VendorNo,
        Brand,
        sum(SalesQuantity) as TotalSalesQuantity,
        sum(SalesDollars) as TotalSalesDollars,
        sum(SalesPrice) as TotalSalesPrice,
        sum(ExciseTax) as TotalExciseTax
    from sales
    Group By VendorNo, Brand
)

select
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
from PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""",conn)
    return vendor_sales_summary


def clean_data(df):
    vendor_sales_summary['Volume'] = vendor_sales_summary['Volume'].astype('float64')
    vendor_sales_summary.fillna(0, inplace=True)
    vendor_sales_summary['VendorName']=vendor_sales_summary['VendorName'].str.strip()
    vendor_sales_summary['Description']=vendor_sales_summary['Description'].str.strip()
    
    vendor_sales_summary['GrossProfit'] = vendor_sales_summary['TotalSalesDollars']-vendor_sales_summary['TotalPurchaseDollars']
    vendor_sales_summary['ProfitMargin'] = (vendor_sales_summary['GrossProfit']/vendor_sales_summary['TotalSalesDollars'])*100
    vendor_sales_summary['StockTurnover'] = vendor_sales_summary['TotalSalesQuantity']/vendor_sales_summary['TotalPurchaseQuantity']
    vendor_sales_summary['SalestoPurchaseRatio'] = vendor_sales_summary['TotalSalesDollars']/vendor_sales_summary['TotalPurchaseDollars']
    
    return df


if __name__ == "__main__":
    
    conn = sqlite3.connect('inventory.db')
    
    logging.info('Creating Vendor Summary Table.........')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())
    
    logging.info('Cleaning Data.......')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())
    
    
    logging.info('Ingesting Data.......')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Completed')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    