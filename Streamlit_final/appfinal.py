import streamlit as st
import pandas as pd
import requests
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from statsbombpy import sb
from pandas import json_normalize
import numpy as np

# Tiêu đề và banner
st.title("Phân Tích Bóng Đá")
st.write("Nghe nhạc cho đỡ chán nha!")
st.video("https://www.youtube.com/watch?v=Bz9dbGWbtpQ")
st.markdown("### Chào mừng đến với ứng dụng phân tích bóng đá")

# Thêm ghi chú
st.write("""
Ghi chú:
- Ứng dụng này bao gồm ba tính năng chính: phân tích trận đấu, so sánh đội bóng và dự đoán kết quả.
- Hãy chọn tính năng ở menu bên trái để bắt đầu.
""")

# Cải tiến sidebar với tiêu đề và các biểu tượng
st.sidebar.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔍 Football Analysis Menu</h1>", unsafe_allow_html=True)
st.sidebar.write("### Chọn một tính năng để bắt đầu phân tích:")

# Thêm khoảng cách cho tính năng
st.sidebar.markdown("___")  # Phân tách đường ngang
option = st.sidebar.radio(
    "Chọn tính năng",
    ("⚽ THỐNG KÊ DỮ LIỆU ĐỘI BÓNG", 
     "📊 MÔ HÌNH ĐÁNH GIÁ PHONG ĐỘ CẦU THỦ", 
     "📈 PHÂN TÍCH TRẬN ĐẤU BẰNG SHOTMAP")
)

# Thêm dòng phân cách cho phần thoáng đãng hơn
st.sidebar.markdown("___")

