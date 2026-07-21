# 小卖部销售管理系统

一个简单易用的 Web 销售管理系统，专为小卖部、便利店老板设计。

## 功能

- 用户注册登录
- 商品管理（增删改查）
- 销售订单（自动扣库存 + 利润计算）
- 库存流水记录
- 数据统计（销售额、利润、趋势图、热销排行）

## 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue3 + Vite + TypeScript + Element Plus |
| 后端 | Python FastAPI + SQLAlchemy |
| 数据库 | PostgreSQL (Supabase) |
| 部署 | Vercel（前端）+ Render（后端） |

## 本地开发

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL（或使用 Supabase 远程数据库）

### 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`，自动代理 API 请求到后端 `http://localhost:8000`。

## 项目状态

🚧 MVP 开发中

- [x] Phase 0-A: 项目初始化
- [ ] Phase 0-B: Docker + CI/CD
- [ ] Phase 1: 用户系统
- [ ] Phase 2: 商品管理
- [ ] Phase 3: 销售系统
- [ ] Phase 4: 数据统计
- [ ] Phase 5: 部署上线
