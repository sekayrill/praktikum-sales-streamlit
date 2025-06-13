import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Dashboard Penjualan - Superstore")

# Load dan Preprocessing Data
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding='latin1')

    # Konversi tanggal
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

    # Kolom waktu tambahan
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Year'] = df['Order Date'].dt.year

    # Hapus duplikat & data kosong
    df = df.drop_duplicates()
    df = df.dropna()

    # Pastikan kolom numerik
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    return df

df = load_data()

# =====================
#  FILTER KATEGORI
# =====================
kategori_terpilih = st.sidebar.multiselect(
    " Pilih Kategori Produk:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Terapkan filter kategori
filtered_df = df[df["Category"].isin(kategori_terpilih)]

# =====================
#  TAMPILKAN DATA
# =====================
st.subheader("Data Penjualan")
st.dataframe(filtered_df)

# =====================
#  TREND PENJUALAN BULANAN
# =====================
st.subheader("Trend Penjualan Bulanan")
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(monthly_sales["Month"], monthly_sales["Sales"], marker='o', linestyle='-')
ax1.set_title("Penjualan Bulanan")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Total Penjualan")
plt.xticks(rotation=45)
st.pyplot(fig1)

# =====================
#  PROFITABILITAS PER KATEGORI
# =====================
st.subheader("Profitabilitas per Kategori Produk")
category_profit = filtered_df.groupby("Category")["Profit"].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(category_profit["Category"], category_profit["Profit"], color='skyblue')
ax2.set_title("Total Profit per Kategori")
ax2.set_xlabel("Kategori")
ax2.set_ylabel("Total Profit")
st.pyplot(fig2)

# =====================
#  METRIK TOTAL PROFIT
# =====================
total_profit = filtered_df['Profit'].sum()
st.metric("Total Profit", f"${total_profit:,.2f}")
