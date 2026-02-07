import pandas as pd
import numpy as np

# Load the CSV file
file_path = 'zerve_hackathon_for_reviewc8fa7c7.csv'
df = pd.read_csv(file_path)

print("=" * 80)
print("COMPREHENSIVE DATA INSPECTION")
print("=" * 80)

# 1. Dataset Dimensions
print("\n📊 DATASET DIMENSIONS")
print(f"Total Rows: {df.shape[0]:,}")
print(f"Total Columns: {df.shape[1]}")

# 2. Column Names and Types
print("\n📋 COLUMN INFORMATION")
print(f"\nColumns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\n🔧 DATA TYPES:")
print(df.dtypes.to_string())

# 3. Memory Usage
print("\n💾 MEMORY USAGE")
memory_usage = df.memory_usage(deep=True)
total_memory = memory_usage.sum() / (1024 ** 2)  # Convert to MB
print(f"Total Memory: {total_memory:.2f} MB")
print(f"\nTop 5 columns by memory usage:")
top_memory = memory_usage.sort_values(ascending=False).head(5)
for col, mem in top_memory.items():
    if col != 'Index':
        print(f"  {col}: {mem / (1024**2):.2f} MB")

# 4. Sample Rows
print("\n👁️  FIRST 5 ROWS")
print(df.head().to_string())

print("\n👁️  LAST 5 ROWS")
print(df.tail().to_string())

# 5. Event Structure Analysis
print("\n🔍 EVENT STRUCTURE ANALYSIS")
if 'event_type' in df.columns:
    print(f"Unique Event Types: {df['event_type'].nunique()}")
    print("\nEvent Type Distribution:")
    event_counts = df['event_type'].value_counts()
    for event, count in event_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {event}: {count:,} ({percentage:.2f}%)")
else:
    print("No 'event_type' column found")

# 6. ID Consistency Checks
print("\n🆔 ID CONSISTENCY CHECKS")
id_columns = [col for col in df.columns if 'id' in col.lower()]
if id_columns:
    for id_col in id_columns:
        unique_count = df[id_col].nunique()
        null_count = df[id_col].isnull().sum()
        print(f"\n  {id_col}:")
        print(f"    Total values: {len(df):,}")
        print(f"    Unique values: {unique_count:,}")
        print(f"    Null values: {null_count:,}")
        print(f"    Duplicate rate: {((len(df) - unique_count) / len(df) * 100):.2f}%")
        # Show sample IDs
        sample_ids = df[id_col].dropna().head(3).tolist()
        print(f"    Sample IDs: {sample_ids}")
else:
    print("No ID columns found")

# 7. Null Value Assessment
print("\n❌ NULL VALUE ASSESSMENT")
null_counts = df.isnull().sum()
null_percentages = (null_counts / len(df)) * 100
null_summary = pd.DataFrame({
    'Column': null_counts.index,
    'Null_Count': null_counts.values,
    'Null_Percentage': null_percentages.values
})
null_summary = null_summary[null_summary['Null_Count'] > 0].sort_values('Null_Count', ascending=False)

if len(null_summary) > 0:
    print("\nColumns with null values:")
    for _, row in null_summary.iterrows():
        print(f"  {row['Column']}: {int(row['Null_Count']):,} ({row['Null_Percentage']:.2f}%)")
else:
    print("✅ No null values found in any column")

# 8. Basic Statistics for Numeric Columns
print("\n📈 NUMERIC COLUMNS STATISTICS")
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    print(df[numeric_cols].describe().to_string())
else:
    print("No numeric columns found")

print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)