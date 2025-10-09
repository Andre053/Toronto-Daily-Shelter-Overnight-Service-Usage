# Daily Shelter & Overnight Service Occupancy & Capacity
# Toronto Open Dataset Exploration

## About
This project aims to provide a full-stack application to better understand the numbers and trends of occupancy and capacity counts of people and groups staying in shelters or benefitting from overnight services. The dataset is published daily by Open Data Toronto, with records going back to 2021. This program uses a Next.js frontend, a Python FastAPI backend, and CSV files for data persistence. While the city reports this data and publishes it on their website, their visualization is limited to a simple comprehensive spreadsheet. This project aims to provide various avenues for analysis, such as with charts, maps, and tables. 

## [IN PROGRESS] Features
1. Heat map of Toronto by FSA, allows selecting a statistic to colour the map, displays overall map stats, can select a specific FSA to display related stats
![Map of Toronto page coloured by average daily count of service users. Hovering over a clicked FSA with a tooltip showing the FSA name. To the right of the map are settings that show the time period and the selected statistic; below the settings are overall statistics and statistics for the selected FSA over the time period.](https://github.com/Andre053/Toronto-Daily-Shelter-Overnight-Service-Usage/blob/main/images/explore-page_2025-10-08.png?raw=true)
2. Page of charts user can customize options for, currently has a line chart to view the main features over time, allows for multiple time aggregations
![Line graph showing service user count over time from 2021 to 2025. On the chart is a tooltip above the hovered over datapoint, with the datapoint highlighted by a small circle. To the left of the graph are settings showing the selected statistic, the frequency to aggregate the data, and the time period.](https://github.com/Andre053/Toronto-Daily-Shelter-Overnight-Service-Usage/blob/main/images/charts-page_2025-10-08.png?raw=true)
3. Data story built from my work on the project
4. Explanation of the project and its background

## Links
- [Open Data dataset](https://open.toronto.ca/dataset/daily-shelter-overnight-service-occupancy-capacity/)
- [City's daily report on the data](https://www.toronto.ca/city-government/data-research-maps/research-reports/housing-and-homelessness-research-and-reports/shelter-census/)
- [Housing Stablity Service System](https://www.toronto.ca/city-government/data-research-maps/research-reports/housing-and-homelessness-research-and-reports/housing-stability-service-system-map-and-terms/)
- [Shelter System](https://www.toronto.ca/community-people/housing-shelter/homeless-help/about-torontos-shelter-system/)
- [Open Database of Addresses](https://www.statcan.gc.ca/en/lode/databases/oda)
- [Canadian Census FSA codes](https://www150.statcan.gc.ca/n1/en/catalogue/92-179-X)

## Limitations
- The map has functionality to show Toronto by neighbourhood, but the data lacks any feature to link each record to the neighbourhood
- Data is available back to 2021, but currently only data until the beginning of 2025 is utilized
- Various limitations about the data itself are presented on the City's daily report
- Currently there are a handful of FSAs that are on the map, but are not mentioned in the data. More investigation needed