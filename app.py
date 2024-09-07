import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sample Data Preparation (Check array lengths)
data = {
    'month': pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%Y-%m'),
    'cpt_code': ['CPT001'] * 12 + ['CPT002'] * 12,  # 24 entries total
    'count': [100, 110, 120, 130, 125, 115, 135, 145, 155, 150, 140, 130] * 2,  # 24 entries
    'denial_rate': [0.1, 0.12, 0.11, 0.09, 0.08, 0.15, 0.13, 0.1, 0.09, 0.07, 0.06, 0.05] * 2  # 24 entries
}

# Ensure all columns are the same length (for debugging)
print(f"Length of 'month': {len(data['month'])}")
print(f"Length of 'cpt_code': {len(data['cpt_code'])}")
print(f"Length of 'count': {len(data['count'])}")
print(f"Length of 'denial_rate': {len(data['denial_rate'])}")

# Now create the DataFrame (all arrays must have the same length)
df = pd.DataFrame(data)

# Function to calculate the allowed amount based on denial rate
def calculate_allowed_amount(cpt_count, denial_rate):
    # Assume allowed amount is calculated as (cpt_count * (1 - denial_rate)) * some_factor
    factor = 100  # This can be adjusted based on the actual formula
    return cpt_count * (1 - denial_rate) * factor

# Add calculated 'allowed_amount' column to the dataframe
df['allowed_amount'] = df.apply(lambda row: calculate_allowed_amount(row['count'], row['denial_rate']), axis=1)

# Streamlit App Interface
st.title('What-If Analysis: CPT Code Denial Rate Impact')

# CPT Code Selection
selected_cpt = st.selectbox('Select CPT Code:', df['cpt_code'].unique())

# Filter data based on the selected CPT code
filtered_df = df[df['cpt_code'] == selected_cpt]

# Display Actual Allowed Amount
st.subheader(f'Actual Allowed Amount for {selected_cpt}')
st.write(filtered_df[['month', 'count', 'denial_rate', 'allowed_amount']])

# Denial Rate Adjustment Slider
adjusted_denial_rate = st.slider('Adjust Denial Rate:', min_value=0.0, max_value=1.0, step=0.01, value=filtered_df['denial_rate'].mean())

# Calculate new allowed amounts with adjusted denial rate
filtered_df['adjusted_allowed_amount'] = filtered_df['count'].apply(lambda x: calculate_allowed_amount(x, adjusted_denial_rate))

# Plot the Comparison using Plotly
fig = go.Figure()

# Actual Allowed Amount line
fig.add_trace(go.Scatter(
    x=filtered_df['month'],
    y=filtered_df['allowed_amount'],
    mode='lines+markers',
    name='Actual Allowed Amount',
    line=dict(color='blue'),
    marker=dict(size=8)
))

# Adjusted Allowed Amount line
fig.add_trace(go.Scatter(
    x=filtered_df['month'],
    y=filtered_df['adjusted_allowed_amount'],
    mode='lines+markers',
    name=f'Adjusted Allowed Amount (Denial Rate = {adjusted_denial_rate:.2f})',
    line=dict(color='orange'),
    marker=dict(size=8)
))

# Update layout
fig.update_layout(
    title=f'Allowed Amount Comparison for {selected_cpt}',
    xaxis_title='Month',
    yaxis_title='Allowed Amount',
    xaxis_tickangle=-45,
    legend_title='Legend',
    hovermode='x'
)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)

# Display adjusted data
st.subheader(f'Adjusted Allowed Amount for {selected_cpt}')
st.write(filtered_df[['month', 'count', 'denial_rate', 'adjusted_allowed_amount']])
