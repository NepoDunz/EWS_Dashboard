library(shiny)
library(shinydashboard)
library(DT)
library(ggplot2)
library(dplyr)

# Load the data outside the server function
df <- read.csv("Outputs.csv")

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
      menuItem("Country-wise Plot", tabName = "country_plot", icon = icon("chart-line")),
      menuItem("Summary Plot", tabName = "summary_plot", icon = icon("chart-bar"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = "country_plot",
              fluidRow(
                box(title = "Select Options", width = 4,
                    selectInput("Country", "Select Country", choices = unique(df$Country)),
                    selectInput("variable_country", "Select Variable", choices = names(df)[!names(df) %in% c("Country", "Year")])
                ),
                box(title = "Summary Table", width = 12,
                    DTOutput("contents_country")
                ),
                box(title = "Country Specific Risk", width = 12,
                    plotOutput("barplot_country")
                )
              )
      ),
      tabItem(tabName = "summary_plot",
              fluidRow(
                box(title = "Select Variable", width = 4,
                    selectInput("variable_summary", "Select Variable", choices = names(df)[!names(df) %in% c("Country", "Year")])
                ),
                box(title = "Summary Table", width = 12,
                    DTOutput("contents_summary")
                ),
                box(title = "Summary of Country Risk", width = 12,
                    plotOutput("barplot_summary")
                )
              )
      )
    )
  )
)

# Server
server <- function(input, output, session) {
  # Output the data table for country-wise plot
  output$contents_country <- renderDT({
    datatable(df)
  })
  
  # Generate the bar plot for selected country and variable
  output$barplot_country <- renderPlot({
    req(input$Country, input$variable_country)
    
    selected_data <- df %>% filter(Country == input$Country)
    
    #ggplot(selected_data, aes_string(x = "Country", y = input$variable_country)) +
    ggplot(selected_data, aes_string(x = "Year", y = input$variable_country)) +
      #geom_bar(stat = "identity") +
      geom_line(color="Blue",size=1.5) +
      labs(title = paste("Scores of", input$variable_country, "for", input$Country),
           x = "",
           y = input$variable_country) +
      theme_minimal()
  })
  
  # Output the data table for summary plot
  output$contents_summary <- renderDT({
    datatable(df)
  })
  
  # Generate the summary bar plot for top 10 countries by selected variable
  output$barplot_summary <- renderPlot({
    req(input$variable_summary)
    
    top_countries <- df %>%
      group_by(Country) %>%
      summarize(Value = sum(.data[[input$variable_summary]], na.rm = TRUE)) %>%
      top_n(10, Value) %>%
      arrange(desc(Value))
    
    ggplot(top_countries, aes(x = reorder(Country, Value), y = Value)) +
      geom_bar(stat = "identity",fill="Blue") +
      coord_flip() +
      labs(title = paste("Top 10 Countries by", input$variable_summary),
           x = "",
           y = input$variable_summary) +
      theme_minimal()
  })
}

# Run the application 
shinyApp(ui = ui, server = server)