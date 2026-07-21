# 小卖部销售管理系统

一个简单的小卖部进销存管理网页应用，支持多人注册、各自管理自己的店铺。

## 功能

- **用户注册/登录** — 每人独立账号，数据互不干扰
- **商品管理** — 添加、编辑、删除商品
- **销售收银** — 选择商品 → 输入数量 → 一键卖出（自动扣库存）
- **销售记录** — 查看历史销售明细
- **收入统计** — 今日/累计销售额和利润

## 本地运行

### 方式一：双击桌面上的 bat 文件（最简单）

桌面上的 `小卖部系统-一键启动.bat` → 双击即可启动。

### 方式二：命令行

**后端：**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173

## 部署

本项目支持免费部署：

- **后端** → Render
- **前端** → Vercel
- **数据库** → Supabase（免费 500MB）

部署配置已包含在项目中（`backend/Dockerfile`、`frontend/vercel.json`）。
