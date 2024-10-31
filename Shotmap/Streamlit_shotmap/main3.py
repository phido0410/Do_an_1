import streamlit as st
from statsbombpy import sb
from pandas import json_normalize
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import pandas as pd
import numpy as np

# Chèn ảnh banner
st.image(
    "https://baohagiang.vn/file/4028eaa4679b32c401679c0c74382a7e/4028eaa57d592b24017d5a5e979736bf/092022/image001_20220908082711.jpg",
    use_column_width=True
)

# Tiêu đề chính
st.title("Phân Tích Trận Đấu Bóng Đá")
st.write("Chào mừng bạn đến với trang phân tích trận đấu bóng đá! Tại đây, bạn có thể lấy dữ liệu từ StatsBomb và phân tích các cú sút của các đội bóng.")

# Hàm cache để lưu dữ liệu đã lấy về nhằm tối ưu hóa
@st.cache_data
def load_matches(competition_id, season_id):
    st.write("Đang tải dữ liệu trận đấu...")
    return sb.matches(competition_id=competition_id, season_id=season_id)

# Khởi tạo biến trạng thái để theo dõi các bước
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "filter_done" not in st.session_state:
    st.session_state.filter_done = False

# Nút "Lấy dữ liệu từ StatsBomb"
if st.button("Lấy dữ liệu từ StatsBomb"):
    st.write("Đang lấy dữ liệu từ StatsBomb...")
    competitions_data = sb.competitions()
    #competitions_df = pd.DataFrame(competitions_data) Không hiển thị dữ liệu sau khi lấy
    st.success("Dữ liệu đã được lấy thành công")
    #st.write(competitions_df) Không hiển thị dữ liệu sau khi lấy

    st.session_state.data_loaded = True  # Đánh dấu đã tải dữ liệu

# Hiển thị các tùy chọn nếu đã tải dữ liệu
if st.session_state.data_loaded:
    st.write("Hãy chắc chắn rằng bạn đã chọn đúng giải đấu và mùa giải, nếu không chọn gì mặc định sẽ là Bundesliga 2023/2024.")
    # Gợi ý Competition ID với tên giải đấu và logo
    competition_options = {
        "Bundesliga - ID: 9": (9, "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark"),
        "Premier League - ID: 2": (2, "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark"),
        # Thêm các giải đấu khác ở đây
    }

    competition_display = list(competition_options.keys())
    competition_choice = st.selectbox("Chọn Competition:", competition_display, index=0)
    competition_id = competition_options[competition_choice][0]
    competition_logo_url = competition_options[competition_choice][1]
    st.image(competition_logo_url, caption=competition_choice.split(" - ")[0], use_column_width=False)

    # Gợi ý Season ID
    season_options = {
        "Bundesliga 2023/2024 - ID: 281": 281,
        "Premier League 2015/2016 - ID: 27": 27,
        # Thêm các mùa giải khác ở đây
    }
    season_display = list(season_options.keys())
    season_choice = st.selectbox("Chọn Season:", season_display, index=0)
    season_id = season_options[season_choice]

    # Nút lọc dữ liệu giải đấu và mùa giải
    if st.button("Lọc dữ liệu giải đấu và mùa giải"):
        st.write("Lọc dữ liệu giải đấu và mùa giải...")
        matches_df = load_matches(competition_id, season_id)
        st.write("Dữ liệu các trận đấu đã lọc:", matches_df)

        st.session_state.filter_done = True  # Đánh dấu đã lọc dữ liệu

