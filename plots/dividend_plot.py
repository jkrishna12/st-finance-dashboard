from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def bar_plotter(df, x_axis, y_axis, x_label, y_label):
    """
    Function used to plot bar graph. 
    
    Parameters:
        df: pandas dataframe
        x_axis: string, column name to plot on the x axis
        y_axis: string, column name to plot on the y axis
        x_label: string, label for the x axis
        y_label: string, label for the y axis
        
    Returns:
        fig: Matplotlib figure: figure of the bar chart
    """   
    
    fig, ax = plt.subplots(figsize = (8,6))    
    
    ax.set_facecolor('#0E1117')
    fig.set_facecolor('#0E1117')
    ax.spines[['right', 'top']].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    sns.barplot(data = df, x = x_axis, y = y_axis, palette = 'Set2', ax = ax)
    
    ax.set(xlabel= x_label, ylabel= y_label)
    
    ax.tick_params(axis='x', rotation=45, colors = 'w')
    
    ax.tick_params(axis='y', colors = 'w')
    
    # ax.grid(True, axis = 'y', alpha = 0.2, color = 'w')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    # for loop used to write specific value of bar 
    for bar in ax.patches:
        
        ax.annotate(f"£{bar.get_height():.2f}",
                    (bar.get_x() + bar.get_width() / 2,
                     bar.get_height()), ha='center', va='center',
                    size=8, xytext=(0, 8),
                    textcoords='offset points', color = 'white')     
    
    return fig

def line_plotter(df, x_axis, y_axis, x_label, y_label):
    """
    Function used to plot line graph 
    
    Parameters:
        df: pandas dataframe
        x_axis: string, column name to plot on the x axis
        y_axis: string, column name to plot on the y axis
        x_label: string, label for the x axis
        y_label: string, label for the y axis
        
    Returns:
        fig: Matplotlib figure: figure of the line graph
    """     

    fig, ax = plt.subplots(figsize = (5,3))
    
    sns.lineplot(data = df, x = x_axis, y = y_axis, ax = ax)
    
    ax.set_facecolor('#0E1117')
    fig.set_facecolor('#0E1117')
    ax.spines[['right', 'top']].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    ax.set(xlabel= x_label, ylabel= y_label)
    
    ax.tick_params(axis='x', rotation=45, colors = 'w')
    
    ax.tick_params(axis='y', colors = 'w')
    
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    ax.grid(True, axis = 'y', alpha = 0.2)
        
    return fig

def dividend_bar_plot(dividends_df):
    """
    Function takes the dividend data frame and returns a 2 figure objects.
    First one is a bar graph of the dividends paid out per year. 
    Second one is a bar graph ofthe dividends paid out per month for the last
    month
    
    Parameter: 
        dividends_df: Pandas Dataframe, dividend portoflio dataframe
        
    Returns:
        fig_year: Matplotlib figure, bar chart of dividends payout per year
        fig_month: Matplotlib figure, bar chart of dividends paid out per month for the last year
    """
    
    # create month and year columns 
    dividends_df['year'] = dividends_df['paidOn'].dt.year
    dividends_df['month'] = dividends_df['paidOn'].dt.month
    
    # group data by year and calculate sum of dividends per year
    year_plot = dividends_df.groupby(dividends_df['paidOn'].dt.year)['amount'].sum().reset_index()

    # define variables needed to plot bar graph
    year_x_axis = 'paidOn'
    year_y_axis = 'amount'
    year_x_label = 'Year'
    year_y_label = 'Dividend Paid Out (£)'
    
    # plot dividends sum per year
    fig_year = bar_plotter(year_plot, year_x_axis, year_y_axis,
                           year_x_label, year_y_label)
    
    # calculate date exactly 1 year ago    
    t = date.today() - relativedelta(years = 1)
    
    # filter dataset to only include records data from last year
    last_yr = dividends_df[dividends_df['paidOn'].dt.date >= t].copy()
    
    # define a new column that shows the year and month
    last_yr.loc[:,'year_month'] = last_yr['paidOn'].dt.to_period('M')
    
    # group data based on the year and month and sum dividends 
    month = last_yr.groupby(['year_month'])['amount'].sum().reset_index() 
    
    # define variables needed to plot bar graph
    month_x_axis = 'year_month'
    month_y_axis = 'amount'
    month_x_label = 'Month'
    month_y_label = 'Dividend Paid Out (£)'
    
    # plot dividends sum per month for the last year     
    fig_month = bar_plotter(month, month_x_axis, month_y_axis,
                            month_x_label, month_y_label)
    
    return fig_year, fig_month


def specific_stock_df(df, option):
    """
    Depdending on the option (list of all stocks) a line graph of dividend payout
    is returned
    
    Parameters:
        df: Pandas Dataframe, of all stock dividend payouts
        option: String, of the stock name
    
    Returns:
        stock_fig: Matplotlib figure, lineplot of the historic dividend payout 
                   for that stock
        stock_paid_out: Integer, sum of dividend pay outs for that stock
    """
    
    # filter the dataset for that stock
    stock_df = df[df['shortName'] == option]
    
    # sort the dataframe in ascending order of pay outs
    stock_sorted_df = stock_df.sort_values('paidOn', ascending = True)
    
    # define variables needed to plot line graph
    stock_x_axis = 'paidOn'
    stock_y_axis = 'amount'
    stock_x_label = 'Month'
    stock_y_label = 'Dividend Paid Out (£)'
    
    # sum of all pay outs for the specific stock
    stock_paid_out = np.round(stock_sorted_df['amount'].sum(), 2)
    
    #if else statement ensures that only stocks with more than 1 pay out have
    # line graph produced
    if len(stock_sorted_df) > 1:
    
        stock_fig = line_plotter(stock_sorted_df, stock_x_axis, stock_y_axis,
                             stock_x_label, stock_y_label)
                
        return stock_fig, stock_paid_out
    
    else:
        
        stock_fig = None
        
        return stock_fig, stock_paid_out
    
def dividend_history(df, entries):    
    
    div_df = df.copy()
    
    div_df['Date'] = div_df['paidOn'].dt.date
    
    div_select = div_df[['shortName', 'amount', 'Date']]
    
    rename_dict = {
        'shortName':'Ticker',
        'amount':'Dividend (£)'
    }
    
    div_hist = div_select.rename(columns = rename_dict)
    
    div_hist = div_hist.iloc[:entries,:]     
    
    return div_hist
    
    
        
    




