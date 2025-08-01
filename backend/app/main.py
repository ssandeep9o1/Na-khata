from fastapi import FastAPI
from app.api.v1.routers import shops, customers, products, transactions, notes

# Create the main FastAPI application instance
app = FastAPI(title="na-khata API")

# Include the shops router
app.include_router(
    shops.router,
    prefix="/api/v1/shops",
    tags=["Shops"]
)

# Include the customers router
app.include_router(
    customers.router,
    prefix="/api/v1/customers",
    tags=["Customers"]
)

# Include the products router
app.include_router(
    products.router,
    prefix="/api/v1/products",
    tags=["Products"]
)

# Include the transactions router
app.include_router(
    transactions.router,
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)

# Include the notes router
app.include_router(
    notes.router,
    prefix="/api/v1/notes",
    tags=["Notes"]
)


# A simple root endpoint for a health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the na-khata API"}