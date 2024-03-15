import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def pie_plot(df, label):
    """
    Takes in a dataframe and returns a pie chart
    
    Paramters:
        df: Pandas Dataframe
        label: String, column name to annotate the pie chart
    Return:
        fig: Matplotlib Figure, Figure of pie chart
    """
    
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    
    fig.set_facecolor('#0E1117')
    
    explode = np.full(len(df), 0.1)
    
    wedges, texts = ax.pie(df['currentPos'], 
                           wedgeprops=dict(width=0.5),
                           startangle=0,
                          colors=sns.color_palette('Set2', len(df)),
                          explode = explode)
    
    # bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="k", lw=0.72)
    
    # kw = dict(arrowprops=dict(arrowstyle="-"),
    #           bbox=bbox_props, zorder=0, va="center")
    
    kw = dict(arrowprops=dict(arrowstyle="-"),
              zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        
        # if statement ensures that holdings greater than 1% are shown
        if df.loc[i, 'pct'] > 1:
        
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            
            kw["arrowprops"].update({"connectionstyle": connectionstyle, 'color':'white'})
            ax.annotate(f"{df.loc[i, label]}, {df.loc[i, 'pct']}%", xy=(x, y), xytext=(1.4*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment,
                        color = 'white', **kw)
    
    return fig


def pie_balance_breakdown(portfolio_df, balance_df, option):
    """
    Function takes in the portfolio and balance dataframes and returns 
    a breakdown of the positions in the form of a pie chart
    
    Parameters:
        portfolio_df: Pandas Dataframe, of portfolio dataframe
        balance_df: Pandas Dataframe, of balance dataframe
        option: String, Depending on the opiton different pie chart will be returned
        
    Returns:
        instrument_fig: Matplotlib figure, pie chart depdning on the option argument
    """
    
    # selecting only relevant columns from portfolio dataframe
    portfolio_df = portfolio_df[['shortName', 'type', 'currentPos']]
    
    # select the current cash from the balance df and create a Dataframe in the 
    # same form as the portfolio dataframe 
    balance_df_concat = pd.DataFrame({'shortName':'Cash','type':'Cash', 'currentPos':balance_df['free']})
    
    # concatenate the balance_df_concat with the portfolio_df
    account_df = pd.concat([portfolio_df, balance_df_concat])
    
    account_val = account_df['currentPos'].sum()
    
    if option == 'Detailed':
        # calculate the percentage of each holding and round to 2dp
        account_df['pct'] = np.round((account_df['currentPos'] / account_val) * 100,2)
    
        # sort values and reset index
        account_df = account_df.sort_values('currentPos', ascending = False)
        account_df.reset_index(inplace = True, drop = True)
        
        holding_fig = pie_plot(account_df, 'shortName')
        
        return holding_fig
        
    elif option == 'General':
        # group the instruments by the type
        account_df_groupby = account_df.groupby('type')['currentPos'].sum().reset_index()
        
        # calculate the percentage of each instrument type and round to 2dp
        account_df_groupby['pct'] = np.round((account_df_groupby['currentPos'] / account_val) * 100,2)
        
        instrument_fig = pie_plot(account_df_groupby, 'type')
        
        return instrument_fig
        
    
def bar_plot(df, fig_option, x_axis, y_axis, x_label, y_label):
    """
    Function takes in a dataframe and axis and label paramters and returns a
    bar figure
    Parameters:
        df: Pandas Dataframe
        fig_option: String
        x_axis: String, column name of df
        y_axis: String, column name of df
        x_label: String, label of the x axis
        y_label: String, label of the y axis
    Returns:
        fig: Matplotlib figure, figure of bar chart
    """
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.set_facecolor('#0E1117')
    fig.set_facecolor('#0E1117')
    ax.spines[['right', 'top']].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    sns.set_palette('Set2', len(df))

    ax = sns.barplot(data = df, x = x_axis, y = y_axis)
    
    ax.set(xlabel = x_label, ylabel = y_label)
    
    ax.tick_params(axis='x', rotation=45, colors = 'w')
    
    ax.tick_params(axis='y', colors = 'w')
    
    # ax.grid(True, axis = 'y', alpha = 0.2, color = 'w')
    
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    for bar in ax.patches:

      # Using Matplotlib's annotate function and
      # passing the coordinates where the annotation shall be done
      # x-coordinate: bar.get_x() + bar.get_width() / 2
      # y-coordinate: bar.get_height()
      # free space to be left to make graph pleasing: (0, 8)
      # ha and va stand for the horizontal and vertical alignment
        
        if bar.get_height() < 0:
            height = 1
        else:
            height = bar.get_height()
        
        ax.annotate(format(bar.get_height(), '.2f'), 
                       (bar.get_x() + bar.get_width() / 2, 
                        height), ha='center', va='center',
                       size=8, xytext=(0, 8),
                       textcoords='offset points', color = 'white')
        
    ax.set_title(f"Portfolio {fig_option}", color = 'white')    
    
    return fig 

def portfolio_position_breakdown(portfolio_df, fig_option):
    """
    Function takes in the portfolio dataframe and returns a bar chart of the 
    value or percentage change depending on the figure option
    Paramters:
        portfolio_df: Pandas Dataframe, of portfolio dataframe
        fig_option: String, dictates what breakdown is returned
    Returns:
        fig_year: Matplotlib Figure, either percentage change bar chart or 
                 absolute value change bar chart depending on fig option
    """
   
    x_axis = 'shortName'
    x_label = 'Ticker'
    
    if fig_option == 'Percent Change':      
        
        y_axis = 'pct_change'
        y_label = 'Percentage Change'
        
        fig_year = bar_plot(portfolio_df, fig_option, x_axis, y_axis,
                            x_label, y_label)
        
        return fig_year
        
    elif fig_option == 'Absolute Value Change':
        
        y_axis = 'abs_value_change'
        y_label = 'Absolute Value Change (£)'
           
        fig_year = bar_plot(portfolio_df, fig_option, x_axis, y_axis,
                            x_label, y_label)
        
        return fig_year