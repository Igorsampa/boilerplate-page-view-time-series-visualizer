import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv',  parse_dates=['date'], index_col='date')

df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot(df=df):
    # Criação do gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    fig.savefig('line_plot.png')
    return fig
draw_line_plot()

def draw_bar_plot(df=df):
    df_bar = df.copy()
    # Transformação da data em index
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    # Agrupamento
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Passa os números dos meses para nomes dos meses
    month_dict = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Criação do gráfico de barras
    fig = df_grouped.plot(kind='bar', figsize=(10, 8))
    fig.set_xlabel("Years")
    fig.set_ylabel("Average Page Views")
    fig.legend([month_dict[i] for i in df_grouped.columns], title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('bar_plot.png')
    return fig
draw_bar_plot()

def draw_box_plot(df=df):
    # Prepara os dados para o box plot
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')  # Ordenar meses corretamente
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Box plot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Box plot por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig
