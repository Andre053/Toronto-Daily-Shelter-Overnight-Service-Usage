# Daily Shelter & Overnight Service Occupancy & Capacity
# Toronto Open Dataset Exploration

## About
This project aims to provide a full-stack application to better understand the numbers and trends of occupancy and capacity counts of people and groups staying in shelters or benefitting from overnight services. The dataset is published daily by Open Data Toronto, with records going back to 2021. This program uses a Next.js frontend, a Python FastAPI backend, and CSV files for data persistence. While the city reports this data and publishes it on their website, their visualization is limited to a simple comprehensive spreadsheet. This project aims to provide various avenues for analysis, such as with charts, maps, and tables. 

## [IN PROGRESS] Features
1. Heat map of Toronto by FSA, allows selecting a statistic to colour the map, displays overall map stats, can select a specific FSA to display related stats
![Spatial Occupancy Statistics page. Under the navigation bar and title are three boxes in a row showing map settings, overall statistics, and FSA statistics respectively. Below is the heat map of Toronto, where each FSA is coloured by intensity according to their average daily service user count, FSAs without statistics are gray. Hovering over the map is a tooltip showing the name of the FSA below.](https://github.com/Andre053/Toronto-Daily-Shelter-Overnight-Service-Usage/blob/main/images/map-page.jpg?raw=true)
2. Page of charts user can customize options for, currently has a line chart to view the main features over time, allows for multiple time aggregations
![Occupancy Statistics Over Time page. Under the navigation bar and title are three boxes in a row showing the graph statistic selected (service users), data frequency (by day), and the date range (2021-01-01 to 2025-10-08). Below is the line graph ofthe data, showing a gradual rise from January 2021 to January 2025, then a steeper decline since then. Hovering over the graph is a circle over the datapoint in line with the mouse, with a tooltip showing the datapoint date and value.](https://github.com/Andre053/Toronto-Daily-Shelter-Overnight-Service-Usage/blob/main/images/chart-page.jpg?raw=true)
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