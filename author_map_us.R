library(install.load)
install_load('tidyverse')
install_load('plotly')
install_load('RColorBrewer')
install_load('webshot')

df <- read.csv('emails_with_info.csv')

df$province <- NULL  # province has no non-NAs, so remove it

df.us <- df %>% filter(country_code == "US")

df.us$institution <- as.character(df.us$institution)

# State two-letter codes in the order output by
# unique(df.us$institution)
# Did this by hand :O
states <- c(
  "MA", "CA", "IL", "CA", "CA", "NY", "MA", "CA", "GA", "MD",
  "NC", "CT", "IL", "OH", "OH", "MD", "TX", "OH", "TX", "PA",
  "PA", "CA", "IN", "NH", "CA", "TX", "NY", "IA", "VA", "MA",
  "IN", "NY", "MA", "CA", "IL", "WA", "PA", "TX", "IN", "NJ",
  "NY", "TX", "NC", "MI", "MI", "CA", "CA", "WI", "FL", "CA",
  "WA", "KS", "IL", "MA", "TN", "NC", "MI", "NC", "CA", "WA",
  "NY", "MO", "LA", "CA", "RI", "IN", "OK", "CO", "PA", "NJ",
  "NY", "FL", "MN", "NY", "IN", "PA", "SC", "TX", "CA", "CA",
  "MI", "CA", "CA", "TX", "HI", "AZ", "SC", "OH", "AZ", "DE",
  "NY", "VA", "SC", "NY", "AZ", "OH", "FL", "NY", "VA", "PA",
  
  "NY", "IA", "PA", "TX", "MS", "MN", "NJ", "GA", "MD", "NM",
  "VA", "NJ", "MI", "OH", "KY", "TX", "MD", "NV", "SD", "MA",
  "NY", "FL", "TX", "MN", "NC", "AL", "TN", "OK", "MO", "UT",
  "PA", "MD", "TN", "IA", "NH", "LA", "UT", "MO", "IL", "NY",
  "NY", "CO", "CT", "GA", "OR", "CA", "IL", "MT", "WA", "MI",
  "IL", "OR", "UT", "PA", "MA", "NY", "NJ", "CA", "NV", "OH",
  "CT", "MN", "TN", "NC", "IN", "TX", "ID", "MD", "PR", "AR",
  "SD", "MO", "NY", "IL", "VA", "FL", "FL", "NE", "IA", "NY",
  "LA", "FL", "WY", "UT", "PA", "LA", "TX", "GA", "TX", "FL",
  "ME", "CA", "NJ", "KS", "FL", "ND", "CO", "MA", "AL", "VA",
  
  "NM", "CA", "MI", "AL", "GA", "KY", "PA", "WI", "NJ", "PA",
  "NY", "AL", "AR", "TX", "MD", "VT", "WI", "OH", "NC", "MA",
  "IN", "TX", "TX", "OH", "CA", "TX", "WI", "OH", "KY", "CA",
  "OH", "VA", "MA", "GA", "IN", "MA", "MA", "VA", "CA", "AL",
  "OH", "NY", "ME", "PA", "PA", "OR", "OR", "MS", "NY", "RI",
  "CO", "CA", "NY", "CT", "UT", "NY", "IL", "CT", "UT", "OR",
  "NY", "ME", "SC", "CT", "CA", "MA", "NY", "CA", "MI", "IL",
  "KY", "OH", "MO", "OH")

institution_map <- data.frame(institution = unique(df.us$institution),
                              state = states,
                              stringsAsFactors = FALSE)

df.us <- left_join(df.us, institution_map, by = "institution")

# Grab number of entries within each state
state.counts <- df.us %>% 
  group_by(state) %>% 
  summarise(count = n())

# Give each state code a longer name for text hover
# (only includes the states for the codes seen)
state_names <- c(
  "Alabama", "Arkansas", "Arizona", "California", "Colorado",
  "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
  "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky",
  "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
  "Minnesota",
  "Missouri", "Mississippi", "Montana", "North Carolina",
  "North Dakota", "Nebraska", "New Hampshire", "New Jersey", 
  "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma",
  "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island",
  "South Carolina", "South Dakota", "Tennessee",
  "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin",
  "Wyoming"
)

state.counts$state_name <- state_names

### Produce choropleth map with Plotly

# light grey boundaries
l <- list(color = toRGB("white"), width = 2)

# specify map projection/options
g <- list(
  scope = 'usa',
  showlakes = TRUE,
  lakecolor = toRGB('white'),
  projection = list(type = 'albers usa')
)

p <- state.counts %>% plot_geo(locationmode = 'USA-states') %>%
  add_trace(
    z = ~count, color = ~count, colors = brewer.pal(5, "PuBuGn"),
    text = ~state_name, locations = ~state, 
    marker = list(line = l)
  ) %>%
  colorbar(title = 'Number<br>of<br>Authors') %>%
  layout(
    title = 'arXiv Authors in the U.S.',
    geo = g
  )

# Save plotly figure
export(p, file = "map_us.png")
#htmlwidgets::saveWidget(p, file = "map_us.html")