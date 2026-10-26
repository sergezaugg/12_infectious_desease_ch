# Swiss Infectious Disease Explorer

### Features
- Visualizes weekly, monthly, and yearly incidence of 42 infectious diseases in Switzerland.
- Interactive and zoomable plots
- simple moving-window-based estimation of trends 
- Data is fetched from the official FOPH API.

### Dependencies
- Python 3.12 
- Streamlit 1.64.0
- Plotly 7.1.0

### Dependencies Data Source
- [FOPH Infectious Disease Data API](https://api.idd.bag.admin.ch/api).

### Installation
1. **Clone the repository**  
2. **Create and activate a virtual environment**  
3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

### Usage
Start the dashboard locally with:
```bash
streamlit run stmain.py
```
### Project Structure

### Credits
- Data management and curation: [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/)
- Web-app concept, analytics and implementation by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

### License
[MIT License](LICENSE)





