import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Import the fuzzywuzzy library and disable the warning
from fuzzywuzzy import fuzz, process
import warnings

warnings.filterwarnings("ignore", module="fuzzywuzzy")

def process_excel_files(path):
    excel_files = glob.glob(path + "/*.xls")
    if not excel_files:
        print("No valid Excel files found.")
        return

    num_files = len(excel_files)
    num_cols = 2  # Number of columns for subplot arrangement
    num_rows = (num_files + 1) // num_cols  # Number of rows for subplot arrangement

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 13))

    for i, file in enumerate(excel_files):
        try:
            print(f"Processing file: {file}")
            df = pd.read_excel(file, skiprows=12)
            if len(df.columns) >= 4:
                df = df.iloc[:, :4]
                df.columns = ["id", "Datum/Uhrzeit", "Temperature", "Relative Humidity"]
                df = df.dropna(subset=["id"])
                df['Datum/Uhrzeit'] = pd.to_datetime(df['Datum/Uhrzeit'], dayfirst=True, errors='coerce')
                df = df.dropna(subset=["Datum/Uhrzeit"])

                row = i // num_cols
                col = i % num_cols

                ax_left = axs[row, col]
                ax_right = ax_left.twinx()

                ax_left.plot(df['Datum/Uhrzeit'], df['Temperature'], color='red', linewidth=0.6)
                ax_right.plot(df['Datum/Uhrzeit'], df['Relative Humidity'], color='blue', linewidth=0.6)

                ax_left.set_ylabel('Temperature [°C]')
                ax_right.set_ylabel('Relative Humidity [%rF]')

                ax_left.set_ylim(10, 30)
                ax_right.set_ylim(25, 70)

                ax_left.tick_params(axis='y', colors='red')
                ax_right.tick_params(axis='y', colors='blue')

                ax_left.spines['right'].set_visible(False)
                ax_left.spines['left'].set_color('red')
                ax_right.spines['left'].set_visible(False)
                ax_right.spines['right'].set_color('blue')

                ax_left.yaxis.labelpad = 15
                ax_right.yaxis.labelpad = 15

                ax_left.spines['top'].set_visible(False)
                ax_left.spines['bottom'].set_visible(True)
                ax_right.spines['top'].set_visible(False)
                ax_right.spines['bottom'].set_visible(True)

                ax_left.xaxis.set_ticks_position('bottom')
                ax_right.xaxis.set_ticks_position('bottom')

                ax_left.tick_params(axis='x', bottom=True)
                ax_right.tick_params(axis='x', bottom=True)


                """
                ax_left.legend().remove()
                ax_right.legend().remove()"""


                ax_left.xaxis.set_major_locator(plt.MaxNLocator(50))  # Set maximum number of x-axis tick labels
                ax_left.xaxis.set_tick_params(rotation=45, labelsize=7)  # Adjust rotation and fontsize of tick labels
                ax_right.xaxis.set_major_locator(plt.MaxNLocator(50))
                ax_right.xaxis.set_tick_params(rotation=45, labelsize=7)

                # Set subplot title as the file name
                file_name = os.path.splitext(os.path.basename(file))[0]
                ax_left.set_title(file_name)

            else:
                raise Exception("Invalid data format")
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    if num_files > 0:

        plt.tight_layout()

        save_path = os.path.join(path, "combined_plot.png")
        plt.savefig(save_path, dpi=500, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    else:
        print("No valid data found in the Excel files.")



# Example usage:
process_excel_files("C:\\Users\Bisagny\OneDrive\Documents\Corak AG\Datenlogger")