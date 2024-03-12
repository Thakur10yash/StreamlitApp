
import streamlit as st
#from EDA_Inbound_Streamlit_utility import plt_2
import plotly.express as px
#import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import numpy as np

#df_in=pd.read_excel('/Users/yashthakur/Desktop/Streamlit/Cargosoft-Data_2022-2024.xlsx')
inbound_data= pd.read_csv('inbound_all.csv')
#Master_data=pd.read_csv('EXPORT 05.01.2024.XLSX - Sheet1.csv')
cargosoft_data=pd.read_csv('Cargosoft_and_cost.csv')
cargosoft_data['Cost per Package']=round(cargosoft_data['Costs']/cargosoft_data['Packages'],2)
#inbound_data=inbound_data[(inbound_data['year']==2023)]


####################### ABC/XYZ analysis data loading ###############
import zipfile

# Define the path to the ZIP file and the name of the CSV file inside the archive
# zip_filename = 'outbound_final_compresed.zip'
# csv_filename = 'data.csv'

# Open the ZIP file

# outbound = pd.read_csv('outbound_final_compresed.csv')

# outbound['PKT real']=outbound['PKT real'].round().astype(int)
# outbound['Material']=outbound['Material'].astype(str)
def create_percentile_bins(df, column_name,n, bin_labels=None):

    # Ensure the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    # Generate default bin labels if not provided
    if bin_labels is None:
        bin_labels = [f'{i+1}0th percentile' for i in range(n)]
    
    # Calculate percentiles
    percentiles = [i/10 for i in range(1, n)]
    percentile_values = df[column_name].quantile(percentiles)
    # Define bins

    #cc = np.concatenate(percentile_values['sum'].values)

    bins = [df[column_name].min() - 1] + percentile_values.tolist() + [df[column_name].max()]
    
    # Use pd.cut to categorize the values into bins
    df['percentile_bin'] = pd.cut(df[column_name], bins=bins, labels=bin_labels, include_lowest=True)
    
    return df
#print(outbound['StandardDeviation'].min(),outbound['StandardDeviation'].max())
#def plot_abc_xyz(outbound,n):
    
    return
