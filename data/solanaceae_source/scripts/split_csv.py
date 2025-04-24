import sqlite3
import csv
import os

# Import CSV into SQLite database
def import_csv_to_db(csv_file, db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Read CSV headers and rows
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Sanitize and validate headers
        sanitized_headers = [
            header.replace('.', '_').strip() for header in headers if header.strip()
        ]
        
        if not sanitized_headers:  # Raise error if no valid headers are found
            raise ValueError("No valid headers found in the CSV file.")
        
        # Create table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(sanitized_headers)})")
        
        # Insert rows
        for row in reader:
            placeholders = ', '.join('?' * len(sanitized_headers))
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(sanitized_headers)}) VALUES ({placeholders})", row[:len(sanitized_headers)])
    
    conn.commit()
    conn.close()

# Export specific fields into separate CSV files
def export_fields_to_csv(db_file, table_name, fields, output_dir):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for field in fields:
        output_file = os.path.join(output_dir, f"{field}_output.csv")
        query = f"SELECT wfo, {field} FROM {table_name} WHERE {field} IS NOT NULL AND {field} != ''"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get headers
        headers = ['Wfo', field]
        
        # Write to CSV
        with open(output_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)  # Write header
            writer.writerows(results)  # Write rows
    
    conn.close()

# Main function
def main():
    csv_file = r'data\solanaceae_source\raw\Brahms_Solanaceae_descriptions_2024_22_28_UPDATED.csv'         # Path to the input CSV file
    db_file = r'data\solanaceae_source\work\sol_source.db'       # SQLite database file
    table_name = 'solanaceae_source'     # Name of the table in SQLite
    output_dir = r'data\solanaceae_source\out'        # Output directory for CSV files

    # Fields to split and export
    fields = [
        'Morphology', 'Cytology', 'General', 'Distribution', 
        'Ecology', 'Conservation', 'Vernacular', 'Use'
    ]

    # Import CSV into SQLite database
    import_csv_to_db(csv_file, db_file, table_name)

    # Export specified fields to individual CSV files
    export_fields_to_csv(db_file, table_name, fields, output_dir)

if __name__ == "__main__":
    main()