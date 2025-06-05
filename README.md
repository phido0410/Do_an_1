
# ⚽ Football Analysis Project

## 📖 Overview

**Football Analysis Project** is a comprehensive football analytics application built with Python and Streamlit. It offers interactive dashboards and insights into team and player performance, along with detailed match shotmaps using data from **SofaScore** and **StatsBomb**.

## 🎯 Key Features

### 1. Team Statistics
- Retrieve team data from SofaScore API
- Analyze seasonal performance metrics
- Display top players by goals, assists, tackles
- Visualize insights with dynamic charts

### 2. Player Performance Analysis
- Analyze last 5-match performance
- Use average ratings and key indicators
- Visualize stats: passes, goals, ratings
- Categorize player roles (Forward, Midfielder, Defender)

### 3. Match Analysis via Shotmap
- Utilize StatsBomb event data
- Visualize shots on a football pitch
- Analyze both teams' shooting actions
- Display match stats and final score

## 🏗️ Project Structure

```
Do_an_1/
├── Data/                          
├── Phongdocauthu/                 
│   ├── Đánh giá cầu thủ 5 trận gần nhất/
│   │   ├── danhgiacauthu.ipynb
│   │   ├── Crawldatacauthu.py
│   │   └── 151545_last5.csv
│   └── Streamlit_danhgia_phongdo_cauthu/
│       ├── app2.py
│       └── backup.py
├── Shotmap/
│   ├── Crawl_and_draw_shotmaps 2/
│   └── Streamlit_shotmap/
│       └── main3.py
├── Thongketoandoi/
│   ├── Thống kê toàn đội trong 1 mùa giải_2/
│   │   └── thongke.ipynb
│   └── Streanlit_thongke_toandoi_trongmuagiai/
│       └── app.py
└── Streamlit_final/
    └── appfinal.py
```

## 🚀 Installation & Usage

### Requirements
- Python 3.8+
- Libraries: `streamlit`, `pandas`, `matplotlib`, `requests`, `statsbombpy`, `mplsoccer`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application

#### 1. Final integrated app (recommended)
```bash
streamlit run Streamlit_final/appfinal.py
```

#### 2. Run individual modules
```bash
# Player performance
streamlit run Phongdocauthu/Streamlit_danhgia_phongdo_cauthu/app2.py

# Team statistics
streamlit run Thongketoandoi/Streanlit_thongke_toandoi_trongmuagiai/app.py

# Match shotmap
streamlit run Shotmap/Streamlit_shotmap/main3.py
```

## 📊 Usage Guide

### Team Statistics
- Select team or enter team ID
- Choose league and season
- Click "Lấy dữ liệu" to fetch API data
- View top players and charts

### Player Performance
- Input player ID
- Enter last 5 match IDs (comma-separated)
- System:
  - Crawls API
  - Creates CSV
  - Displays analysis & charts

### Shotmap Analysis
- Choose league and season (StatsBomb)
- Filter and select match
- Enter Match ID
- View interactive shotmap and stats

## 🔧 API & Data

### SofaScore API
- Host: `sofascore.p.rapidapi.com`
- Used for player/team stats
- Endpoints:
  - `/matches/get-player-statistics`
  - `/teams/get-statistics`

### StatsBomb API
- Used for match event and shotmap data
- Library: `statsbombpy`

## 📈 Analytics Metrics

### Player Stats
- `totalPass`, `accuratePass`, `keyPass`, `goals`, `rating`, `tackles`, `assists`

### Performance Rating
- **High (≥ 7.0)**: Green
- **Average (6.0 – 6.9)**: Orange
- **Low (< 6.0)**: Red-orange

## 🎨 UI & Visualization

### Visuals
- Bar charts
- Multi-axis plots
- Football pitch shotmaps
- Color-coded charts

### UI Features
- Sidebar menus with icons
- Team logos as ID hints
- Banner/video background
- Responsive layout

## 📝 Advanced Features

### Data Management
- Auto CSV generation by ID
- Handle NaN and missing values
- Export/import supported

### Error Handling
- API connection checks
- User input validation
- Detailed error messages

### Optimization
- Streamlit caching (`@st.cache_data`)
- Session state
- Lazy loading

## 🔮 Future Development
- ML-based match prediction
- Cross-team player comparisons
- Trend analysis over time
- Multi-source data integration

### Technical Enhancements
- Database support
- Real-time streaming
- Mobile design
- Multi-language UI

## 🤝 Contribution

Developed by a dedicated football analytics team. Contributions and feedback are welcome!

## 📄 License

This project is intended for academic and research purposes.

---

For questions or feedback, feel free to open an issue or contact the dev team.