# Định nghĩa từng ứng dụng
def analyze_match():
    st.subheader("Phân Tích Toàn Bộ Đội Bóng Trong Mùa Giải")
    # Thêm code của phần phân tích trận đấu
    # Hàm để lấy dữ liệu từ API
    def get_team_data(team_id, tournament_id, season_id):
        url = f"https://sofascore.p.rapidapi.com/teams/get-player-statistics?teamId={team_id}&tournamentId={tournament_id}&seasonId={season_id}&type=overall"
        headers = {
            'x-rapidapi-host': 'sofascore.p.rapidapi.com',
            'x-rapidapi-key': '5fa1b3ec61msh748c83f0ec34ff4p18fe14jsn062670fd057e'  # Thay thế bằng API key của bạn
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to retrieve data: {response.status_code}")
            return None
    # Gợi ý kèm theo URL logo
    teams = {
        "Liverpool - 44": "https://api.sofascore.app/api/v1/team/44/image",
        "Manchester City - 17": "https://api.sofascore.app/api/v1/team/17/image",
        "Arsenal - 42": "https://api.sofascore.app/api/v1/team/42/image",
        "Chelsea - 38": "https://api.sofascore.app/api/v1/team/38/image",
        "Tottenham - 33": "https://api.sofascore.app/api/v1/team/33/image",
        "Manchester United - 35": "https://api.sofascore.app/api/v1/team/35/image",
        "Real Madrid - 2829": "https://api.sofascore.app/api/v1/team/2829/image",
        "Barcelona - 2817": "https://api.sofascore.app/api/v1/team/2817/image",
        "Alentico Madrid - 2836": "https://api.sofascore.app/api/v1/team/2836/image",
        "Bayern Munich - 2672": "https://api.sofascore.app/api/v1/team/2672/image",
        "Borussia Dortmund - 2673": "https://api.sofascore.app/api/v1/team/2673/image",
        "Bayern Leverkusen - 2681": "https://api.sofascore.app/api/v1/team/2681/image",
        "Juventus - 2687": "https://api.sofascore.app/api/v1/team/2687/image",
        "AC Milan - 2692": "https://api.sofascore.app/api/v1/team/2692/image",
        "Inter Milan - 2697": "https://api.sofascore.app/api/v1/team/2697/image",
        "Napoli - 2714": "https://api.sofascore.app/api/v1/team/2714/image",
        "Paris Saint-Germain - 1644": "https://api.sofascore.app/api/v1/team/1644/image",
        "Inter Miami - 337602": "https://api.sofascore.app/api/v1/team/337602/image",
        "Al Nass - 23400": "https://api.sofascore.app/api/v1/team/23400/image",
        "Al Hilal - 21895": "https://api.sofascore.app/api/v1/team/21895/image",
        "Al Ittihad - 34315": "https://api.sofascore.app/api/v1/team/34315/image",


    }

    tournaments = {
        "UEFA Champions League - 7": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "Premier League - 17": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "La Liga - 8": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "Bundesliga - 35": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Serie A - 23": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "V-League - 626": "https://api.sofascore.app/api/v1/unique-tournament/626/image/dark",
        "mls - 242": "https://api.sofascore.app/api/v1/unique-tournament/242/image/dark",
        "saudi-professional-league - 955": "https://api.sofascore.app/api/v1/unique-tournament/955/image/dark",
    }

    seasons = {
        "UEFA Champions League 2024/2025 - 61644": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "UEFA Champions League 2023/2024 - 52162": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "UEFA Champions League 2022/2023 - 41897": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "UEFA Champions League 2021/2022 - 36886": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "UEFA Champions League 2020/2021 - 29267": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
        "Premier League 2024/2025 - 61627": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "Premier League 2023/2024 - 52186": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "Premier League 2022/2023 - 41886": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "Premier League 2021/2022 - 37036": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "Premier League 2020/2021 - 29415": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
        "La Liga 2024/2025 - 61643": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "La Liga 2023/2024 - 52376": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "La Liga 2022/2023 - 42409": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "La Liga 2021/2022 - 37223": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "La Liga 2020/2021 - 32501": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
        "Bundesliga 2024/2025 - 63516": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Bundesliga 2023/2024 - 52608": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Bundesliga 2022/2023 - 42268": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Bundesliga 2021/2022 - 37166": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Bundesliga 2020/2021 - 28210": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
        "Serie A 2024/2025 - 63515": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "Serie A 2023/2024 - 52760": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "Serie A 2022/2023 - 42415": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "Serie A 2021/2022 - 37475": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "Serie A 2020/2021 - 32523": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
        "Ligue 1 2024/2025 - 61736": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
        "Ligue 1 2023/2024 - 52571": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
        "Ligue 1 2022/2023 - 42273": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
        "Ligue 1 2021/2022 - 37167": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
        "Ligue 1 2020/2021 - 28222": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
        "Mls 2024/2025 - 57317": "https://api.sofascore.app/api/v1/unique-tournament/242/image/dark",
        "Saudi-professional-league 2024/2025 - 63998": "https://api.sofascore.app/api/v1/unique-tournament/955/image/dark",  
    }

    # Thiết lập giao diện
    st.image("https://e0.365dm.com/23/06/2048x1152/skysports-premier-league-fixtures_6187020.jpg?20230614111423", use_column_width=True) # Ảnh banner bóng đá
    st.title("⚽THỐNG KÊ DỮ LIỆU ĐỘI BÓNG⚽")

    st.markdown("""
        **Chào mừng bạn đến với trang thống kê bóng đá!**
        Hãy nhập các thông tin cần thiết và chúng tôi sẽ lấy dữ liệu về đội bóng của bạn.
    """)
    st.markdown("""
        **Hướng dẫn:**
        - Mỗi tùy chọn bao gồm tên và ID, được phân cách bởi dấu " - ".
        - Ví dụ: Nếu bạn chọn "Liverpool - 44", thì ID của Liverpool là **44**.
        - ID này sẽ được sử dụng để truy xuất dữ liệu từ API.
        - Hãy chắc chắn rằng đội bóng của bạn ở đúng giải đấu và mùa giải bạn chọn.
    """)

    # Hiển thị gợi ý id đội bóng kèm logo và cho phép chọn
    with st.expander("Gợi ý id đội bóng:"):
        team_options = []
        for team, logo_url in teams.items():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(logo_url, width=50)
            with col2:
                st.markdown(team)
            team_options.append(team)
        st.markdown("<h4 style='color: #0072B8;'>Chọn đội bóng:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
        selected_team = st.selectbox("🟢 Chọn đội bóng", team_options, index=0)  # Thêm biểu tượng

    # Hiển thị gợi ý id giải đấu kèm logo và cho phép chọn
    with st.expander("Gợi ý id giải đấu:"):
        tournament_options = []
        for tournament, logo_url in tournaments.items():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(logo_url, width=50)
            with col2:
                st.markdown(tournament)
            tournament_options.append(tournament)
        st.markdown("<h4 style='color: #0072B8;'>Chọn giải đấu:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
        selected_tournament = st.selectbox("🟢 Chọn giải đấu", tournament_options, index=0)  # Thêm biểu tượng

    # Hiển thị gợi ý id mùa giải kèm logo và cho phép chọn
    with st.expander("Gợi ý id mùa giải:"):
        season_options = []
        for season, logo_url in seasons.items():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(logo_url, width=50)
            with col2:
                st.markdown(season)
            season_options.append(season)
        st.markdown("<h4 style='color: #0072B8;'>Chọn mùa giải:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
        selected_season = st.selectbox("🟢 Chọn mùa giải", season_options, index=0)  # Thêm biểu tượng


    # Tách ID từ lựa chọn của người dùng
    team_id_from_select = selected_team.split(" - ")[-1]
    tournament_id_from_select = selected_tournament.split(" - ")[-1]
    season_id_from_select = selected_season.split(" - ")[-1]

    # Giao diện chọn thông tin đội bóng với ID tự động điền từ lựa chọn
    st.markdown("### Nhập ID thủ công hoặc sử dụng từ gợi ý:")

    team_id = st.text_input("Nhập team ID:", value=team_id_from_select)
    tournament_id = st.text_input("Nhập tournament ID (Giải đấu):", value=tournament_id_from_select)
    season_id = st.text_input("Nhập season ID (Mùa giải):", value=season_id_from_select)

    # Hiển thị thông tin đã chọn
    st.write(f"Bạn đã chọn đội bóng từ gợi ý: {selected_team}")
    st.write(f"Giải đấu từ gợi ý: {selected_tournament}")
    st.write(f"Mùa giải từ gợi ý: {selected_season}")
    st.write("HÃY KIỂM TRA KĨ ĐỘI BÓNG CỦA BẠN CÓ CHƠI Ở GIẢI ĐẤU VÀ MÙA GIẢI BẠN CHỌN KHÔNG!")

    # Khi nhấn nút "Lấy Dữ Liệu"
    if st.button("Lấy Dữ Liệu"):
        # Ưu tiên giá trị nhập thủ công, nếu không có sẽ dùng từ gợi ý
        final_team_id = team_id if team_id else team_id_from_select
        final_tournament_id = tournament_id if tournament_id else tournament_id_from_select
        final_season_id = season_id if season_id else season_id_from_select

        if final_team_id and final_tournament_id and final_season_id:
            with st.spinner('Đang tải dữ liệu...'):
                data = get_team_data(final_team_id, final_tournament_id, final_season_id)

                # Kiểm tra nếu không có dữ liệu trả về
                if not data or 'topPlayers' not in data:
                    st.error("Không có dữ liệu cho đội bóng, giải đấu hoặc mùa giải đã chọn. Vui lòng kiểm tra lại.")
                else:
                    player_stats = {}
                    keys = ['rating', 'goals', 'assists', 'totalShots', 'shotsOnTarget',
                            'accuratePasses', 'keyPasses', 'accurateLongBalls',
                            'successfulDribbles', 'tackles', 'interceptions']

                    for key in keys:
                        for player_info in data.get('topPlayers', {}).get(key, []):
                            player = player_info.get('player', {})
                            statistics = player_info.get('statistics', {})
                            player_name = player.get('name')

                            if player_name not in player_stats:
                                player_stats[player_name] = {
                                    'name': player_name,
                                    'position': player.get('position'),
                                    'type': statistics.get('type'),
                                    'appearances': statistics.get('appearances')
                                }

                            player_stats[player_name][key] = statistics.get(key)

                    # Tạo tập hợp các khóa duy nhất
                        fieldnames = set()
                        for stats in player_stats.values():
                            fieldnames.update(stats.keys())
                        fieldnames = list(fieldnames)

                    # Lưu dữ liệu vào file CSV
                    file_name = f"{final_team_id}_{final_tournament_id}_{final_season_id}.csv"
                    with open(file_name, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(player_stats.values())

                    st.success(f"Dữ liệu đã được crawl và lưu vào file {file_name}")

                    # Hiển thị file dữ liệu vừa crawl
                    data_df = pd.DataFrame(player_stats.values())
                    st.write(data_df.head())

                    # Phần thống kê cả mùa
                    st.title('📊 Thống Kê Cầu Thủ Mùa Giải 📊')

                    # Input for file name
                    file_name_input = st.text_input("Tự động phân tích dữ liệu", value=file_name)

                    if file_name_input:
                        try:
                            # Load data
                            data = pd.read_csv(file_name_input)

                            # Convert data types
                            data['assists'] = pd.to_numeric(data['assists'], errors='coerce')
                            data['keyPasses'] = pd.to_numeric(data['keyPasses'], errors='coerce')
                            data['goals'] = pd.to_numeric(data['goals'], errors='coerce')
                            data['tackles'] = pd.to_numeric(data['tackles'], errors='coerce')

                            # Tạo báo cáo thống kê
                            report = {
                                'Total Goals': data['goals'].sum(),
                                'Total Assists': data['assists'].sum(),
                                'Total Key Passes': data['keyPasses'].sum(),
                                'Total Tackles': data['tackles'].sum(),
                            }

                            # Tạo biểu đồ cho các chỉ số tổng quát
                            fig, ax1 = plt.subplots(figsize=(10, 6))

                            # Biểu đồ cho Goals và Assists
                            goals_bars = ax1.bar(['Total Goals', 'Total Assists'], 
                                                [report['Total Goals'], report['Total Assists']], 
                                                color=['blue', 'orange'], alpha=0.7)
                            ax1.set_ylabel('Goals & Assists', color='black', fontsize=12)
                            ax1.tick_params(axis='y', labelcolor='black')
                            ax1.set_ylim(0, max(report['Total Goals'], report['Total Assists']) * 1.2)

                            # Thêm giá trị lên trên các cột của Goals và Assists
                            for bar in goals_bars:
                                yval = bar.get_height()
                                ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, 
                                        f'{yval:.0f}', ha='center', va='bottom', fontsize=10, color='black')

                            # Tạo một trục y thứ hai cho Key Passes và Tackles
                            ax2 = ax1.twinx()
                            tackles_bars = ax2.bar(['Total Key Passes', 'Total Tackles'], 
                                                    [report['Total Key Passes'], report['Total Tackles']], 
                                                    color=['green', 'red'], alpha=0.7, width=0.4, align='edge')
                            ax2.set_ylabel('Key Passes & Tackles', color='black', fontsize=12)
                            ax2.tick_params(axis='y', labelcolor='black')
                            ax2.set_ylim(0, max(report['Total Key Passes'], report['Total Tackles']) * 1.2)

                            # Thêm giá trị lên trên các cột của Key Passes và Tackles
                            for bar in tackles_bars:
                                yval = bar.get_height()
                                ax2.text(bar.get_x() + bar.get_width()/2, yval + 1, 
                                        f'{yval:.0f}', ha='center', va='bottom', fontsize=10, color='black')

                            # Vẽ đường ngăn cách giữa các nhóm cột
                            plt.axvline(x=1.5, color='black', linestyle='--', linewidth=1)

                            # Thiết lập tiêu đề và hiển thị biểu đồ
                            plt.title('Báo Cáo Thống Kê Chỉ Số Của Toàn Đội Trong Mùa Giải', fontsize=16, fontweight='bold', color='navy')
                            plt.grid(axis='y', linestyle='--', alpha=0.7)
                            plt.tight_layout()

                            # Hiển thị biểu đồ
                            st.pyplot(fig)

                            # Get top 3 players for each category
                            top_scorers = data.nlargest(3, 'goals')
                            top_assist_providers = data.nlargest(3, 'assists')
                            top_key_passes = data.nlargest(3, 'keyPasses')
                            top_tacklers = data.nlargest(3, 'tackles')

                            # Function to plot bar charts for top players
                            def plot_top_players(top_players, stat, title, color):
                                fig, ax = plt.subplots()
                                bars = ax.bar(top_players['name'], top_players[stat], color=color, edgecolor='black', linewidth=1.5)
                                ax.set_title(title, fontsize=16, fontweight='bold', color='navy')
                                ax.set_ylabel(stat.capitalize(), fontsize=14)
                                ax.set_ylim(0, top_players[stat].max() * 1.2)
                                ax.grid(axis='y', linestyle='--', alpha=0.7)
                                for bar in bars:
                                    yval = bar.get_height()
                                    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom', fontsize=12, color='black')
                                st.pyplot(fig)

                            # Top 3 Goals
                            st.header('⚽ Top 3 Cầu Thủ Có Bàn Thắng Cao Nhất ⚽')
                            st.write(top_scorers[['name', 'goals', 'rating']])
                            plot_top_players(top_scorers, 'goals', 'Top 3 Cầu Thủ Có Bàn Thắng Cao Nhất', 'purple')

                            # Top 3 Assists
                            st.header('🎯 Top 3 Cầu Thủ Kiến Tạo Nhiều Nhất 🎯')
                            st.write(top_assist_providers[['name', 'assists', 'rating']])
                            plot_top_players(top_assist_providers, 'assists', 'Top 3 Cầu Thủ Kiến Tạo Nhiều Nhất', 'orange')

                            # Top 3 Key Passes
                            st.header('📊 Top 3 Cầu Thủ Có Đường Chuyền Chính Xác Nhiều Nhất 📊')
                            st.write(top_key_passes[['name', 'keyPasses', 'rating']])
                            plot_top_players(top_key_passes, 'keyPasses', 'Top 3 Cầu Thủ Có Đường Chuyền Chính Xác Nhiều Nhất', 'green')

                            # Top 3 Tackles
                            st.header('🛡️ Top 3 Cầu Thủ Có Số Pha Tắc Bóng Cao Nhất 🛡️')
                            st.write(top_tacklers[['name', 'tackles', 'rating']])
                            plot_top_players(top_tacklers, 'tackles', 'Top 3 Cầu Thủ Có Số Pha Tắc Bóng Cao Nhất', 'red')

                        except Exception as e:
                            st.error(f"Có lỗi xảy ra khi đọc file: {e}")

def compare_teams():
    st.subheader("ĐÁNH GIÁ PHONG ĐỘ CẦU THỦ")
    # Thêm code của ĐÁNH GIÁ PHONG ĐỘ CẦU THỦ
    # Thông tin RapidAPI
    RAPIDAPI_HOST = "sofascore.p.rapidapi.com"
    RAPIDAPI_KEY = "5fa1b3ec61msh748c83f0ec34ff4p18fe14jsn062670fd057e"

    # Hàm để lấy dữ liệu từ RapidAPI
    def get_player_statistics(match_id, player_id):
        url = f"https://sofascore.p.rapidapi.com/matches/get-player-statistics?matchId={match_id}&playerId={player_id}"
        headers = {
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi kết nối tới API: {e}")
            return None

    # Hàm để phân loại vị trí cầu thủ
    def classify_position(pos):
        position_map = {
            'F': 'Tiền đạo',
            'M': 'Tiền vệ',
            'D': 'Hậu vệ'
        }
        return position_map.get(pos, 'Khác')

    # Tiêu đề ứng dụng
    st.title("MÔ HÌNH ĐÁNH GIÁ PHONG ĐỘ CẦU THỦ")
    st.image("https://static.bongda24h.vn/medias/standard/2018/9/10/FIFPro-va-55-cau-thu-xuat-sac-nhat-the-gioi-mua-giai-201718-hinh-anh.jpg", use_column_width=True)

    # Nhập ID cầu thủ và ID trận đấu
    player_id = st.text_input("Nhập ID cầu thủ:")
    match_ids = st.text_input("Nhập 5 ID trận đấu (ngăn cách bằng dấu phẩy):")

    # Nút lấy dữ liệu
    if st.button("Lấy dữ liệu"):
        if player_id and match_ids:
            match_ids_list = match_ids.split(",")
            file_name = f"{player_id}_last5.csv"

            # Mở file CSV để ghi dữ liệu
            with open(file_name, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "match_id", "name", "height", "team", "position", "totalPass", "accuratePass", "totalLongBalls", 
                    "accurateLongBalls", "totalCross", "aerialLost", "aerialWon", "duelLost", "duelWon", 
                    "challengeLost", "dispossessed", "totalContest", "wonContest", "onTargetScoringAttempt", 
                    "blockedScoringAttempt", "goals", "wasFouled", "fouls", "totalOffside", "minutesPlayed", 
                    "touches", "rating", "possessionLostCtrl", "keyPass", "expectedAssists"
                ])
                writer.writeheader()

                for match_id in match_ids_list:
                    data = get_player_statistics(match_id.strip(), player_id)
                    if data:  # Kiểm tra xem dữ liệu có hợp lệ không
                        row = {
                            "match_id": match_id.strip(),
                            "name": data.get("player", {}).get("name", ""),
                            "height": data.get("player", {}).get("height", ""),
                            "team": data.get("team", {}).get("name", ""),
                            "position": data.get("player", {}).get("position", ""),
                            "totalPass": data.get("statistics", {}).get("totalPass", 0),
                            "accuratePass": data.get("statistics", {}).get("accuratePass", 0),
                            "totalLongBalls": data.get("statistics", {}).get("totalLongBalls", 0),
                            "accurateLongBalls": data.get("statistics", {}).get("accurateLongBalls", 0),
                            "totalCross": data.get("statistics", {}).get("totalCross", 0),
                            "aerialLost": data.get("statistics", {}).get("aerialLost", 0),
                            "aerialWon": data.get("statistics", {}).get("aerialWon", 0),
                            "duelLost": data.get("statistics", {}).get("duelLost", 0),
                            "duelWon": data.get("statistics", {}).get("duelWon", 0),
                            "challengeLost": data.get("statistics", {}).get("challengeLost", 0),
                            "dispossessed": data.get("statistics", {}).get("dispossessed", 0),
                            "totalContest": data.get("statistics", {}).get("totalContest", 0),
                            "wonContest": data.get("statistics", {}).get("wonContest", 0),
                            "onTargetScoringAttempt": data.get("statistics", {}).get("onTargetScoringAttempt", 0),
                            "blockedScoringAttempt": data.get("statistics", {}).get("blockedScoringAttempt", 0),
                            "goals": data.get("statistics", {}).get("goals", 0),
                            "wasFouled": data.get("statistics", {}).get("wasFouled", 0),
                            "fouls": data.get("statistics", {}).get("fouls", 0),
                            "totalOffside": data.get("statistics", {}).get("totalOffside", 0),
                            "minutesPlayed": data.get("statistics", {}).get("minutesPlayed", 0),
                            "touches": data.get("statistics", {}).get("touches", 0),
                            "rating": data.get("statistics", {}).get("rating", 0),
                            "possessionLostCtrl": data.get("statistics", {}).get("possessionLostCtrl", 0),
                            "keyPass": data.get("statistics", {}).get("keyPass", 0),
                            "expectedAssists": data.get("statistics", {}).get("expectedAssists", 0)
                        }
                        writer.writerow(row)
                        st.success(f"Đã hoàn thành lấy dữ liệu cho trận đấu {match_id.strip()}")
                    else:
                        st.error(f"Lỗi khi lấy dữ liệu cho trận đấu {match_id.strip()}")

            # Đọc file CSV
            player_data = pd.read_csv(file_name)

            # Lọc các chỉ số cần thiết bao gồm cả vị trí
            filtered_data = player_data[['name', 'match_id', 'position', 'totalPass', 'accuratePass', 'keyPass', 'goals', 'rating']].copy()

            # Xử lý dữ liệu NaN
            filtered_data.fillna(0, inplace=True)  # Thay thế NaN bằng 0

            if 'name' in filtered_data.columns and 'position' in filtered_data.columns:
                # Lấy tên cầu thủ và phân loại vị trí
                player_name = filtered_data['name'][0]  # Tên cầu thủ
                position = filtered_data['position'][0]   # Vị trí cầu thủ
                position_description = classify_position(position)  # Phân loại vị trí

                # Cập nhật tên cầu thủ để bao gồm thông tin vị trí
                player_name_with_position = f"{player_name} ({position_description})"

                # Đánh giá phong độ cầu thủ
                avg_rating = filtered_data['rating'].mean()
                if avg_rating < 6:
                    evaluation = "Phong độ Thấp: Cầu thủ thể hiện phong độ kém."
                    color = "#ff6347"  # Màu đỏ cam cho phong độ thấp
                elif 6 <= avg_rating < 7:
                    evaluation = "Phong độ Ổn định: Cầu thủ thể hiện phong độ trung bình."
                    color = "#ffa500"  # Màu cam cho phong độ ổn định
                else:
                    evaluation = "Phong độ Cao: Cầu thủ thể hiện phong độ tốt."
                    color = "#32cd32"  # Màu xanh lá cho phong độ cao

                # Hiển thị đánh giá
                st.subheader("Đánh giá cầu thủ:")
                st.markdown(
                    f"""
                    <div style='padding: 20px; border: 2px solid {color}; border-radius: 10px; background-color: #f0f8ff;'>
                        <h1 style='color: {color}; text-align: center; font-weight: bold;'>{evaluation}</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # Vẽ biểu đồ cho từng chỉ số
                x_labels = [f'Trận đấu {i+1}' for i in range(len(filtered_data))]
                
                metrics = {
                    'totalPass': 'Total Passes',
                    'accuratePass': 'Accurate Passes',
                    'keyPass': 'Key Passes',
                    'goals': 'Goals',
                    'rating': 'Rating'
                }
                
                colors = {
                    'totalPass': 'blue',
                    'accuratePass': 'orange',
                    'keyPass': 'royalblue',
                    'goals': 'mediumseagreen',
                    'rating': 'purple'
                }
                
                for metric, label in metrics.items():
                    plt.figure(figsize=(10, 6))
                    bars = plt.bar(x_labels, filtered_data[metric], color=colors[metric], edgecolor='black')
                    plt.title(f'{label} per Match - {player_name_with_position}', fontsize=16, fontweight='bold')
                    plt.xlabel('Trận đấu', fontsize=12)
                    plt.ylabel(label, fontsize=12)
                    plt.xticks(rotation=45, fontsize=10)
                    plt.grid(axis='y', linestyle='--', alpha=0.7)
                    for bar in bars:
                        yval = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)
                    plt.tight_layout()
                    st.pyplot(plt)

                # Tạo dữ liệu cho biểu đồ
                evaluation_labels = ['Rating trung bình']
                evaluation_scores = [avg_rating]

                # Biểu đồ cột cho đánh giá cầu thủ
                plt.figure(figsize=(6.5, 5))
                bars = plt.bar(evaluation_labels, evaluation_scores, color='lightblue', edgecolor='black')

                # Thiết lập tiêu đề và nhãn
                plt.title(f'Phong độ {player_name_with_position} - 5 trận gần nhất', fontsize=14, fontweight='bold')
                plt.ylabel('Giá trị', fontsize=14)
                plt.ylim(0, 10)

                # Thiết lập bước nhảy cho trục Y là 1
                plt.yticks(range(0, 11), fontsize=12)

                # Thêm đường tham chiếu
                plt.axhline(7.0, color='blue', linestyle='--', label='Mức cao')
                plt.axhline(5.5, color='red', linestyle='--', label='Mức ổn định')

                # Hiển thị số liệu trên đỉnh cột
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=12)

                # Thêm chú thích
                plt.legend(fontsize=12)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(plt)
            else:
                st.error("Dữ liệu không chứa thông tin về tên hoặc vị trí cầu thủ.")
        else:
            st.warning("Vui lòng nhập ID cầu thủ và ID trận đấu.")


def predict_outcome():
    st.subheader("PHÂN TÍCH BIỂU ĐỒ SHOTMAP")
    # Thêm code của PHÂN TÍCH BIỂU ĐỒ SHOTMAP
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


if option == "⚽ THỐNG KÊ DỮ LIỆU ĐỘI BÓNG":
    analyze_match()
elif option == "📊 MÔ HÌNH ĐÁNH GIÁ PHONG ĐỘ CẦU THỦ":
    compare_teams()
elif option == "📈 PHÂN TÍCH TRẬN ĐẤU BẰNG SHOTMAP":
    predict_outcome()