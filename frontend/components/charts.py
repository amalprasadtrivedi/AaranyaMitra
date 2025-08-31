"""
Reusable Chart Components for AaranyaMitra Frontend

This module provides:
1. Bar chart generator.
2. Pie chart generator.
3. Line chart generator (optional, for time-series or trend analysis).
4. Wrapper functions using matplotlib and Streamlit.

Author: Amal Prasad Trivedi
"""

import streamlit as st
import matplotlib.pyplot as plt


# ---------------------------
# BAR CHART
# ---------------------------
def plot_bar_chart(labels, values, title="Bar Chart", xlabel="", ylabel="", colors=None):
    """
    Create and display a bar chart.

    Args:
        labels (list): Categories for the x-axis.
        values (list): Numerical values for each category.
        title (str): Chart title.
        xlabel (str): X-axis label.
        ylabel (str): Y-axis label.
        colors (list): Optional list of colors for bars.
    """
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)


# ---------------------------
# PIE CHART
# ---------------------------
def plot_pie_chart(values, labels, title="Pie Chart", colors=None):
    """
    Create and display a pie chart.

    Args:
        values (list): Numerical values for each category.
        labels (list): Labels corresponding to each slice.
        title (str): Chart title.
        colors (list): Optional list of colors for slices.
    """
    fig, ax = plt.subplots()
    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )
    ax.set_title(title)
    ax.axis("equal")  # Equal aspect ratio ensures pie is circular
    st.pyplot(fig)


# ---------------------------
# LINE CHART
# ---------------------------
def plot_line_chart(x_values, y_values, title="Line Chart", xlabel="", ylabel="", color="blue"):
    """
    Create and display a line chart.

    Args:
        x_values (list): X-axis values (e.g., years, categories).
        y_values (list): Y-axis values (numerical).
        title (str): Chart title.
        xlabel (str): X-axis label.
        ylabel (str): Y-axis label.
        color (str): Line color.
    """
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, marker="o", linestyle="-", color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)
