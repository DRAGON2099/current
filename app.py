import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Read data from the Excel file
excel_data = pd.read_excel('your_excel_file.xlsx')

@app.route('/')
def index():
    return render_template('codes.html')

@app.route('/search', methods=['POST'])
def search():
    # Get search parameters from the form
    search_type = request.form.get('search_type')
    value_to_search = request.form.get('value_to_search')

    # Define the column name based on the selected search type
    column_name = get_column_name(search_type)

    if column_name:
        # Create a condition for the selected column and search value
        condition = (excel_data[column_name] == float(value_to_search))

        # Add optional filters to the condition
        optional_filters = ["reduction", "uts", "elongation", "yield"]
        for filter_type in optional_filters:
            optional_filter_value = request.form.get('optional_filter_' + filter_type)
            if optional_filter_value:
                optional_column_name = get_column_name(filter_type)
                if optional_column_name:
                    condition &= (excel_data[optional_column_name] == float(optional_filter_value))

        # Filter data based on the condition
        filtered_data = excel_data[condition]

        # Convert filtered data to HTML table
        table_html = filtered_data.to_html(classes='table', index=False) if not filtered_data.empty else "<p>No matching records found.</p>"

        return render_template('codes.html', table_html=table_html)

    return render_template('codes.html', error_message="Invalid search type.")

def get_column_name(search_type):
    # Map search type to the corresponding column name
    column_mapping = {
        'uts': 'Ultimate Tensile Stress, [MPa]',
        'elongation': 'Tensile elongation [%]',
        'reduction': 'Reduction area [%]',
        'yield': 'Yield Stress, [MPa]'
    }
    return column_mapping.get(search_type)

if __name__ == '__main__':
    app.run(debug=True)
