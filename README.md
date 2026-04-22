# SDG Analysis: Urbanization vs Air Pollution (PM2.5)

A data visualization project exploring the relationship between urban population growth and PM2.5 air pollution across countries, built as part of a college data visualization course.

## Files

| File | Description |
|------|-------------|
| `urban.csv` | Raw urban population data from World Bank |
| `pm25.csv` | Raw PM2.5 air pollution data from World Bank |
| `dv_project-data-preparation.ipynb` | Data cleaning and merging notebook |
| `final_dataset.csv` | Cleaned and merged dataset |
| `dv-project.twbx` | Tableau workbook with 4 visualizations and a dashboard |
| `dv_project-streamlit.py` | Streamlit dashboard with interactive filters |

## Data Sources

- [Urban Population — World Bank](https://data.worldbank.org/indicator/SP.URB.TOTL)
- [PM2.5 Air Pollution — World Bank](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)

## Running the Streamlit App

```bash
pip install streamlit pandas plotly numpy
streamlit run dv_project-streamlit.py