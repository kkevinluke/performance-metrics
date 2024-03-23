import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def calculate_overall_score(quality, productivity, efficiency, pkt):
    # Assign weights
    quality_weight = 0.35
    productivity_weight = 0.35
    efficiency_weight = 0.25
    pkt_weight = 0.05

    # Calculate individual scores
    quality_score = quality * quality_weight
    productivity_score = productivity * productivity_weight
    efficiency_score = efficiency * efficiency_weight
    pkt_score = pkt * pkt_weight

    # Calculate overall score
    overall_score = quality_score + productivity_score + efficiency_score + pkt_score
    return overall_score

def update_table(df, name, date, quality, productivity, efficiency, pkt):
    # Create DataFrame for new row
    new_row = pd.DataFrame({
        'Name': [name],
        'Date': [date],
        'Quality': [quality],
        'Productivity': [productivity],
        'Efficiency': [efficiency],
        'PKT': [pkt]
    })
    
    # Concatenate DataFrame with new row
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Calculate overall score
    df['Overall Score'] = df.apply(lambda row: calculate_overall_score(row['Quality'], row['Productivity'], row['Efficiency'], row['PKT']), axis=1)
    
    return df

def display_bar(df):
    # Plotting
    plt.figure(figsize=(15, 6))
    
    # Define colors for each metric
    colors = ['b', 'g', 'r', 'c', 'm']
    
    # Define bar width and space between metrics
    bar_width = 0.1
    space_between = 0.05
    
    # Loop through each metric and plot a bar graph
    for i, column in enumerate(df.columns[2:]):
        plt.bar(df.index + (i * (bar_width + space_between)), df[column], width=bar_width, color=colors[i], label=column)

    plt.xlabel('Employee')
    plt.ylabel('Scores')
    plt.title("Employee's Quality Scores")
    plt.xticks(df.index + ((len(df.columns[2:]) - 1) / 2) * (bar_width + space_between), df['Name'])  # Adjust x-axis ticks
    plt.legend()
    plt.tight_layout()

    # Annotate each bar with its corresponding metric
    for i, column in enumerate(df.columns[2:]):
        for j, value in enumerate(df[column]):
            plt.text(j + i * (bar_width + space_between), value + 1, str(value), ha='center', va='bottom', fontsize=8)

    st.pyplot()

def display_pi(df):
    # Define colors for each metric
    colors = ['b', 'g', 'r', 'c', 'm']

    # Define labels for each metric
    labels = df.columns[2:-1]  # Exclude 'Overall Score'

    # Loop through each employee and plot a pie chart for each
    for i, row in df.iterrows():
        scores = row[2:-1].tolist()  # Extract scores for each metric, excluding 'Overall Score'
        total_score = sum(scores)  # Total score for the employee

        # Calculate proportions for each metric
        proportions = [score / total_score for score in scores]

        # Create a pie chart with custom segment sizes
        plt.figure(figsize=(6, 6))
        plt.pie(proportions, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title("Employee: {} Quality Scores".format(row['Name']))

        st.pyplot()

# Main Streamlit app
def main():
    st.title("Employee Performance Evaluation")

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Name', 'Date', 'Quality', 'Productivity', 'Efficiency', 'PKT', 'Overall Score'])

    # Collect user input for employee evaluation
    while True:
        name = st.text_input("Enter name of employee:")
        date = st.text_input("Enter date in dd/mm/yyyy format for {}: ".format(name))
        quality = st.number_input("Enter the quality score (out of 100) for {}: ".format(name), min_value=0, max_value=100, value=0)
        productivity = st.number_input("Enter the productivity score (out of 100) for {}: ".format(name), min_value=0, max_value=100, value=0)
        efficiency = st.number_input("Enter the efficiency score (out of 100) for {}: ".format(name), min_value=0, max_value=100, value=0)
        pkt = st.number_input("Enter the PKT score (out of 100) for {}: ".format(name), min_value=0, max_value=100, value=0)
        if st.button("Add Employee"):
            df = update_table(df, name, date, quality, productivity, efficiency, pkt)

        # Display scores as bar chart and pie chart
        display_bar(df)
        display_pi(df)

if __name__ == "__main__":
    main()
