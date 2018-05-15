library(install.load)
install_load('tidyverse')
install_load('plotly')
install_load('RColorBrewer')
install_load('webshot')

df <- read.csv('emails_with_info.csv')

df$province <- NULL  # province has no non-NAs, so remove it

# Grab number of entries within each country
country.counts <- df %>% 
                    group_by(country_code) %>% 
                    summarise(count = n_distinct(document_id))

# Map every ISO Alpha-2 country code to an ISO Alpha-3 country code
# (plotly requires Alpha-3)
# (from https://github.com/gsnaveen/plotly-worldmap-mapping-2letter-CountryCode-to-3letter-country-code)
country.mapping = read.csv('countryMap.txt', sep='\t')
country.mapping <- country.mapping %>% 
                    rename(country = Countrylet, country_code = X2let, country_code_A3 = X3let)

country.counts <- inner_join(country.counts, country.mapping, by = "country_code")

### Produce choropleth map with Plotly

# light grey boundaries
l <- list(color = toRGB("grey"), width = 0.5)

# specify map projection/options
g <- list(
  showframe = FALSE,
  showcoastlines = FALSE,
  projection = list(type = 'Mercator')
)

p <- country.counts %>% plot_geo() %>%
  add_trace(
    z = ~count, color = ~count, colors = brewer.pal(5, "YlGnBu"),
    text = ~country, locations = ~country_code_A3, 
    marker = list(line = l)
  ) %>%
  colorbar(title = 'Number<br>of<br>Authors') %>%
  layout(
    title = 'arXiv Authors World-Wide',
    geo = g
  )

# Save plotly figure
htmlwidgets::saveWidget(p, file = "map.html")
