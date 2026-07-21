# 小卖部销售管理系统

一个简单易用的本地销售管理 Demo。

## 功能

- 商品管理（增删改查）
- 销售记录（自动扣库存 + 利润计算）
- 销售统计（今日/累计销售额、利润）

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue3 + Vite + TypeScript + Element Plus |
| 后端 | Python FastAPI + SQLAlchemy |
| 数据库 | SQLite（零配置，文件自动创建） |

## 本地运行

### 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

后端运行在 `http://localhost:8000`

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`，自动代理 API 请求到后端。

### 使用

1. 打开浏览器访问 `http://localhost:5173`
2. 在「商品管理」Tab 添加商品
3. 在「销售」Tab 选择商品并卖出
4. 在「销售记录」Tab 查看历史
5. 在「统计」Tab 查看销售额和利润
