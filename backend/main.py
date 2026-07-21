"""
小卖部销售管理系统 - 后端
一个文件搞定：FastAPI + SQLite + 全部接口
"""
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ============================================================
# 数据库（SQLite，文件自动创建在当前目录）
# ============================================================
engine = create_engine("sqlite:///./store.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Product(Base):
    """商品表"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)        # 商品名称
    cost_price = Column(Float, nullable=False)  # 成本价
    sell_price = Column(Float, nullable=False)  # 售价
    stock = Column(Integer, default=0)          # 库存


class Sale(Base):
    """销售记录表"""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    product_name = Column(Text, nullable=False)   # 商品名称快照
    quantity = Column(Integer, nullable=False)     # 销售数量
    sell_price = Column(Float, nullable=False)     # 售价快照
    cost_price = Column(Float, nullable=False)     # 成本价快照
    profit = Column(Float, nullable=False)         # 这笔利润
    created_at = Column(Text, default=lambda: datetime.now().isoformat())


# 启动时自动建表
Base.metadata.create_all(engine)

# ============================================================
# FastAPI
# ============================================================
app = FastAPI(title="小卖部销售管理系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 请求模型
# ============================================================
class ProductCreate(BaseModel):
    name: str
    cost_price: float
    sell_price: float
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    cost_price: float | None = None
    sell_price: float | None = None
    stock: int | None = None


class SaleCreate(BaseModel):
    product_id: int
    quantity: int


# ============================================================
# 接口
# ============================================================

@app.get("/api/health")
def health():
    return {"status": "ok"}


# --- 商品 CRUD ---

@app.get("/api/products")
def get_products():
    """商品列表"""
    db = SessionLocal()
    items = db.query(Product).all()
    db.close()
    return items


@app.post("/api/products")
def create_product(p: ProductCreate):
    """新增商品"""
    db = SessionLocal()
    product = Product(name=p.name, cost_price=p.cost_price, sell_price=p.sell_price, stock=p.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return product


@app.put("/api/products/{pid}")
def update_product(pid: int, p: ProductUpdate):
    """修改商品"""
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        db.close()
        raise HTTPException(404, "商品不存在")
    if p.name is not None:
        product.name = p.name
    if p.cost_price is not None:
        product.cost_price = p.cost_price
    if p.sell_price is not None:
        product.sell_price = p.sell_price
    if p.stock is not None:
        product.stock = p.stock
    db.commit()
    db.refresh(product)
    db.close()
    return product


@app.delete("/api/products/{pid}")
def delete_product(pid: int):
    """删除商品"""
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        db.close()
        raise HTTPException(404, "商品不存在")
    db.delete(product)
    db.commit()
    db.close()
    return {"ok": True}


# --- 销售 ---

@app.post("/api/sales")
def create_sale(s: SaleCreate):
    """创建销售：扣库存 + 记录利润"""
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == s.product_id).first()
    if not product:
        db.close()
        raise HTTPException(404, "商品不存在")
    if product.stock < s.quantity:
        db.close()
        raise HTTPException(400, f"库存不足，当前库存 {product.stock}")

    profit = (product.sell_price - product.cost_price) * s.quantity
    sale = Sale(
        product_id=product.id,
        product_name=product.name,
        quantity=s.quantity,
        sell_price=product.sell_price,
        cost_price=product.cost_price,
        profit=profit,
    )
    product.stock -= s.quantity
    db.add(sale)
    db.commit()
    db.refresh(sale)
    db.close()
    return sale


@app.get("/api/sales")
def get_sales():
    """销售记录（倒序）"""
    db = SessionLocal()
    items = db.query(Sale).order_by(Sale.id.desc()).all()
    db.close()
    return items


# --- 统计 ---

@app.get("/api/stats")
def get_stats():
    """统计数据：今日 + 累计"""
    db = SessionLocal()
    today_prefix = datetime.now().strftime("%Y-%m-%d")

    today_sales = db.query(Sale).filter(Sale.created_at.like(f"{today_prefix}%")).all()
    all_sales = db.query(Sale).all()

    db.close()
    return {
        "today_revenue": sum(s.sell_price * s.quantity for s in today_sales),
        "today_profit": sum(s.profit for s in today_sales),
        "today_count": len(today_sales),
        "total_revenue": sum(s.sell_price * s.quantity for s in all_sales),
        "total_profit": sum(s.profit for s in all_sales),
        "total_count": len(all_sales),
    }
