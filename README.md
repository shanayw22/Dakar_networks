# README: Data Cleaning for Zonal Influence Maps

## Overview

This README outlines the data cleaning and preprocessing steps for the **Zonal Influence Maps** project, which investigates the impact of proximity to BRT and TER infrastructure on building development in Dakar. It documents all key inputs, workflows, decision points, and experiments, ensuring full transparency and ease of replication.

---

## Data Sources

### Remote Sensing & Buildings
- [Google Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2) – Multispectral satellite imagery.
- [Google Open Buildings Temporal v1](https://developers.google.com/maps/documentation/open-buildings/overview) – Building footprints and height data from 2016 and 2023.

### World Bank
- [Dakar Land Use / Land Cover – Core City Area and Larger Urban Area](https://datacatalog.worldbank.org/search/dataset/0038978/Dakar--Senegal----Land-Use---Land-Cover--Core-City-Area-and-Larger-Urban-Area-)
  - `eo4sd_dakar_lulcvhr_2018` (Very High Resolution – Core City)
  - `eo4sd_dakar_lulchr_2018` (High Resolution – Wider Region)
- `BRT_full_line.gpkg`
- `stations_of_BRT1.gpkg`
- `ter_full_line.zip`
- `Dakar_zones/` – Communes and administrative boundaries.

---

## Cleaning Steps

### 1. Data Extraction
- Processed Sentinel-2 image mosaics for **2016** and **2023** via **Google Earth Engine**.
- Extracted bands:
  - `building_presence` (float 0 to 1)
  - `building_height` (float in meters)
- Exported as multi-band GeoTIFFs at **3.9159-meter resolution**, clipped to Areas of Interest (AOIs) - [-17.8, 14.5, -17.1, 15.1].
- Chunked into `4096 × 4096` pixel blocks for processing.

### 2. Height and Presence Change Calculation
- Loaded `.tif` rasters using `rasterio`.
- Pixel size: **3.9159 meters × 3.9159 meters**
- Computed heightand presence difference:

```
height_diff = height_2023 - height_2016
pres_diff =presence_2023 - presence_2016
```
- Computed distance to BRT
- Computed distance to TER
- Joined zone name
- Added presence and height data for 2017 and 2022



### 3. Land Use Classification
- **Core Region:** Used the `N_L4` column from `eo4sd_dakar_lulcvhr_2018`.
  - *Residential*: High to very-low density zones
  - *Commercial/Other*: Commercial, industrial, airport, port, construction, sport, extraction, dumps
- **Wider Dakar Region:** Used general categories from `eo4sd_dakar_lulchr_2018`.
  - *Unclassified Artificial Surfaces*: “Artificial Surfaces” in `N_L4`
  - *Other*: Agriculture, forest, wetlands, bare land, water, unknown

### 4. Buffer Creation and Spatial Join
- Reprojected all spatial data to **UTM Zone 28N (EPSG:32628)**.
- Merged BRT and TER lines into a single GeoDataFrame.
- Created buffer zones at:
  - **500m**, **1km**, **2km**, **5km**, **10km**
- Performed spatial join to assign:
  - Proximity zone
  - Land use class
- Retained only relevant classes:
  - Residential
  - Commercial
  - Unclassified Artificial Surfaces

### 5. Output Structure
- Per-building shapefiles exported with:
  - Geometry
  - Height change label
  - Presence change label
  - Land use class
  - Buffer zone
- Output files saved to `/outputs/`
- File naming convention:  
  ```
  buildings_<landuse>_<buffer>.gpkg
  ```

---

## Tools Used

- Google Earth Engine
- `rasterio`, `geopandas`, `pandas`, `numpy`
- QGIS (for manual validation)
- `tqdm` for progress tracking

---

## Notes

- All rasters aligned to a **4-meter** resolution grid.
- Distance calculations use projected CRS: **EPSG:32628**.
- Class thresholds (e.g., >1m for height increase) are domain-informed.

---

## Approaches Attempted But Discarded

### 1. OSM-Based Land Use Classification
- Attempted to use `landuse=*` tags from OpenStreetMap.
- **Problems**:
  - Incomplete coverage outside the urban core.
  - Inconsistent tagging.
  - Poor spatial match with building footprints.


### 3. PostGIS-Based Chunking
- Considered database-driven chunk management.
- **Problems**:
  - Too complex for current scope.
  - Simpler to manage with `rasterio` blocks.

### 4. Full Temporal Differencing in Earth Engine
- Tried differencing buildings in GEE itself.
- **Problems**:
  - Limited join capabilities.
  - Harder to manage class masking and proximity buffers.

---

## Contact

For replication questions, reach out to the research team or file an issue on this repository.
