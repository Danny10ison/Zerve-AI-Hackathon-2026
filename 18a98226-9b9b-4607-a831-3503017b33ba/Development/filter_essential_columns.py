import pandas as pd

# Filter to essential columns that capture success metrics
essential_columns = [
    # User/Session IDs
    'distinct_id',
    'person_id',
    'prop_$session_id',
    'prop_session_id',
    'prop_$user_id',
    'prop_user_id',
    
    # Temporal data
    'timestamp',
    'created_at',
    
    # Event tracking
    'event',
    
    # Success indicators - credits and tool usage
    'prop_credits_used',
    'prop_credit_amount',
    'prop_tool_name',
    
    # Additional context for workflows
    'prop_$pathname',
    'prop_message_id'
]

# Filter columns that exist in the dataframe
existing_columns = [col for col in essential_columns if col in df.columns]

# Create filtered dataset
filtered_df = df[existing_columns].copy()

print("=" * 80)
print("ESSENTIAL COLUMNS FILTERING COMPLETE")
print("=" * 80)

print(f"\n📊 FILTERING SUMMARY")
print(f"Original columns: {df.shape[1]}")
print(f"Essential columns: {len(existing_columns)}")
print(f"Columns removed: {df.shape[1] - len(existing_columns)}")
print(f"Rows retained: {filtered_df.shape[0]:,}")

print(f"\n✅ RETAINED COLUMNS ({len(existing_columns)}):")
for i, col in enumerate(existing_columns, 1):
    print(f"  {i}. {col}")

print(f"\n🎯 SUCCESS METRICS CAPTURED:")
print(f"  ✓ User/Session IDs: distinct_id, person_id, session_id variants, user_id variants")
print(f"  ✓ Temporal data: timestamp, created_at")
print(f"  ✓ Event tracking: event")
print(f"  ✓ Success indicators: credits_used, credit_amount, tool_name")
print(f"  ✓ Workflow context: pathname, message_id")

print(f"\n📈 DATA PREVIEW:")
print(filtered_df.head(10).to_string())

print(f"\n💾 MEMORY SAVINGS:")
original_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
filtered_memory = filtered_df.memory_usage(deep=True).sum() / (1024 ** 2)
memory_saved = original_memory - filtered_memory
savings_percentage = (memory_saved / original_memory) * 100

print(f"  Original: {original_memory:.2f} MB")
print(f"  Filtered: {filtered_memory:.2f} MB")
print(f"  Saved: {memory_saved:.2f} MB ({savings_percentage:.1f}% reduction)")

print(f"\n🔍 COLUMN DETAILS:")
for col in existing_columns:
    non_null = filtered_df[col].notna().sum()
    null_pct = (filtered_df[col].isna().sum() / len(filtered_df)) * 100
    unique_vals = filtered_df[col].nunique()
    print(f"\n  {col}:")
    print(f"    Non-null: {non_null:,} ({100-null_pct:.1f}%)")
    print(f"    Unique values: {unique_vals:,}")

print("\n" + "=" * 80)