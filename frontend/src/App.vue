<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// ============================================================
// 数据
// ============================================================
const activeTab = ref('products')

// 商品管理
const products = ref<any[]>([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const form = ref({ id: 0, name: '', cost_price: 0, sell_price: 0, stock: 0 })

// 销售
const saleForm = ref({ product_id: null as number | null, quantity: 1 })
const saleProducts = computed(() => products.value.filter((p) => p.stock > 0))

// 销售记录
const sales = ref<any[]>([])

// 统计
const stats = ref({
  today_revenue: 0,
  today_profit: 0,
  today_count: 0,
  total_revenue: 0,
  total_profit: 0,
  total_count: 0,
})

// ============================================================
// 方法
// ============================================================
async function loadAll() {
  const [p, s, st] = await Promise.all([
    api.get('/products'),
    api.get('/sales'),
    api.get('/stats'),
  ])
  products.value = p.data
  sales.value = s.data
  stats.value = st.data
}

// --- 商品 ---
function openAdd() {
  isEditing.value = false
  form.value = { id: 0, name: '', cost_price: 0, sell_price: 0, stock: 0 }
  dialogVisible.value = true
}

function openEdit(row: any) {
  isEditing.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

async function saveProduct() {
  if (!form.value.name.trim()) {
    ElMessage.warning('请输入商品名称')
    return
  }
  if (isEditing.value) {
    await api.put(`/products/${form.value.id}`, form.value)
    ElMessage.success('修改成功')
  } else {
    await api.post('/products', form.value)
    ElMessage.success('添加成功')
  }
  dialogVisible.value = false
  await loadAll()
}

async function delProduct(row: any) {
  await ElMessageBox.confirm(`确认删除「${row.name}」？`, '提示', { type: 'warning' })
  await api.delete(`/products/${row.id}`)
  ElMessage.success('删除成功')
  await loadAll()
}

// --- 销售 ---
async function doSale() {
  if (!saleForm.value.product_id) {
    ElMessage.warning('请选择商品')
    return
  }
  if (saleForm.value.quantity < 1) {
    ElMessage.warning('数量至少为1')
    return
  }
  try {
    await api.post('/sales', saleForm.value)
    ElMessage.success('销售成功！')
    saleForm.value = { product_id: null, quantity: 1 }
    await loadAll()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '销售失败')
  }
}

// ============================================================
// 初始化
// ============================================================
onMounted(loadAll)
</script>

<template>
  <div class="app">
    <h1 class="title">小卖部销售管理系统</h1>

    <el-tabs v-model="activeTab" class="tabs">
      <!-- ================================================== -->
      <!-- Tab 1: 商品管理 -->
      <!-- ================================================== -->
      <el-tab-pane label="商品管理" name="products">
        <div class="toolbar">
          <el-button type="primary" @click="openAdd">+ 新增商品</el-button>
        </div>

        <el-table :data="products" border stripe>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="cost_price" label="成本价" width="100">
            <template #default="{ row }">¥{{ row.cost_price.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column prop="sell_price" label="售价" width="100">
            <template #default="{ row }">¥{{ row.sell_price.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column prop="stock" label="库存" width="80">
            <template #default="{ row }">
              <span :class="{ 'low-stock': row.stock <= 10 }">{{ row.stock }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button size="small" @click="openEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="delProduct(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ================================================== -->
      <!-- Tab 2: 销售 -->
      <!-- ================================================== -->
      <el-tab-pane label="销售" name="sale">
        <el-card class="sale-card">
          <h3>收银台</h3>
          <el-form label-width="80px" style="max-width: 400px">
            <el-form-item label="商品">
              <el-select
                v-model="saleForm.product_id"
                placeholder="选择商品"
                style="width: 100%"
              >
                <el-option
                  v-for="p in saleProducts"
                  :key="p.id"
                  :label="`${p.name}（库存${p.stock}）¥${p.sell_price}`"
                  :value="p.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="数量">
              <el-input-number v-model="saleForm.quantity" :min="1" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" @click="doSale">确认销售</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- ================================================== -->
      <!-- Tab 3: 销售记录 -->
      <!-- ================================================== -->
      <el-tab-pane label="销售记录" name="records">
        <el-table :data="sales" border stripe>
          <el-table-column prop="id" label="单号" width="80" />
          <el-table-column prop="product_name" label="商品" />
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column label="售价" width="100">
            <template #default="{ row }">¥{{ row.sell_price.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="利润" width="100">
            <template #default="{ row }">
              <span class="profit">¥{{ row.profit.toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="金额" width="100">
            <template #default="{ row }">¥{{ (row.sell_price * row.quantity).toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="时间" width="200">
            <template #default="{ row }">
              {{ row.created_at?.replace('T', ' ').slice(0, 19) }}
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ================================================== -->
      <!-- Tab 4: 统计 -->
      <!-- ================================================== -->
      <el-tab-pane label="统计" name="stats">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-label">今日销售额</div>
              <div class="stat-value">¥{{ stats.today_revenue.toFixed(2) }}</div>
              <div class="stat-sub">{{ stats.today_count }} 笔订单</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-label">今日利润</div>
              <div class="stat-value profit">¥{{ stats.today_profit.toFixed(2) }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-label">累计利润</div>
              <div class="stat-value profit">¥{{ stats.total_profit.toFixed(2) }}</div>
              <div class="stat-sub">共 {{ stats.total_count }} 笔</div>
            </el-card>
          </el-col>
        </el-row>

        <el-card style="margin-top: 20px">
          <div class="stat-label">累计销售额</div>
          <div class="stat-value">¥{{ stats.total_revenue.toFixed(2) }}</div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- ================================================== -->
    <!-- 商品编辑弹窗 -->
    <!-- ================================================== -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑商品' : '新增商品'"
      width="400px"
    >
      <el-form label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="如：可口可乐" />
        </el-form-item>
        <el-form-item label="成本价">
          <el-input-number v-model="form.cost_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="售价">
          <el-input-number v-model="form.sell_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="form.stock" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style>
body {
  margin: 0;
  background: #f5f5f5;
}
.app {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
}
.title {
  text-align: center;
  color: #303133;
  margin-bottom: 20px;
}
.tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}
.toolbar {
  margin-bottom: 16px;
}
.low-stock {
  color: #f56c6c;
  font-weight: bold;
}
.profit {
  color: #e6a23c;
  font-weight: bold;
}
.sale-card {
  max-width: 500px;
}
.stat-card {
  text-align: center;
  padding: 10px 0;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}
.stat-sub {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
</style>
