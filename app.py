import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional

st.set_page_config(page_title="EEP105 Group Dashboard", page_icon="📊", layout="wide")

# Reusable data loaders
@st.cache_data(show_spinner=False)
def load_csv(url: str) -> Optional[pd.DataFrame]:
	try:
		df = pd.read_csv(url)
		return df
	except Exception as e:
		st.warning(f"Could not load CSV from {url}: {e}")
		return None

@st.cache_data(show_spinner=False)
def load_excel(url: str, sheet_name: Optional[str] = None) -> Optional[pd.DataFrame]:
	try:
		df = pd.read_excel(url, sheet_name=sheet_name)
		return df
	except Exception as e:
		st.warning(f"Could not load Excel from {url}: {e}")
		return None

BASE = "https://raw.githubusercontent.com/Veto1oox/GroupProjEEP105/main/"

st.title("EEP105 Group Dashboard")
st.caption("This dashboard summarizes key findings from our case study. Data are loaded directly from GitHub-hosted files so no local uploads are needed.")

# Tabs for sections
section_tabs = st.tabs([
	"Global CO₂ Emissions",
	"Global GDP",
	"Energy Use",
	"Pakistan Temperature",
	"Disasters (PAK/IND/IRN)",
	"About & Data Sources",
])

# 1) Global CO2 emissions
with section_tabs[0]:
	st.subheader("Global CO₂ Emissions (Fossil + Land Use)")
	df_emissions = load_csv(BASE + "co2-fossil-plus-land-use.csv")
	if df_emissions is not None and not df_emissions.empty:
		# Basic assumptions for common OWID-format datasets
		country_col = "country" if "country" in df_emissions.columns else None
		year_col = "year" if "year" in df_emissions.columns else None
		value_col_candidates = ["co2", "co2_emissions", "emissions"]
		value_col = next((c for c in value_col_candidates if c in df_emissions.columns), None)

		if country_col and year_col and value_col:
			available_countries = sorted(c for c in df_emissions[country_col].dropna().unique() if isinstance(c, str))
			default_countries = [c for c in ["World", "United States", "China", "India", "Pakistan"] if c in available_countries][:3]
			selected_countries = st.multiselect("Select countries", options=available_countries, default=default_countries)

			if selected_countries:
				filtered = df_emissions[df_emissions[country_col].isin(selected_countries)].copy()
				pivot = filtered.pivot_table(index=year_col, columns=country_col, values=value_col, aggfunc="sum").sort_index()
				st.line_chart(pivot)
				st.dataframe(filtered[[country_col, year_col, value_col]].sort_values([country_col, year_col]).tail(1000))
			else:
				st.info("Select at least one country to view the time series.")
		else:
			st.dataframe(df_emissions.head(1000))
			st.info("Displayed first rows because expected columns were not found.")
	else:
		st.stop()

# 2) Global GDP
with section_tabs[1]:
	st.subheader("Global GDP")
	df_gdp = load_csv(BASE + "glb_gdp.csv")
	if df_gdp is not None and not df_gdp.empty:
		country_col = "country" if "country" in df_gdp.columns else None
		year_col = "year" if "year" in df_gdp.columns else None
		value_col_candidates = ["gdp", "GDP", "value"]
		value_col = next((c for c in value_col_candidates if c in df_gdp.columns), None)

		if country_col and year_col and value_col:
			available_countries = sorted(c for c in df_gdp[country_col].dropna().unique() if isinstance(c, str))
			default_countries = [c for c in ["World", "United States", "China", "India", "Pakistan"] if c in available_countries][:3]
			selected_countries = st.multiselect("Select countries", options=available_countries, default=default_countries, key="gdp_countries")

			if selected_countries:
				filtered = df_gdp[df_gdp[country_col].isin(selected_countries)].copy()
				pivot = filtered.pivot_table(index=year_col, columns=country_col, values=value_col, aggfunc="sum").sort_index()
				st.line_chart(pivot)
				st.dataframe(filtered[[country_col, year_col, value_col]].sort_values([country_col, year_col]).tail(1000))
			else:
				st.info("Select at least one country to view the time series.")
		else:
			st.dataframe(df_gdp.head(1000))
			st.info("Displayed first rows because expected columns were not found.")

# 3) Energy Use
with section_tabs[2]:
	st.subheader("Energy Use")
	df_energy = load_csv(BASE + "ene_cosp.csv")
	if df_energy is not None and not df_energy.empty:
		year_col = "year" if "year" in df_energy.columns else None
		if year_col:
			# Show the sum across numeric columns by year as a simple overview
			numeric_cols = [c for c in df_energy.columns if pd.api.types.is_numeric_dtype(df_energy[c])]
			if numeric_cols:
				agg = df_energy.groupby(year_col)[numeric_cols].sum().sort_index()
				st.line_chart(agg)
			st.dataframe(df_energy.head(1000))
		else:
			st.dataframe(df_energy.head(1000))

# 4) Pakistan Temperature
with section_tabs[3]:
	st.subheader("Pakistan Min/Max Temperature")
	df_temp = load_excel(BASE + "pak_min_max_temp.xlsx")
	if df_temp is not None and not df_temp.empty:
		year_col = "year" if "year" in df_temp.columns else None
		numeric_cols = [c for c in df_temp.columns if pd.api.types.is_numeric_dtype(df_temp[c])]
		if year_col and numeric_cols:
			agg = df_temp.groupby(year_col)[numeric_cols].mean().sort_index()
			st.line_chart(agg)
		st.dataframe(df_temp.head(1000))

# 5) Disasters
with section_tabs[4]:
	st.subheader("Reported Disasters: Pakistan, India, Iran")
	df_disasters = load_excel(BASE + "pak_ind_irn_disasters.xlsx")
	if df_disasters is not None and not df_disasters.empty:
		year_col = "year" if "year" in df_disasters.columns else None
		if year_col:
			numeric_cols = [c for c in df_disasters.columns if pd.api.types.is_numeric_dtype(df_disasters[c])]
			if numeric_cols:
				agg = df_disasters.groupby(year_col)[numeric_cols].sum().sort_index()
				st.line_chart(agg)
		st.dataframe(df_disasters.head(1000))

# 6) About/Data Sources
with section_tabs[5]:
	st.subheader("About this dashboard")
	st.markdown(
		"""
		- This dashboard is built for EnvEcon 105 to communicate key findings from our case study.
		- All datasets are referenced via raw GitHub URLs, so the notebook need not ship data files.
		- Use the tabs to explore CO₂ emissions, GDP, energy use, temperature trends, and disasters.
		"""
	)
	st.markdown("**Primary data sources (GitHub raw):**")
	st.code(
		"\n".join([
			BASE + "co2_pcap_cons.csv",
			BASE + "co2-fossil-plus-land-use.csv",
			BASE + "pak_ind_irn_disasters.xlsx",
			BASE + "glb_gdp.csv",
			BASE + "ene_cosp.csv",
			BASE + "pak_min_max_temp.xlsx",
		])
	)
	st.markdown("Run locally: `pip install -r requirements.txt && streamlit run app.py`")
