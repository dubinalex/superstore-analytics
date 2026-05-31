"""
Superstore Sales Analysis — портфолио для Авито
Автор: Александр Дубин
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

# -------------------------------------------------------------------
# 1. Загрузка и подготовка данных
# -------------------------------------------------------------------
df = pd.read_csv('superstore_final_dataset (1).csv', encoding='latin1')
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['order_date'] = pd.to_datetime(df['order_date'], format='%d/%m/%Y')
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month

print(f"✅ Данные: {df.shape[0]} строк, {df.shape[1]} колонок")
print(f"   Период: {df['order_date'].min()} — {df['order_date'].max()}")

# -------------------------------------------------------------------
# 2. Основные метрики
# -------------------------------------------------------------------
total_sales = df['sales'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()
avg_order = total_sales / total_orders

print("\n📊 КЛЮЧЕВЫЕ МЕТРИКИ")
print(f"   Выручка:    ${total_sales:,.0f}")
print(f"   Заказов:    {total_orders}")
print(f"   Клиентов:   {total_customers}")
print(f"   Средний чек: ${avg_order:,.0f}")

# -------------------------------------------------------------------
# 3. Статистическая проверка гипотезы (ANOVA)
# -------------------------------------------------------------------
consumer = df[df['segment'] == 'Consumer']['sales']
corporate = df[df['segment'] == 'Corporate']['sales']
home = df[df['segment'] == 'Home Office']['sales']

f_stat, p_value = f_oneway(consumer, corporate, home)

print("\n📊 СТАТИСТИЧЕСКАЯ ПРОВЕРКА")
print(f"   Гипотеза: сегмент клиента влияет на сумму покупки")
print(f"   p-value = {p_value:.6f}")

if p_value < 0.05:
    print("   ➜ Влияет (различия статистически значимы)")
else:
    print("   ➜ НЕ влияет (различия статистически не значимы)")

# -------------------------------------------------------------------
# 4. График 1: Выручка по категориям
# -------------------------------------------------------------------
category_sales = df.groupby('category')['sales'].sum().sort_values()

plt.figure(figsize=(10, 6))
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
plt.barh(category_sales.index, category_sales.values, color=colors)
plt.title('Выручка по категориям товаров', fontsize=14)
plt.xlabel('Выручка ($)')
for i, v in enumerate(category_sales.values):
    plt.text(v + 5000, i, f'${v:,.0f}', va='center')
plt.tight_layout()
plt.savefig('images/category_sales.png', dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------------------
# 5. График 2: Динамика продаж по месяцам
# -------------------------------------------------------------------
monthly = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()

plt.figure(figsize=(14, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2)
plt.title('Динамика продаж по месяцам', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('images/sales_trend.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Анализ завершён. Графики сохранены в папку images/")