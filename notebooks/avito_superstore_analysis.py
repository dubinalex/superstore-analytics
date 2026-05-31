# %% [markdown]
# # Анализ продаж Superstore

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

# %%
# Загрузка данных
df = pd.read_csv('superstore_final_dataset (1).csv', encoding='latin1')
print("✅ Данные загружены")

# %%
# Чистка
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['order_date'] = pd.to_datetime(df['order_date'], format='%d/%m/%Y')
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month

print(f"Период: {df['order_date'].min()} — {df['order_date'].max()}")
print(f"Строк: {len(df)}, колонок: {len(df.columns)}")

# %%
# Метрики
total_sales = df['sales'].sum()
orders = df['order_id'].nunique()
customers = df['customer_id'].nunique()
avg_check = total_sales / orders

print(f"Выручка: ${total_sales:,.0f}")
print(f"Заказов: {orders}")
print(f"Клиентов: {customers}")
print(f"Средний чек: ${avg_check:,.0f}")

# %%
# ANOVA
consumer = df[df['segment'] == 'Consumer']['sales']
corporate = df[df['segment'] == 'Corporate']['sales']
home = df[df['segment'] == 'Home Office']['sales']

f_stat, p_value = f_oneway(consumer, corporate, home)
print(f"\nANOVA p-value = {p_value:.6f}")

if p_value < 0.05:
    print("➜ сегмент влияет на сумму покупки")
else:
    print("➜ статистически значимых различий нет")

# %%
# График по категориям
category_sales = df.groupby('category')['sales'].sum().sort_values()

plt.figure(figsize=(10, 6))
plt.barh(category_sales.index, category_sales.values, color='steelblue')
plt.title('Выручка по категориям товаров')
plt.xlabel('Выручка ($)')
plt.tight_layout()
plt.show()

# %%
# Динамика по месяцам
monthly = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()

plt.figure(figsize=(14, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o')
plt.title('Динамика продаж по месяцам')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()