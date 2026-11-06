# Swiss Infectious Disease Explorer

### Features
- Visualizes weekly, monthly, and yearly incidence of infectious diseases in Switzerland
- Detailed summary of data freshness for each disease
- Select custom disease subset to compare
- simple moving-window-based estimation of trends 
- Interactive and zoomable plotly plots
- Data automatically downloaded via the official FOPH API
- Protected maintenance page to manually re-download data via API

### Dependencies
- Python 3.12 
- Streamlit 1.64.0
- Plotly 7.1.0

### Dependencies Data Source
- [FOPH Infectious Disease Data API](https://www.idd.bag.admin.ch/en/portal-data).

### Installation
1. Clone the repository  
2. Create and activate a Python venv
3. Install dependencies with ```pip install -r requirements.txt```

### Set a maintenance code (facultative)
1. Create a file ```.streamlit/secrets.toml``` with one key: ```maintenancecode```
2. The value is a string with you code.
3. This is needed to access the data refresh button in running app

### Usage (Easy with VS Code)
1. Open this repo with "Open Folder..."
2. Activate virtual environment (CTRL-SHIFT-P, "Python Select Interpreter") 
3. Open a terminal and type: ```streamlit run app.py```

### Usage (With CMD terminal under windows)
1. Open cmd and navigate to root dir of this repo
3. Activate venv with ```[full-path-to-venv-dir]\Scripts\activate.bat```
4. type: ```streamlit run app.py```

### Project Structure
```text
12_infectious_desease_ch/
├── .streamlit/          # Streamlit configuration and theme
├── historical_data/     # Historical 'fall-back' data files
├── pages/               # Pages for frontend 
├── pics/                # Images and logos
├── resources/           # CSS styles and static codebooks  
├── src/                 # Data processing and reusable utilities
├── .gitignore           # Git ignore rules
├── app.py               # Main app's entry point
├── config.py            # Python config values needed by code
├── LICENSE              # MIT License
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

### Credits
- Data management and curation: [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/)
- Web-app concept, analytics and implementation by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

### License
[MIT License - © 2026 Serge Zaugg](LICENSE)





