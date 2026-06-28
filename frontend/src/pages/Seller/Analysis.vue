<template>
  <div class="page-wrapper">
    <div class="page-header">
      <div>
        <h1>Analysis</h1>
        <p class="subtitle">Your store performance at a glance</p>
      </div>
      <span class="last-updated">Last updated: {{ lastUpdated }}</span>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading dashboard...</p>
    </div>

    <template v-else>

      <!-- ── KPI row ── -->
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Total Products</span>
            <span class="kpi-value">{{ stats.totalProducts }}</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Portfolio Value</span>
            <span class="kpi-value">₹{{ formatNumber(stats.totalValue) }}</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Total Units</span>
            <span class="kpi-value">{{ formatNumber(stats.totalUnits) }}</span>
          </div>
        </div>

        <div class="kpi-card" :class="{ 'kpi-card--alert': stats.lowStockCount > 0 }">
          <div class="kpi-icon kpi-icon--alert">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Low Stock Items</span>
            <span class="kpi-value" :class="{ 'value--alert': stats.lowStockCount > 0 }">{{ stats.lowStockCount }}</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Avg. Price</span>
            <span class="kpi-value">₹{{ formatNumber(stats.avgPrice) }}</span>
          </div>
        </div>
      </div>

      <!-- ── Main grid ── -->
      <div class="main-grid">

        <!-- Category breakdown -->
        <div class="card">
          <div class="card-header">
            <h2>Products by Category</h2>
          </div>
          <div class="card-body">
            <div class="category-list">
              <div class="category-row" v-for="cat in stats.byCategory" :key="cat.name">
                <div class="category-meta">
                  <span class="category-name">{{ cat.name }}</span>
                  <span class="category-count">{{ cat.count }} products</span>
                </div>
                <div class="bar-track">
                  <div class="bar-fill" :style="{ width: cat.pct + '%' }"></div>
                </div>
                <span class="category-pct">{{ cat.pct }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Low stock alerts -->
        <div class="card">
          <div class="card-header">
            <h2>Inventory Alerts</h2>
            <span class="badge" :class="stats.lowStockCount > 0 ? 'badge--red' : 'badge--green'">
              {{ stats.lowStockCount > 0 ? stats.lowStockCount + ' need attention' : 'All stocked' }}
            </span>
          </div>
          <div class="card-body">
            <div v-if="stats.lowStockItems.length === 0" class="all-good">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
              <p>All products are well stocked</p>
            </div>
            <div v-else class="alert-list">
              <div class="alert-row" v-for="item in stats.lowStockItems" :key="item.id">
                <div class="alert-info">
                  <span class="alert-name">{{ item.name }}</span>
                  <span class="alert-brand">{{ item.brand }} · {{ item.category }}</span>
                </div>
                <div class="stock-pill" :class="item.stock === 0 ? 'pill--red' : 'pill--orange'">
                  {{ item.stock === 0 ? 'Out of stock' : item.stock + ' left' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Top products by value -->
        <div class="card card--full">
          <div class="card-header">
            <h2>Top Products by Inventory Value</h2>
            <span class="card-hint">price × quantity</span>
          </div>
          <div class="card-body">
            <table class="perf-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Qty</th>
                  <th>Value</th>
                  <th>Share</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(p, i) in stats.topByValue" :key="p.id">
                  <td class="rank">{{ i + 1 }}</td>
                  <td>
                    <div class="prod-cell">
                      <span class="prod-name">{{ p.name }}</span>
                      <span class="prod-brand">{{ p.brand }}</span>
                    </div>
                  </td>
                  <td><span class="cat-tag">{{ p.category }}</span></td>
                  <td>₹{{ formatNumber(p.price) }}</td>
                  <td>{{ p.stock }}</td>
                  <td class="value-cell">₹{{ formatNumber(p.value) }}</td>
                  <td>
                    <div class="share-bar-wrap">
                      <div class="share-bar" :style="{ width: p.share + '%' }"></div>
                      <span class="share-pct">{{ p.share }}%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Price distribution -->
        <div class="card">
          <div class="card-header">
            <h2>Price Distribution</h2>
          </div>
          <div class="card-body">
            <div class="price-buckets">
              <div class="bucket-row" v-for="bucket in stats.priceBuckets" :key="bucket.label">
                <span class="bucket-label">{{ bucket.label }}</span>
                <div class="bar-track">
                  <div class="bar-fill bar-fill--blue" :style="{ width: bucket.pct + '%' }"></div>
                </div>
                <span class="bucket-count">{{ bucket.count }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Stock health -->
        <div class="card">
          <div class="card-header">
            <h2>Stock Health</h2>
          </div>
          <div class="card-body">
            <div class="health-grid">
              <div class="health-item health-item--green">
                <span class="health-num">{{ stats.healthyStock }}</span>
                <span class="health-label">Healthy<br><small>qty &gt; 10</small></span>
              </div>
              <div class="health-item health-item--orange">
                <span class="health-num">{{ stats.warningStock }}</span>
                <span class="health-label">Low<br><small>qty 1–10</small></span>
              </div>
              <div class="health-item health-item--red">
                <span class="health-num">{{ stats.outOfStock }}</span>
                <span class="health-label">Out of stock<br><small>qty = 0</small></span>
              </div>
            </div>
            <div class="health-bar-strip">
              <div class="hb-green" :style="{ flex: stats.healthyStock }"></div>
              <div class="hb-orange" :style="{ flex: stats.warningStock }"></div>
              <div class="hb-red" :style="{ flex: stats.outOfStock || 0.01 }"></div>
            </div>
          </div>
        </div>

      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useProductsStore } from '@/stores/products';

export default {
  setup() {
    const productsStore = useProductsStore();
    const lastUpdated = ref('');

    const formatNumber = (n) => {
      if (n === undefined || n === null) return '0';
      return Number(n).toLocaleString('en-IN', { maximumFractionDigits: 2 });
    };

    onMounted(async () => {
      try {
        await productsStore.fetchSellerStats();
        lastUpdated.value = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
      } catch (e) {
        console.error(e);
      }
    });

    return {
      loading: computed(() => productsStore.loading),
      lastUpdated,
      stats: computed(() => productsStore.stats),
      formatNumber
    };
  }
};
</script>

<style scoped>
* { box-sizing: border-box; }

.page-wrapper {
  margin-top: 70px;
  padding: 40px 48px;
  background-color: #fafafa;
  min-height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-shrink: 0;
}

.page-header h1 { font-size: 26px; font-weight: 700; margin: 0 0 4px 0; color: #1a1a1a; }
.subtitle { font-size: 13px; color: #737373; margin: 0; }
.last-updated { font-size: 12px; color: #a3a3a3; }

/* Loading */
.loading {
  display: flex; flex-direction: column; align-items: center;
  gap: 16px; padding: 80px 0; color: #737373;
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 3px solid #f0f0f0; border-top-color: #1a1a1a;
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* KPI row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.kpi-card--alert { border-color: #fca5a5; background: #fff5f5; }

.kpi-icon {
  width: 40px; height: 40px; border-radius: 8px;
  background: #f5f5f5; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.kpi-icon svg { stroke: #1a1a1a; }
.kpi-icon--alert { background: #fee2e2; }
.kpi-icon--alert svg { stroke: #dc2626; }

.kpi-body { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.kpi-label { font-size: 11px; color: #737373; font-weight: 500; white-space: nowrap; }
.kpi-value { font-size: 20px; font-weight: 700; color: #1a1a1a; line-height: 1.2; }
.value--alert { color: #dc2626; }

/* Cards */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.card--full { grid-column: 1 / -1; }

.card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px 14px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h2 { font-size: 14px; font-weight: 700; color: #1a1a1a; margin: 0; }
.card-hint { font-size: 11px; color: #a3a3a3; }

.badge {
  font-size: 11px; font-weight: 600; padding: 3px 10px;
  border-radius: 20px;
}
.badge--red { background: #fee2e2; color: #dc2626; }
.badge--green { background: #dcfce7; color: #16a34a; }

.card-body { padding: 20px 24px; }

/* Category bars */
.category-list { display: flex; flex-direction: column; gap: 14px; }
.category-row { display: flex; align-items: center; gap: 12px; }
.category-meta { width: 140px; flex-shrink: 0; }
.category-name { display: block; font-size: 13px; font-weight: 600; color: #1a1a1a; }
.category-count { font-size: 11px; color: #a3a3a3; }

.bar-track {
  flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden;
}
.bar-fill {
  height: 100%; background: #1a1a1a; border-radius: 4px;
  transition: width 0.6s ease;
}
.bar-fill--blue { background: #3b82f6; }
.category-pct { font-size: 12px; font-weight: 600; color: #737373; width: 36px; text-align: right; }

/* Alert list */
.all-good {
  display: flex; flex-direction: column; align-items: center;
  gap: 12px; padding: 24px 0; color: #16a34a; text-align: center;
}
.all-good svg { stroke: #16a34a; }
.all-good p { font-size: 13px; margin: 0; }

.alert-list { display: flex; flex-direction: column; gap: 10px; }
.alert-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: #fafafa; border-radius: 8px;
  border: 1px solid #f0f0f0;
}
.alert-info { display: flex; flex-direction: column; gap: 2px; }
.alert-name { font-size: 13px; font-weight: 600; color: #1a1a1a; }
.alert-brand { font-size: 11px; color: #a3a3a3; }

.stock-pill {
  font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; white-space: nowrap;
}
.pill--red { background: #fee2e2; color: #dc2626; }
.pill--orange { background: #ffedd5; color: #ea580c; }

/* Performance table */
.perf-table {
  width: 100%; border-collapse: collapse; font-size: 13px;
}
.perf-table thead th {
  padding: 8px 12px; text-align: left;
  font-size: 11px; font-weight: 700; color: #737373;
  text-transform: uppercase; letter-spacing: 0.5px;
  border-bottom: 1px solid #f0f0f0;
}
.perf-table tbody tr { border-bottom: 1px solid #f9f9f9; transition: background 0.15s; }
.perf-table tbody tr:hover { background: #fafafa; }
.perf-table tbody tr:last-child { border-bottom: none; }
.perf-table td { padding: 10px 12px; vertical-align: middle; }

.rank { font-size: 12px; font-weight: 700; color: #a3a3a3; width: 28px; }
.prod-cell { display: flex; flex-direction: column; gap: 1px; }
.prod-name { font-weight: 600; color: #1a1a1a; }
.prod-brand { font-size: 11px; color: #a3a3a3; }
.cat-tag {
  display: inline-block; padding: 2px 8px;
  background: #f5f5f5; color: #737373;
  border-radius: 10px; font-size: 11px; font-weight: 500; text-transform: capitalize;
}
.value-cell { font-weight: 700; color: #1a1a1a; }

.share-bar-wrap { display: flex; align-items: center; gap: 8px; min-width: 100px; }
.share-bar { height: 6px; background: #1a1a1a; border-radius: 3px; transition: width 0.5s; }
.share-pct { font-size: 11px; color: #737373; white-space: nowrap; }

/* Price distribution */
.price-buckets { display: flex; flex-direction: column; gap: 14px; }
.bucket-row { display: flex; align-items: center; gap: 12px; }
.bucket-label { width: 110px; font-size: 12px; color: #737373; flex-shrink: 0; }
.bucket-count { font-size: 12px; font-weight: 700; color: #1a1a1a; width: 24px; text-align: right; }

/* Stock health */
.health-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.health-item {
  padding: 16px; border-radius: 10px; text-align: center;
  display: flex; flex-direction: column; gap: 4px; align-items: center;
}
.health-item--green { background: #dcfce7; }
.health-item--orange { background: #ffedd5; }
.health-item--red { background: #fee2e2; }

.health-num { font-size: 28px; font-weight: 800; line-height: 1; }
.health-item--green .health-num { color: #16a34a; }
.health-item--orange .health-num { color: #ea580c; }
.health-item--red .health-num { color: #dc2626; }

.health-label { font-size: 11px; font-weight: 600; color: #555; text-align: center; line-height: 1.4; }
.health-label small { font-weight: 400; color: #a3a3a3; }

.health-bar-strip {
  display: flex; height: 8px; border-radius: 4px; overflow: hidden; gap: 2px;
}
.hb-green { background: #16a34a; border-radius: 4px; }
.hb-orange { background: #ea580c; border-radius: 4px; }
.hb-red { background: #dc2626; border-radius: 4px; }

/* Responsive */
@media (max-width: 1100px) {
  .kpi-row { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 860px) {
  .main-grid { grid-template-columns: 1fr; }
  .card--full { grid-column: auto; }
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .page-wrapper { padding: 20px 14px; }
  .kpi-row { grid-template-columns: 1fr; }
}
</style>