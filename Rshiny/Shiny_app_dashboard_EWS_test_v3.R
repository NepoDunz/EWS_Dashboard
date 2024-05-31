# Load necessary libraries
library(shiny)
library(shinydashboard)
library(shinydashboardPlus)
library(ggplot2)
library(ggiraph)
library(rnaturalearth)
library(rnaturalearthdata)
library(sf)
library(dplyr)
library(plotly)
library(tidyr)

# Load the data outside the server function
df <- read.csv("C:/Users/wb574010/OneDrive - WBG/Nepo's Work/MFR/EWS/EWS development consultants/Dashboard/Shinyapp/Outputs.csv")



calculate_population_difference <- function(input_df) {
  selected_year_data <- input_df[input_df$Year == 2024, ]
  previous_year_data <- input_df[input_df$Year == 2023, ]
  
  merged_data <- merge(selected_year_data, previous_year_data, by = "Country", suffixes = c("_2024", "_2023"))
  merged_data$risk_difference <- merged_data$EWS_TOTAL_2024 - merged_data$EWS_TOTAL_2023
  
  return(merged_data)
}

# Adjusted make_donut function to remove title and set dark background
make_donut <- function(input_response, input_text) {
  df_selected_year <- data.frame(
    Topic = c('', input_text),
    value = c(100 - input_response, input_response)
  )
  
  chart_color <- if (input_text == 'Risk increase') c('grey', 'red') else c('grey', 'green')
  
  plot <- plot_ly(df_selected_year, labels = ~Topic, values = ~value, type = 'pie', hole = 0.6, marker = list(colors = chart_color)) %>%
    layout(
      showlegend = FALSE,
      paper_bgcolor = '#1a2226',  # Set dark background for the chart
      plot_bgcolor = '#1a2226',   # Set dark background for the plot area
      annotations = list(
        text = '',  # Remove title text
        showarrow = FALSE,
        font = list(color = 'white')
      )
    )
  
  return(plot)
}

