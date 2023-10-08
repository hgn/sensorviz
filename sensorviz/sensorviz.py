#!/usr/bin/env python3

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # Import Matplotlib dates module
from datetime import datetime
import numpy as np


def replace_extension(filename, newext):
    root, ext = os.path.splitext(filename)
    return f"{root}.{newext}"


def year_boundaries(df_date_column):
    dates = []
    df_year = df_date_column.dt.year
    for year in sorted(set(df_year))[1:]:
        dates.append(datetime(year, 1, 1))
    return dates


def draw_year_separator(ax, df_date_column):
    years = year_boundaries(df_date_column)
    for year in years:
        ax.axvline(year, color="#A9A9A9", linestyle="solid")


def draw(ax, daily, monthly, date_column, data_column,
         average_temp, title, unit, color):
    # Calculate the overall average temperature
    ax.axhline(
        average_temp,
        color="gray",
        linestyle="dotted",
        label=title,
        alpha=0.8,
        linewidth=1,
    )

    ax.plot(daily.index, daily.values, linestyle="-", color=color, alpha=0.1, linewidth=3)
    ax.plot(
        monthly.index,
        monthly.values,
        marker="o",
        linestyle="-",
        color=color,
        markersize=8,
        linewidth=3,
    )
    ax.set_title(title, fontsize=12)
    ax.set_ylabel(f"{title} ({unit})", fontsize=12)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(True, alpha=0.5)

    max_temp_value = np.max(data_column)
    min_temp_value = np.min(data_column)
    max_temp_index = np.argmax(data_column)
    min_temp_index = np.argmin(data_column)
    max_temp_date = date_column[max_temp_index]
    min_temp_date = date_column[min_temp_index]
    ax.scatter(
        max_temp_date,
        max_temp_value,
        color="red",
        label=f"Max {title}",
        marker="o",
        s=20,
    )
    ax.annotate(
        f"Max: {max_temp_value:.1f}{unit}",
        (max_temp_date, max_temp_value),
        fontsize=8,
        textcoords="offset points",
        xytext=(10, 0),
        ha="left",
        bbox=dict(boxstyle="round, pad=0.4", edgecolor="none", facecolor="white"),
    )

    ax.scatter(
        min_temp_date,
        min_temp_value,
        color="green",
        label=f"Min {title}",
        marker="o",
        s=20,
    )
    ax.annotate(
        f"Min: {min_temp_value:.1f}{unit}",
        (min_temp_date, min_temp_value),
        fontsize=8,
        textcoords="offset points",
        xytext=(10, 0),
        ha="left",
        bbox=dict(boxstyle="round, pad=0.4", edgecolor="none", facecolor="white"),
    )

    # Format the x-ax1 to display "Month Year" for each month
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )  # Format as "Month Year"

    # Annotate each data point with temperature values
    for date, temp in zip(monthly.index, monthly.values):
        disp = "{:.1f}{}".format(float(temp), unit)
        ax.annotate(
            disp,
            (date, temp),
            fontsize=8,
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            bbox=dict(boxstyle="round, pad=0.4", edgecolor="none", facecolor="white"),
        )


def visualize_temp(df, ax1):
    date_column = "Date"
    temperature_column = "Temperature"

    df[date_column] = pd.to_datetime(df[date_column])

    daily = df.groupby(df[date_column].dt.date)[temperature_column].mean().reset_index()
    daily.set_index("Date", inplace=True)

    monthly = df.resample("M", on=date_column)[temperature_column].mean().reset_index()
    monthly.set_index("Date", inplace=True)

    average_temp = np.mean(df[temperature_column])

    draw_year_separator(ax1, df[date_column])
    draw(
        ax1,
        daily,
        monthly,
        df[date_column],
        df[temperature_column],
        average_temp,
        "Temperature",
        "°C",
        "blue",
    )


def visualize_hum(df, ax1):
    date_column = "Date"
    temperature_column = "Humanity"

    df[date_column] = pd.to_datetime(df[date_column])

    daily = df.groupby(df[date_column].dt.date)[temperature_column].mean().reset_index()
    daily.set_index("Date", inplace=True)

    monthly = df.resample("M", on=date_column)[temperature_column].mean().reset_index()
    monthly.set_index("Date", inplace=True)

    average_temp = np.mean(df[temperature_column])
    draw_year_separator(ax1, df[date_column])
    draw(
        ax1,
        daily,
        monthly,
        df[date_column],
        df[temperature_column],
        average_temp,
        "Humanity",
        "%",
        "magenta",
    )


def generate(filename: str) -> None:
    custom_column_names = ["Date", "Temperature", "Humanity"]
    df = pd.read_csv(filename, skiprows=1, names=custom_column_names)

    # Create a plot with custom styling and a thicker line (linewidth=3)
    fig, (ax1, ax2) = plt.subplots(
        figsize=(12, 12), nrows=2, ncols=1, sharex=True
    )  # Set the figure size

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    visualize_temp(df, ax1)
    visualize_hum(df, ax2)

    # Show the plot
    fig.autofmt_xdate()  # Automatically format x-axis labels for better readability
    plt.tight_layout()
    # Save as PNG
    new_filename = replace_extension(filename, "png")
    plt.savefig(new_filename, format="png", dpi=300, bbox_inches="tight")
    print(f"generated {new_filename}")
    # Save as PDF
    new_filename = replace_extension(filename, "pdf")
    plt.savefig(new_filename, format="pdf")
    print(f"generated {new_filename}")

    # plt.show()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: sensorviz <filename.csv>")
        return 1
    filename = sys.argv[1]
    generate(filename)
    return 0


if __name__ == "__main__":
    sys.exit(main())
