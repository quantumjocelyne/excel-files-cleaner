import matplotlib.pyplot as plt
import glob
import os
from fuzzywuzzy import fuzz, process
import warnings
import pandas as pd

warnings.filterwarnings("ignore", module="fuzzywuzzy")

def find_header_row(df, expected_header_names, unwanted_header_elements):
    # Iterate through rows and search for a row that closely matches the expected header names
    for i, row in enumerate(df.iterrows()):
        row_text = " ".join(str(cell) for cell in row[1])

        # Check if any unwanted header element exists in the row_text
        if any(unwanted in row_text for unwanted in unwanted_header_elements):
            continue

        # Use fuzzy matching to compare the row text to expected header names
        best_match = find_best_match(row_text, expected_header_names)
        ratio = fuzz.token_set_ratio(row_text.lower(), best_match.lower())
        if ratio >= 80:  # Adjust the threshold as needed
            return i
    return None

def find_best_match(needle, haystack):
    best_match, _ = process.extractOne(needle, haystack)
    return best_match

def clean_and_process_excel_files(path, expected_header_names, unwanted_header_elements):
    excel_files = glob.glob(os.path.join(path, "*.xls"))
    if not excel_files:
        print("No valid Excel files found.")

    num_files = len(excel_files)
    num_cols = 2
    num_rows = (num_files + 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 13))

    for i, file in enumerate(excel_files):
        try:
            print(f"Processing file: {file}")
            file_extension = os.path.splitext(file)[1]
            if file_extension.lower() == ".xls":
                df = pd.read_excel(file, header=None)
                # Find the best-matching header name for 'Datum/Uhrzeit'
                datum_uhrzeit_header = find_best_match("Datum/Uhrzeit", expected_header_names)
                header_row = find_header_row(df, expected_header_names, unwanted_header_elements)
                print(f"Header row: {df.iloc[header_row].values}")
                if header_row is not None:
                    df = pd.read_excel(file, skiprows=header_row)
                else:
                    raise Exception("Header row not found")
            else:
                raise Exception("Invalid file format")

            row = i // num_cols
            col = i % num_cols

            ax_left = axs[row, col]
            ax_right = ax_left.twinx()

            # Dynamically get the temperature and relative humidity headers based on expected header names (column-matching logic
            # robuist to handle variations in column names dynamically across different files)
            temp_headers = [col for col in df.columns if "Temperatur" in str(col) or "Lufttemperatur" in str(col)]
            rh_headers = [col for col in df.columns if "Feuchtigkeit" in str(col) or "Luftfeuchte" in str(col)]

            if temp_headers and rh_headers:
                temp_header = temp_headers[0]
                rh_header = rh_headers[0]

                #ax_left.plot(df[datum_uhrzeit_header], df[temp_header], color='red', linewidth=0.6)
                #ax_right.plot(df[datum_uhrzeit_header], df[rh_header], color='blue', linewidth=0.6)


                ax_left.plot(df["Datum/Uhrzeit"], df[temp_header], color='red', linewidth=0.6)
                ax_right.plot(df["Datum/Uhrzeit"], df[rh_header], color='blue', linewidth=0.6)

                # Display a subset of the timestamps on the x-axis
                num_ticks = 10  # adjust this as needed
                ticks = df["Datum/Uhrzeit"].iloc[::len(df) // num_ticks].values
                ax_left.set_xticks(ticks)
                ax_left.set_xticklabels(ticks, rotation=45, ha='right')


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

                file_name = os.path.splitext(os.path.basename(file))[0]
                ax_left.set_title(file_name)
            else:
                print(f"Temperature and/or relative humidity headers not found in {file}.")

        except Exception as e:
            print(f"Error processing file {file}: {e}")
            
    # If the total number of plots is odd, remove the last empty subplot
    if num_files % 2 != 0:
        fig.delaxes(axs[-1, -1])

    if num_files > 0:
        plt.tight_layout()
        save_path = os.path.join(path, "combined_plot_data.png")
        plt.savefig(save_path, dpi=500, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    else:
        print("No valid data found in the Excel files.")

# Define the expected header names to match
expected_header_names = ["Datum/Uhrzeit", "Temperatur[°C]", "rel.Luftfeuchte[%rF]", "Lufttemperatur[°C]", "%Feuchtigkeit[%rF]"]
# Define the unwanted header elements
unwanted_header_elements = ["Temperatur [°C]", "rel.Luftfeuchte [%rF]", "Lufttemperatur [°C]", "%Feuchtigkeit [%rF]"]

clean_and_process_excel_files("C:\\Users\Bisagny\OneDrive\Documents\Corak AG\Datenlogger", expected_header_names, unwanted_header_elements)