# UI
ui <- dashboardPage(
  dashboardHeader(
    title = tags$div(
      tags$img(src = "WBLOGO.jpg", height = "30px", style = "margin-right: 10px;"),
      tags$h1("Early Warning System Dashboard", style = "display: inline; margin: 0; vertical-align: middle; color: white;")
    ),
    tags$li(class = "dropdown",
            tags$style(HTML("
              .main-header .logo {
                background-color: #000000 !important;
                color: white !important;
                font-family: Arial, Helvetica, sans-serif;
              }
              .main-header .navbar {
                background-color: #000000 !important;
                color: white !important;
              }
              .main-header .navbar-custom-menu .navbar-nav > li > a {
                color: white !important;
              }
              .main-header .navbar-custom-menu .navbar-nav > li > a:hover {
                background-color: #000000 !important;
              }
              .main-header .logo span {
                display: inline-block;
                vertical-align: middle;
                line-height: 30px; /* Adjust this value to match the height of your logo */
              }
              .main-header .navbar-custom-menu .navbar-nav > li > a {
                color: white !important;
              }
            ")))
  ),

  dashboardSidebar(
    sidebarMenu(
      menuItem("Overview", tabName = "overview_plot", icon = icon("dashboard"))
    )
  ),
  dashboardBody(
    tags$style(HTML("
      .content-wrapper, .right-side {
        background-color: #1a2226; /* Dark content background */
      }
      .box.box-solid.box-primary>.box-header {
        color: #fff;
        background: #1e282c; /* Dark box header background */
      }
      .box.box-solid.box-primary {
        border-color: #1e282c; /* Dark box border color */
      }
      .box.box-solid.box-primary>.box-body {
        color: #fff;
        background-color: #1a2226; /* Dark box body background */
      }
    ")),
    tabItems(
      tabItem(tabName = "overview_plot",
              fluidRow(
                box(
                  title = "Top 5 Countries by Total Risk Score",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 10,
                  plotOutput("bar_plot", width = "100%", height = "600px")
                ),
                box(
                  title = "Risk Change",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 2,
                  height = "400px",
                  fluidRow(
                    box(
                      title = "Risk Increase",
                      status = "primary",
                      solidHeader = TRUE,
                      width = 12,
                      plotlyOutput("donut_increase", height = "200px")
                    ),
                    box(
                      title = "Risk Decrease",
                      status = "primary",
                      solidHeader = TRUE,
                      width = 12,
                      plotlyOutput("donut_decrease", height = "200px")
                    )
                  )
                )
              ),
              fluidRow(
                box(
                  title = "Interactive Global Map",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 6,
                  girafeOutput("global_map", width = "100%", height = "800px")
                ),
                box(
                  title = "Heatmap",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 6,
                  plotlyOutput("heatmap", width = "100%", height = "500px")
                )
              )
      )
    )
  )
)




# Server
server <- function(input, output, session) {
  df <- read.csv("C:/Users/wb574010/OneDrive - WBG/Nepo's Work/MFR/EWS/EWS development consultants/Dashboard/Shinyapp/Outputs.csv")
  # Check the loaded data
  print(head(df)) # Print the first few rows to check the structure
  
  # Check if data filtering and merging is working
  observe({
    print(unique(df$Year)) # Print unique years to check if the data contains the expected years
  })
  
  output$global_map <- renderGirafe({
    # Get high-resolution world map data
    world <- ne_countries(scale = "medium", returnclass = "sf")
    
    # Drop Antarctica
    world <- world %>% filter(name != "Antarctica")
    
    # Filter data for the year 2024
    data_2024 <- df %>% filter(Year == 2024)
    
    # Merge the data with world spatial data
    world <- world %>%
      left_join(data_2024, by = c("iso_a3" = "Country"))
    
    # Create a ggplot
    p <- ggplot(data = world) +
      geom_sf_interactive(aes(fill = EWS_TOTAL, tooltip = paste("Country:", name, "<br> Risk Score:", EWS_TOTAL)), color = "black") +
      scale_fill_gradient(low = "white", high = "darkred", na.value = "grey", name = "Total Risk Score") +
      theme_minimal() +
      theme(
        axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        panel.grid = element_blank(),
        plot.margin = margin(0, 0, 0, 0, "cm"),  # Remove margins
        plot.background = element_rect(fill = "#1a2226"),
        panel.background = element_blank(),
        legend.position = "right",
        legend.text = element_text(color = "white")
      )
    
    # Make the ggplot interactive using ggiraph
    girafe(ggobj = p, options = list(opts_hover(css = "fill:orange;")), width_svg = 15, height_svg = 7)
  })
  
 
  output$bar_plot <- renderPlot({
    # Filter data for the year 2024
    data_2024 <- df %>% filter(Year == 2024)
    
    # Identify the top 5 countries by EWS_TOTAL score
    top_5_countries <- data_2024 %>% arrange(desc(EWS_TOTAL)) %>% head(5)
    
    # Filter the data to only include the top 5 countries
    top_5_data <- data_2024 %>% filter(Country %in% top_5_countries$Country)
    
    # Pivot the data to long format for faceting
    top_5_data_long <- top_5_data %>%
      select(Country, EWS_TOTAL, EWS_FISCAL, EWS_EXTERNAL, EWS_FINAL) %>%
      pivot_longer(cols = c(EWS_TOTAL, EWS_FISCAL, EWS_EXTERNAL, EWS_FINAL), 
                   names_to = "Risk_Type", values_to = "Score") %>%
      mutate(Risk_Type = factor(Risk_Type, levels = c("EWS_TOTAL", "EWS_FISCAL", "EWS_EXTERNAL", "EWS_FINAL")))
    
    # Custom labels for the facets
    risk_labels <- c(EWS_TOTAL = "Total Risk", EWS_FISCAL = "Fiscal Risk", EWS_EXTERNAL = "External Risk", EWS_FINAL = "Financial Risk")
    
    # Create a bar plot with facets for each risk score
    ggplot(top_5_data_long, aes(x = reorder(Country, Score), y = Score, fill = Score)) +
      geom_bar(stat = "identity") +
      geom_text(aes(label = Score), vjust = 0.5, hjust = 1.0, color = "black", size = 5, fontface = "bold") +
      coord_flip() +
      scale_fill_gradient(low = "yellow", high = "darkred", na.value = "white") +
      facet_wrap(~ Risk_Type, scales = "free", ncol = 2, labeller = labeller(Risk_Type = risk_labels)) +  # Use custom labels
      theme_minimal() +
      theme(
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text = element_text(color = "white"),
        axis.ticks = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.margin = margin(10, 10, 10, 10, "pt"),
        plot.background = element_rect(fill = "#1a2226", color = NA),
        panel.background = element_rect(fill = "#1a2226", color = NA),
        legend.position = "none",
        strip.background = element_rect(fill = "grey20"),  # Background for facet headers
        strip.text = element_text(color = "white", face = "bold")  # Text for facet headers
      )
  })
  
  
  
  
  
  output$donut_increase <- renderPlotly({
    selected_year_data <- calculate_population_difference(df)
    
    country_risk_increase <- sum(selected_year_data$risk_difference > 0) / n_distinct(selected_year_data$Country) * 100
    
    donut_chart_increase <- make_donut(country_risk_increase, 'Risk increase')
    
    donut_chart_increase
  })
  
  output$donut_decrease <- renderPlotly({
    selected_year_data <- calculate_population_difference(df)
    
    country_risk_decrease <- sum(selected_year_data$risk_difference < 0) / n_distinct(selected_year_data$Country) * 100
    
    donut_chart_decrease <- make_donut(country_risk_decrease, 'Risk decrease')
    
    donut_chart_decrease
  })
  
  output$heatmap <- renderPlotly({
    # Define the function to create the heatmap
    make_heatmap <- function(input_df, input_y, input_x, input_color, input_color_theme) {
      heatmap <- ggplot(input_df, aes_string(x = input_x, y = input_y, fill = input_color)) +
        geom_tile(color = "white") +
        scale_fill_distiller(palette = input_color_theme, direction = 1) +  # Use direction = 1 for better color representation
        labs(x = "", y = "Year") +
        theme_minimal() +
        theme(
          plot.background = element_rect(fill = "#1a2226"),  # Black background
          panel.grid.major = element_blank(),  # Remove major grid lines
          panel.grid.minor = element_blank(),  # Remove minor grid lines
          axis.title = element_text(size = 18, face = "bold", margin = margin(15, 0, 0, 0, "pt"), color= 'white'),
          axis.text.x = element_text(angle = 90, size = 18, hjust = 1,color ='white'),
          axis.text.y = element_text(size = 18, color ='white'),
          legend.position = "none"
        )
      return(heatmap)
    }
    
    # Call the function to create the heatmap
    heatmap <- make_heatmap(input_df = df, input_y = "Year", input_x = "Country", input_color = "EWS_TOTAL", input_color_theme = "Reds")
    
    # Render the heatmap as a plotly object
    ggplotly(heatmap)
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)