#inbound_data.head(1)
def plot_abc_xyz(percent_inbound):
    field1='percentile_bin'
    field2='Standard Deviation'
    heatmap_data = percent_inbound.iloc[:, 1:]
    # Create the heatmap figure using only the cell values
    #col_to_use=['DREIEICH','KREFELD','LANGENHAGEN','MEERANE','SCHWIEBERDINGEN']
    col_to_use=list(percent_inbound.columns)[1:]

    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=percent_inbound[field1],
            text=percent_inbound[col_to_use].astype(str),
            texttemplate="%{text}%",
            xgap=5,
            ygap=5,
            colorscale=[[0, 'grey'], [1, 'red']],
            colorbar=dict(
    #             tickvals=[0, 0.5, 1],
    #             ticktext=['0%', '50%', '100%'],
    #             tickmode='array',
                x=1.07,
                len=1,
                outlinewidth=0,
                thickness=20
            )
        ))

    # Annotate the heatmap with row and column totals (excluding the last row and last column)
    for i, row_total in enumerate(percent_inbound.iloc[:, 1:].sum(axis=1)):
        fig.add_annotation(text=f'{row_total:.2f}%', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
    for j, col_total in enumerate(percent_inbound.iloc[:, 1:].sum()):
        fig.add_annotation(text=f'{col_total:.2f}%', xref='x', yref='paper', x=j, y=1.1, showarrow=False)

    # Customize the layout
    fig.update_layout(
        title='Profile between ' +field1+' and ' +  field2,
        template='plotly_white',
        xaxis=dict(ticks='', nticks=len(percent_inbound.columns)),
        yaxis=dict(ticks='', nticks=len(percent_inbound[field1])),  # Adjust the number of y-axis ticks to exclude the last row
        xaxis_title=field2,
        yaxis_title=field1,
        width=790


    #     margin=dict(l=25, r=25, b=25, t=25)
    )

    # fig.update_traces(coloraxis_colorbar=dict(thickness=20, len=0.75))
    st.plotly_chart(fig)
    # Show the plot
    #st.plotly_chart(fig)
    
#df_in=standerdize_cols(df=df_in,selected_cols=['Place of delivery','Place of loading'])
#df_in['year']=df_in['Creation Date'].dt.year
#df_in['month']=df_in['Creation Date'].dt.month
#df_in=df_in[df_in['year']>=2022]
#print(df_in)

import matplotlib.pyplot as plt

def plot_histo_2(df, place_of_loading, place_of_delivery, cost_or_pallets='Packages',Year='2023'):
    data1=df[df['year']==Year]
    data1 = df[(df['Place of Loading'] == place_of_loading) & (df['Place of Delivery'] == place_of_delivery)]

    # Create a histogram using Plotly Express
    fig = px.histogram(data1, x=cost_or_pallets, nbins=10,
                       title='Histogram of ' + cost_or_pallets + ' for Different Orders',
                       labels={cost_or_pallets: cost_or_pallets, 'value': 'Frequency'})

    # Show the histogram in Streamlit
    st.plotly_chart(fig)

def plot_histo(df, place_of_loading, place_of_delivery, cost_or_pallets='Packages',Year='2023'):
    data2=df[df['year']==Year]
    data2 = df[(df['Place of Loading'] == place_of_loading) & (df['Place of Delivery'] == place_of_delivery)]
    data2['month'] = data2['Creation Date'].dt.month

    # Create a bar plot using Plotly Express
    fig = px.bar(data2.groupby('month')[cost_or_pallets].sum().reset_index(), x='month', y=cost_or_pallets,
                 title='Distribution of ' + cost_or_pallets + ' per Month',
                 labels={'month': 'Month', cost_or_pallets: cost_or_pallets})

    # Add labels to the bars
    fig.update_traces(text=data2.groupby('month')[cost_or_pallets].sum().values, textposition='inside')

    # Show the plot in Streamlit
    st.plotly_chart(fig)

def heatmap_sum(percent_inbound,field1,field2,metric):
    heatmap_data = percent_inbound.iloc[:, 1:]
    col_to_use = list(percent_inbound.columns)[1:]

    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=percent_inbound[field1+str('_')],
            text=round((heatmap_data / 1000),2).astype(str) + 'K',  # Convert values to millions and then to string with 'M' suffix
            texttemplate="%{text}",
            xgap=5,
            ygap=5,
            colorscale=[[0, 'grey'], [1, 'red']],
            colorbar=dict(
                x=1.07,
                len=1,
                outlinewidth=0,
                thickness=20
            )
        ))

    # Annotate the heatmap with row and column totals (excluding the last row and last column)
    for i, row_total in enumerate(percent_inbound.iloc[:, 1:].sum(axis=1)):
        fig.add_annotation(text=f'{row_total/1000:.0f}K', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
    for j, col_total in enumerate(percent_inbound.iloc[:, 1:].sum()):
        fig.add_annotation(text=f'{col_total/1000:.2f}K', xref='x', yref='paper', x=j, y=1.1, showarrow=False)

    # Customize the layout
    fig.update_layout(
        title='Profile of' +metric+ ' between '+field1+' and ' +field2,
        template='plotly_white',
        xaxis=dict(ticks='', nticks=len(percent_inbound.columns), tickformat='.2s'),
        yaxis=dict(ticks='', nticks=len(percent_inbound[field1+str('_')])),  # Adjust the number of y-axis ticks to exclude the last row
        xaxis_title=field2,
        yaxis_title=field1,
    )

    # Show the plot
    st.plotly_chart(fig)  
def heatmap_mean(percent_inbound,field1,field2,metric):
    heatmap_data = percent_inbound.iloc[:, 1:]
    col_to_use = list(percent_inbound.columns)[1:]

    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=percent_inbound[field1+str('_')],
            text=round((heatmap_data),2).astype(str),  # Convert values to millions and then to string with 'M' suffix
            texttemplate="%{text}",
            xgap=5,
            ygap=5,
            colorscale=[[0, 'grey'], [1, 'red']],
            colorbar=dict(
                x=1.07,
                len=1,
                outlinewidth=0,
                thickness=20
            )
        ))

    # Annotate the heatmap with row and column totals (excluding the last row and last column)
    for i, row_total in enumerate(percent_inbound.iloc[:, 1:].mean(axis=1)):
        fig.add_annotation(text=f'{row_total:.0f}', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
    for j, col_total in enumerate(percent_inbound.iloc[:, 1:].mean()):
        fig.add_annotation(text=f'{col_total:.2f}', xref='x', yref='paper', x=j, y=1.1, showarrow=False)

    # Customize the layout
    fig.update_layout(
        title='Profile of' +metric+ ' between '+field1+' and ' +field2,
        template='plotly_white',
        xaxis=dict(ticks='', nticks=len(percent_inbound.columns), tickformat='.2s'),
        yaxis=dict(ticks='', nticks=len(percent_inbound[field1+str('_')])),  # Adjust the number of y-axis ticks to exclude the last row
        xaxis_title=field2,
        yaxis_title=field1,
    )

    # Show the plot
    st.plotly_chart(fig)
def plot_heatmap_cost(df,f1,f2,value1,value2,metric):
## Top Loading Locations 
    field1=f1
    top=5
    metric=metric
    top_field1=value1
    # top delivery locations
    field2=f2
    top=5
    metric=metric
    top_field2=value2
    
    # factory and warehouse loading mapping
    by_factory_group = df.groupby([field1,field2], as_index=False)\
        .agg({metric:['sum','mean']})
    by_factory_group.columns = by_factory_group.columns.map('_'.join)
    by_factory_group['percentage_sales']=round(by_factory_group[metric+'_sum']/sum(by_factory_group[metric+'_sum']),3)
    by_factory_group['Rank'] = by_factory_group['percentage_sales'].rank(ascending=False)
    by_factory_group=by_factory_group.sort_values(by=['percentage_sales'],ascending=False)
    # keeping only top values
    by_factory_group=by_factory_group[by_factory_group[field2+str('_')].isin(top_field2)]
    by_factory_group=by_factory_group[by_factory_group[field1+str('_')].isin(top_field1)]
    #by_factory_group.head(5)
    col_to_use1 = metric+'_sum'
    pivot_final_data = by_factory_group.pivot(
        index=[field1+'_'],
        columns=[field2+'_'],
        values=[col_to_use1]
    ).reset_index()
    pivot_final_data.rename(columns = {metric+'_sum':''}, inplace = True) 
    pivot_final_data.rename(columns = {field2+'_':field2}, inplace = True) 

    pivot_final_data.columns = pivot_final_data.columns.map(''.join)
    pivot_final_data
    percent_inbound=pivot_final_data
    #percent_inbound.head()
    heatmap_sum(percent_inbound,field1=field1,field2=field2,metric=metric)
def plot_heatmap_mean_cost(df,f1,f2,value1,value2,metric):
## Top Loading Locations 
    field1=f1
    top=5
    metric=metric
    top_field1=value1
    # top delivery locations
    field2=f2
    top=5
    metric=metric
    top_field2=value2
    
    # factory and warehouse loading mapping
    by_factory_group = df.groupby([field1,field2], as_index=False)\
        .agg({metric:['sum','mean']})
    by_factory_group.columns = by_factory_group.columns.map('_'.join)
    by_factory_group['percentage_sales']=round(by_factory_group[metric+'_sum']/sum(by_factory_group[metric+'_sum']),3)
    by_factory_group['Rank'] = by_factory_group['percentage_sales'].rank(ascending=False)
    by_factory_group=by_factory_group.sort_values(by=['percentage_sales'],ascending=False)
    # keeping only top values
    by_factory_group=by_factory_group[by_factory_group[field2+str('_')].isin(top_field2)]
    by_factory_group=by_factory_group[by_factory_group[field1+str('_')].isin(top_field1)]
    #by_factory_group.head(5)
    col_to_use1 = metric+'_mean'
    pivot_final_data = by_factory_group.pivot(
        index=[field1+'_'],
        columns=[field2+'_'],
        values=[col_to_use1]
    ).reset_index()
    pivot_final_data.rename(columns = {metric+'_mean':''}, inplace = True) 
    pivot_final_data.rename(columns = {field2+'_':field2}, inplace = True) 

    pivot_final_data.columns = pivot_final_data.columns.map(''.join)
    pivot_final_data
    percent_inbound=pivot_final_data
    #percent_inbound.head()
    heatmap_mean(percent_inbound,field1=field1,field2=field2,metric=metric)



def main():
    st.set_page_config(
        page_title="Multi-Page Streamlit App",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("IB Data EDA")

    # Create a sidebar with page selection
    page = st.sidebar.radio("Select Page", ["Inbound Cost", "ABC/XYZ on Outbound Data",'Inbound Shipment Time Anlysis'])
    if page == "Inbound Cost":
       
        st.header("Inbound")
        col_y, col_p = st.columns(2)
        with col_y:
            st.write('Year')
            options = cargosoft_data['year'].unique()
            year = st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=[2022,2023,2024]  # You can set default selections here
            )
        with col_p:
            st.write('Type of Loading')
            #options=cargosoft_data['Type of Loading'].unique()
            options=['Palletized']
            type_of_loading_l=st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=['Palletized']
            )
        col_d,col_x = st.columns(2)
        with col_d:
            st.write('Place of delivery')
            options = cargosoft_data['Place of Delivery'].unique()
            delivery_l = st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=['LANGENHAGEN', 'KREFELD', 'MEERANE', 'SCHWIEBERDINGEN', 'DREIEICH']
                #default=options
                )
        with col_x:
            st.write('Place of loading')
            options = cargosoft_data['Place of Loading'].unique()
            loading_l = st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=['RADOM', 'TARNOWO PODGORNE', 'LANGENHAGEN', 'MANISA', 'HAMBURG']
                #default=options
                )

        # st.write("You selected:", year)
        
        #radio_options = ["Place of loading","Place of delivery",'Product group','Type of Loading','month' ]
        #radio_selection = st.radio("Choose an option:", radio_options)
        col1,col2= st.columns(2)
        with col1:
            title=''
            plot_histo_2(cargosoft_data[cargosoft_data['year']==year],loading_l,delivery_l,cost_or_pallets='Packages',Year=year)

        # col2 = st.columns(1)
        with col2:
            plot_histo_2(cargosoft_data[cargosoft_data['year']==year],loading_l,delivery_l,cost_or_pallets='Costs',Year=year)
            #st.write('Hello 2')
        col3,col4= st.columns(2)
        with col3:
            plot_histo(cargosoft_data[cargosoft_data['year']==year],loading_l,delivery_l,cost_or_pallets='Packages',Year=year)

        # col2 = st.columns(1)
        with col4:
            plot_histo(cargosoft_data[cargosoft_data['year']==year],loading_l,delivery_l,cost_or_pallets='Costs',Year=year)
            #st.write('Hello 2')

        col5,col6= st.columns(2)
        with col5:
            st.write('Select Field 1')
            #options=cargosoft_data['Type of Loading'].unique()
            options=['Place of Loading','Place of Delivery','Product group']
            filed1=st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=['Palletized']
            )
        with col6:
            st.write('Select Field 2')
            options=['Place of Delivery','Place of Loading','Product group']
            filed2=st.selectbox(
                label='Select your options',
                options=options,
                index=0
                #default=['Palletized']
            ) 

        col7,col8=st.columns(2)
        with col7:
            st.write('Select the Values for '+ str(filed1))
            options = cargosoft_data[filed1].unique()
            values_field1 = st.multiselect(
                label='Select your options',
                options=options,
                default=cargosoft_data[filed1].unique()[:4]
                #default=options
                )
        with col8:
            st.write('Select the Values for '+ str(filed2))
            options = cargosoft_data[filed2].unique()
            values_field2 = st.multiselect(
                label='Select your options',
                options=options,
                default=cargosoft_data[filed2].unique()[:4]
                #default=options
                )
        st.write('Select Metric')
        options=['Costs','Packages']
        metric=st.selectbox(
            label='Select your options',
            options=options,
            index=0
            #default=['Palletized']
        )

        plot_heatmap_cost(cargosoft_data[cargosoft_data['year']==year],filed1,filed2,values_field1,values_field2,metric=metric)
        plot_heatmap_mean_cost(cargosoft_data[cargosoft_data['year']==year],filed1,filed2,values_field1,values_field2,metric='Cost per Package')
    # if page == "ABC/XYZ on Outbound Data":
    #     st.header("ABC/XYZ Anlysis")
    #     col_y, col_p = st.columns(2)
    #     with col_y:
    #         st.write('Year')
    #         options = cargosoft_data['year'].unique()
    #         year = st.multiselect(
    #             label='Select your options',
    #             options=options,
    #             default=[2022,2023,2024]  # You can set default selections here
    #         )
    #     with col_p:
    #         st.write('No. of Percentile bins')
    #         #options=cargosoft_data['Type of Loading'].unique()
    #         options=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    #         bin_size=st.selectbox(
    #             label='Select your options',
    #             options=options,
    #             index=4
    #             #default=['Palletized']
    #         )
    #     outbound=pd.read_csv('outbound_final.csv')
    #     outbound['PKT real']=outbound['PKT real'].round().astype(int)
    #     outbound['Material']=outbound['Material'].astype(str)
    #     outbound=outbound[outbound['year'].isin(year)]
    #     outbound['StandardDeviation'] = outbound.groupby('Material')['PKT real'].transform('std')
    #     outbound_by_Material_2 = outbound.groupby(['Material']).agg({'PKT real':'sum', 'StandardDeviation':'mean'}).reset_index()
    #     outbound_by_Material_2=create_percentile_bins(outbound_by_Material_2,'PKT real',bin_size)
    #     outbound_by_Material_2['Percent']=round((outbound_by_Material_2['PKT real']/sum(outbound_by_Material_2['PKT real']))*100,2)
    #     outbound_by_Material_2=outbound_by_Material_2.sort_values(by=('Percent'),ascending=False)
    #     outbound_by_Material_2['StandardDeviation']=round(outbound_by_Material_2['StandardDeviation'],2)
    #     bins = [0, 100, 200, float('inf')]  # Define the bin edges
    #     labels = ['Low', 'Medium', 'High']  # Define the labels for each bin
    #     # Add a new column with labels based on the value range of 'Values'
    #     outbound_by_Material_2['Standard Deviation'] = pd.cut(outbound_by_Material_2['StandardDeviation'], bins=bins, labels=labels, right=False)
    #     grouped_data2 = outbound_by_Material_2.groupby(['percentile_bin','Standard Deviation'])['PKT real'].sum().reset_index()
    #     grouped_data2['percentage_sales']=round((grouped_data2['PKT real']/sum(grouped_data2['PKT real']))*100,2)
    #     grouped_data2['Rank'] = grouped_data2['percentage_sales'].rank(ascending=False)
    #     grouped_data2=grouped_data2.sort_values(by=['percentage_sales'],ascending=True)
    #     #grouped_data2 = grouped_percentil.groupby(['percentile_bin','Standard Deviation'])['PKT real'].sum().reset_index()
    #     metric_use='percentage_sales'
    #     field1_use='percentile_bin'
    #     field2_use='Standard Deviation_'


    #     col_to_use1 = 'percentage_sales'
    #     pivot_final_data = grouped_data2.pivot(
    #     index=['percentile_bin'],
    #     columns=['Standard Deviation'],
    #     values=[col_to_use1]
    #     ).reset_index()

    #     pivot_final_data.rename(columns = {'percentage_sales':''}, inplace = True) 
    #     pivot_final_data.rename(columns = {field1_use:'percentile_bin'}, inplace = True) 
    #     pivot_final_data.columns = pivot_final_data.columns.map(''.join)
    #     percent_inbound=pivot_final_data
    #     percent_inbound
    #     plot_abc_xyz(percent_inbound)
if __name__ == "__main__":
    main()
