⸻

README: Analysis for Zonal Influence Maps

Overview

This README details the analytical procedures applied to cleaned spatial data for assessing the impact of proximity to BRT and TER infrastructure on building development in Dakar, using Difference-in-Differences (DiD) and other statistical models.

⸻

Analysis Steps
	1.	Preparation for DiD Analysis
	•	Loaded geospatial data for 2016 and 2023.
	•	Merged baseline (2016) building attributes with changes from 2016–2023 (height_dif, height_cha, change).
	•	Appended group identifiers: treated (within 0–2 km of infrastructure) and control (5–10 km away).
	•	Computed post-treatment building heights
	•	Converted data to long format: each building has two entries (2016 and 2023).
	•	Created binary indicators:
	•	post: 1 if post-treatment (2023)
	•	treated: 1 if in treated area
	•	post_treated: interaction term for treatment effect
	•	An additional DiD analysis was conducted using a narrower treatment-control setup:
	•	Treated: 0–1 km from infrastructure
	•	Control: 1–2 km away
	•	All relevant shapefiles for this analysis are saved and zipped in the zone_buffer_exports.zip archive within the generated folder.
	2.	Statistical Modeling
	•	By Land Use Class (LandUseCla):
	•	OLS Regression:
Predicted building height and presence as a function of post, treated, and post_treated. The coefficient on post_treated is the DiD estimator.
	•	Multinomial Logistic Regression:
Modeled categorical changes in building presence (change) and building height (height_cha) for the post-treatment period.
	•	Stored and exported model results, including coefficients and p-values.
	3.	Visualization
	•	Generated bar plots of treatment effects (post_treated) and associated p-values for OLS models.

⸻

Tools Used
	•	Python
	•	geopandas
	•	pandas
	•	statsmodels
	•	scikit-learn

⸻

Output Structure
	•	All outputs saved in a structured directory.
	•	Filenames indicate buffer size and land use class (e.g., zones_residential_1km.gpkg, buildings_commercial_500m.gpkg).
	•	Zipped outputs from alternate DiD configurations (e.g., 0–1 km treated vs 1–2 km control) are included in zone_buffer_exports.zip in the generated folder.

New Output Files in output/ Folder
	•	dakar_raster_to_csv.csv: Tabular CSV format of raster-based data used for modeling, containing the following columns:

presence_2016, height_2016, presence_2023, height_2023, height_change,
presence_change, lulc_class, presence_2017, height_2017,
presence_2022, height_2022, zone_id, distance_brt, distance_ter, zone_name


	•	dakar_14band_stack_with_distance.tif: Raster file with 14 stacked bands representing all above variables (except zone_name, which is tabular only).

These outputs allow for streamlined analysis of spatial and temporal dynamics across zones, and facilitate machine learning, modeling, and mapping tasks.

⸻

Notes
	•	Analyses are stratified by land use class for granularity.
	•	DiD analysis enables causal inference on the effect of transport infrastructure proximity on urban development.
	•	Outputs support spatial visualization and integration with mapping platforms or dashboards.

⸻
