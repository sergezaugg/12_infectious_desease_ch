# Swiss Influenza Monitoring Visualization

A simple interactive dashboard for visualizing Swiss influenza surveillance data, using data provided weekly by the Swiss Federal Office of Public Health (FOPH).

## Features

- Visualizes weekly incidence rates of influenza (flu) in Switzerland.
- Supports the mandatory reporting ("oblig") data sources.
- Interactive plots by age, sex, region, and influenza type.
- Customizable color schemes and area plot thresholds.
- Data is fetched live from the official FOPH API.

## Installation

1. **Download or clone the repository**  
2. **Create and activate a virtual environment**  
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   # or 
   pip install --upgrade -r requirements.txt
   ```

## Usage

Start the dashboard locally with:

```bash
streamlit run stmain.py
```

The app will automatically download the latest data from the FOPH API and display interactive plots.

## Project Structure

- `stmain.py` – Main Streamlit entry point and navigation.
- `page00.py` – Main visualization page.
- `page01.py` – Color settings page.
- `page02.py` – Credits and background info.
- `utils.py` – Data fetching, preprocessing, and plotting utilities.
- `meta_data/` – Metadata JSON files for each data source.
- `pics/` – Logo images.
- `.streamlit/` – Streamlit configuration.

## Data Source

- Data is fetched from the [FOPH Infectious Disease Data API](https://api.idd.bag.admin.ch/api).
- Official data explorer: [www.idd.bag.admin.ch/dataexplorer](https://www.idd.bag.admin.ch/dataexplorer)

## Credits

- Data management and curation: [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/)
- Dashboard by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

## License

[MIT License](LICENSE)





