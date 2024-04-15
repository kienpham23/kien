import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")

# Tiêu đề trang
st.markdown("<h1 style='font-size:30px;'>Interactive Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:30px;'>Interact with this dashboard using the widgets on the sidebar</h2>", unsafe_allow_html=True)

# Phân chia layout thành hai cột
left_column, right_column = st.columns(2)

# Sidebar
st.sidebar.markdown("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
range_values = st.sidebar.slider("Choose a range:", min_value=1.00, max_value=10.00, value=(2.50, 7.50))

st.sidebar.markdown(" Select your preferred genre(s) and year to view the movies released that year and on that genre ")
genres = movies_data['genre'].unique()
selected_genres = st.sidebar.multiselect("Choose Genre:", genres)

st.sidebar.markdown("### Filter by Year")
years = sorted(movies_data['year'].unique())
selected_year = st.sidebar.selectbox("Choose a Year:", years)


# Lọc dữ liệu dựa trên các yếu tố được chọn
filtered_data = movies_data[(movies_data['genre'].isin(selected_genres)) &
                            (movies_data['year'] == selected_year)]

# Hiển thị bảng dữ liệu
filtered_data = filtered_data.reset_index(drop=True)
filtered_data['year'] = filtered_data['year'].astype(str)
with left_column:
    st.write("### Lists of movies filtered by year and Genre")
    st.dataframe(filtered_data[['name', 'genre', 'year']])

# Biểu đồ line  

# Lọc dữ liệu dựa trên các yếu tố được chọn
filtered_data = movies_data[(movies_data["score"] >= range_values[0]) & 
                            (movies_data["score"] <= range_values[1])]

# Tính toán điểm trung bình của mỗi thể loại từ dữ liệu đã lọc
sum_score_filtered = filtered_data.groupby('genre')['score'].sum()
# Hiển thị biểu đồ thống kê với tổng số điểm của tất cả các phim trong mỗi thể loại và dữ liệu đã lọc
with right_column:
    st.write("### Total User Score of Movies in Each Genre")
    if not sum_score_filtered.empty:
        fig = px.line(x=sum_score_filtered.index, y=sum_score_filtered.values, labels={'x':'Genre', 'y':' Score'})
        fig.update_xaxes(tickangle=45)
        fig.update_layout(width=500, height=400, margin=dict(l=50, r=50, t=50, b=50), xaxis=dict(tickvals=sum_score_filtered.index, ticktext=sum_score_filtered.index))  # Thêm lề cho biểu đồ
        st.plotly_chart(fig)

# Xóa các dòng có giá trị NaN
movies_data.dropna(inplace=True)

# Hiển thị biểu đồ cột Matplotlib
st.write("""Average Movie Budget, Grouped by Genre""")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']
fig = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud, color='maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre', fontsize=20)
st.pyplot(fig)
