# Reddit Sentiment Analyzer for Stock Trends

I built this project to experiment with applying NLP and data pipelines to market sentiment by turning unstructured Reddit discussions into actionable stock signals. It scrapes daily stock-related posts, analyzes their sentiment, computes aggregated metrics, and presents a Buy/Sell/Hold signal on a dashboard. The system is implemented using FastAPI and PostgreSQL on the backend, FinBERT via HuggingFace for financial sentiment analysis, Prefect for scheduling the ETL workflow, and a React.js frontend for visualizing trends and metrics.

## Architecture Diagram

![Architecture](architecture.png)

## Preview

![Dashboard 0](Dashboard0.png)  
![Dashboard 1](Dashboard1.png)
