"""
小卖部销售管理系统 - 后端
FastAPI + PostgreSQL/SQLite + JWT认证
"""
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import engine, get_db
from models import Base, User, Product, Sale

# ============================================================
# 初始化
# ============================================================
Base.metadata.create_all(engine)

app = FastAPI(title="小卖部销售管理系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# ============================================================
# 工具函数
# ============================================================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401)
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(401)
        return user
    except JWTError:
        raise HTTPException(401, "登录已过期，请重新登录")


# ============================================================
# 请求模型
# ============================================================
class RegisterRequest(BaseModel):
    username: str
    password: str
    store_name: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


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


class BatchSaleItem(BaseModel):
    product_id: int
    quantity: int


class BatchSaleCreate(BaseModel):
    items: list[BatchSaleItem]


# ============================================================
# 健康检查（无需登录）
# ============================================================
@app.get("/api/health")
def health():
    return {"status": "ok"}


# ============================================================
# 认证接口（无需登录）
# ============================================================
@app.post("/api/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if len(req.username) < 2:
        raise HTTPException(400, "用户名至少2个字符")
    if len(req.password) < 4:
        raise HTTPException(400, "密码至少4个字符")
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(400, "用户名已被注册")

    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        store_name=req.store_name or req.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "username": user.username}


@app.post("/api/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(400, "用户名或密码错误")
    return {"token": create_token(user.id), "username": user.username}


# ============================================================
# 商品管理（需要登录）
# ============================================================
@app.get("/api/products")
def get_products(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Product).filter(Product.user_id == user.id).all()


@app.post("/api/products")
def create_product(
    p: ProductCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = Product(
        user_id=user.id,
        name=p.name,
        cost_price=p.cost_price,
        sell_price=p.sell_price,
        stock=p.stock,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.put("/api/products/{pid}")
def update_product(
    pid: int,
    p: ProductUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == pid, Product.user_id == user.id).first()
    if not product:
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
    return product


@app.delete("/api/products/{pid}")
def delete_product(
    pid: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == pid, Product.user_id == user.id).first()
    if not product:
        raise HTTPException(404, "商品不存在")
    db.delete(product)
    db.commit()
    return {"ok": True}


# ============================================================
# 销售（需要登录）
# ============================================================
@app.post("/api/sales")
def create_sale(
    s: SaleCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == s.product_id, Product.user_id == user.id).first()
    if not product:
        raise HTTPException(404, "商品不存在")
    if product.stock < s.quantity:
        raise HTTPException(400, f"库存不足，当前库存 {product.stock}")

    profit = (product.sell_price - product.cost_price) * s.quantity
    sale = Sale(
        user_id=user.id,
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
    return sale


@app.post("/api/sales/batch")
def create_batch_sale(
    batch: BatchSaleCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = []
    total_profit = 0.0
    for item in batch.items:
        product = db.query(Product).filter(Product.id == item.product_id, Product.user_id == user.id).first()
        if not product:
            raise HTTPException(404, f"商品 {item.product_id} 不存在")
        if product.stock < item.quantity:
            raise HTTPException(400, f"「{product.name}」库存不足，当前库存 {product.stock}")

        profit = (product.sell_price - product.cost_price) * item.quantity
        total_profit += profit
        sale = Sale(
            user_id=user.id,
            product_id=product.id,
            product_name=product.name,
            quantity=item.quantity,
            sell_price=product.sell_price,
            cost_price=product.cost_price,
            profit=profit,
        )
        product.stock -= item.quantity
        db.add(sale)
        results.append({
            "product_name": product.name,
            "quantity": item.quantity,
            "sell_price": product.sell_price,
            "profit": round(profit, 2),
        })

    db.commit()
    return {"items": results, "total_profit": round(total_profit, 2), "total_count": len(batch.items)}


@app.get("/api/sales")
def get_sales(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Sale).filter(Sale.user_id == user.id).order_by(Sale.id.desc()).all()


# ============================================================
# 统计（需要登录）
# ============================================================
@app.get("/api/stats")
def get_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today_prefix = datetime.now().strftime("%Y-%m-%d")
    today_sales = (
        db.query(Sale)
        .filter(Sale.user_id == user.id, Sale.created_at.like(f"{today_prefix}%"))
        .all()
    )
    all_sales = db.query(Sale).filter(Sale.user_id == user.id).all()

    return {
        "today_revenue": sum(s.sell_price * s.quantity for s in today_sales),
        "today_profit": sum(s.profit for s in today_sales),
        "today_count": len(today_sales),
        "total_revenue": sum(s.sell_price * s.quantity for s in all_sales),
        "total_profit": sum(s.profit for s in all_sales),
        "total_count": len(all_sales),
    }
