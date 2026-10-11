# Swiss Infectious Disease Explorer

A simple interactive app for visualizing Swiss mandatory surveillance data, using data provided weekly by the Swiss Federal Office of Public Health (FOPH).

## Features

- Visualizes weekly and monthly incidence rates of XXX diseases in Switzerland.
- Interactive plots by age, sex, region, and type.
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

TBD

## Data Source

- Data is fetched from the [FOPH Infectious Disease Data API](https://api.idd.bag.admin.ch/api).
- Official data explorer: [www.idd.bag.admin.ch/dataexplorer](https://www.idd.bag.admin.ch/dataexplorer)

## Credits

- Data management and curation: [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/)
- Dashboard by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

## License

[MIT License](LICENSE)