# Hiển thị phần nhập Match ID nếu đã lọc dữ liệu
if st.session_state.filter_done:
    st.write("Coppy Match ID từ bảng trên để xem thông tin trận đấu.")
    st.subheader("Nhập ID Trận Đấu")
    match_id = st.text_input("Vui lòng nhập Match ID:")
    if match_id and st.button("Xử lý dữ liệu trận đấu"):
        events = sb.events(match_id=int(match_id))
        df = json_normalize(events, sep='_')
        df = pd.DataFrame(events)

        # Lọc tên của 2 đội bóng
        unique_teams = df['team'].unique()
        if len(unique_teams) == 2:
            Tendoi1, Tendoi2 = unique_teams
            st.success(f"Trận đấu giữa {Tendoi1} và {Tendoi2}")

            # Lọc thông số những cú sút từ 2 đội
            Doi1_shots = df[(df['type'] == 'Shot') & (df['team'] == Tendoi1)]
            Doi2_shots = df[(df['type'] == 'Shot') & (df['team'] == Tendoi2)]

            # Vẽ biểu đồ những cú sút
            st.subheader("Biểu Đồ Cú Sút")
            st.write("Dưới đây là biểu đồ thể hiện các cú sút của hai đội trong trận đấu:")
            # Thiết lập sân bóng
            pitch = Pitch()
            # specifying figure size (width, height)
            fig, ax = pitch.draw(figsize=(15.6, 10.4))
            fig.set_facecolor('black')
            ax.patch.set_facecolor('black')
            pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)  # optional stripes
            pitch.draw(ax=ax)

            # Đếm số cú sút và số cú sút thành bàn của mỗi đội
            Doi1_total_shots = len(Doi1_shots['id'])
            Doi1_goals = Doi1_shots[Doi1_shots['shot_outcome'] == 'Goal'].shape[0]

            Doi2_total_shots = len(Doi2_shots['id'])
            Doi2_goals = Doi2_shots[Doi2_shots['shot_outcome'] == 'Goal'].shape[0]

            # Loop through đội 1
            for x in range(len(Doi1_shots['id'])):
                if Doi1_shots['period'].iloc[x] == 1 or Doi1_shots['period'].iloc[x] == 2:
                    size = np.sqrt(Doi1_shots['shot_statsbomb_xg'].iloc[x]) * 200
                    if Doi1_shots['shot_outcome'].iloc[x] == 'Goal':
                        plt.plot(
                            [Doi1_shots['location'].iloc[x][0], Doi1_shots['shot_end_location'].iloc[x][0]],
                            [Doi1_shots['location'].iloc[x][1], Doi1_shots['shot_end_location'].iloc[x][1]],
                            color='blue'
                        )
                        plt.scatter(Doi1_shots['location'].iloc[x][0], Doi1_shots['location'].iloc[x][1], s=size, color='blue')
                    else:
                        plt.plot(
                            [Doi1_shots['location'].iloc[x][0], Doi1_shots['shot_end_location'].iloc[x][0]],
                            [Doi1_shots['location'].iloc[x][1], Doi1_shots['shot_end_location'].iloc[x][1]],
                            color='red'
                        )
                        plt.scatter(Doi1_shots['location'].iloc[x][0], Doi1_shots['location'].iloc[x][1], s=size, color='red')

            # Loop through đội 2
            for x in range(len(Doi2_shots['id'])):
                if Doi2_shots['period'].iloc[x] == 1 or Doi2_shots['period'].iloc[x] == 2:
                    size = np.sqrt(Doi2_shots['shot_statsbomb_xg'].iloc[x]) * 200
                    if Doi2_shots['shot_outcome'].iloc[x] == 'Goal':
                        plt.plot(
                            [120 - Doi2_shots['location'].iloc[x][0], 120 - Doi2_shots['shot_end_location'].iloc[x][0]],
                            [80 - Doi2_shots['location'].iloc[x][1], 80 - Doi2_shots['shot_end_location'].iloc[x][1]],
                            color='blue'
                        )
                        plt.scatter(120 - Doi2_shots['location'].iloc[x][0], 80 - Doi2_shots['location'].iloc[x][1], s=size, color='blue')
                    else:
                        plt.plot(
                            [120 - Doi2_shots['location'].iloc[x][0], 120 - Doi2_shots['shot_end_location'].iloc[x][0]],
                            [80 - Doi2_shots['location'].iloc[x][1], 80 - Doi2_shots['shot_end_location'].iloc[x][1]],
                            color='red'
                        )
                        plt.scatter(120 - Doi2_shots['location'].iloc[x][0], 80 - Doi2_shots['location'].iloc[x][1], s=size, color='red')

            # Lấy tên đội từ Doi1_shots và Doi2_shots
            team1_name = Doi1_shots['team'].iloc[0]
            team2_name = Doi2_shots['team'].iloc[0]

            # Thiết lập tiêu đề với tên đội từ Doi1_shots và Doi2_shots cùng với tỉ số
            plt.title(f'{team2_name} Shots (Bên Trái) vs {team1_name} Shots (Bên Phải)\n Tỉ Số: {team1_name} {Doi1_goals} - {Doi2_goals} {team2_name}', color='white', size=20)

            # Chú thích cho tia màu xanh dương
            # Thêm nền cho chú thích
            plt.text(100, 90, 
                    'Chú thích: Tia màu Xanh dương là Cú sút thành bàn\n'
                    'Tia màu đỏ là những cú sút về hướng về khung thành', 
                    color='white', 
                    fontsize=12, 
                    ha='center', 
                    bbox=dict(facecolor='blue', alpha=0.5, boxstyle='round,pad=0.5'))  # Thêm nền cho chú thích

            # Hiển thị biểu đồ
            st.pyplot(fig)
