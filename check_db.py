import sqlite3

conn = sqlite3.connect("quotes.db")
cursor = conn.cursor()

# Count total quotes
cursor.execute("SELECT COUNT(*) FROM quotes")
count = cursor.fetchone()
print(f"Total quotes: {count[0]}")

# Show first 3 quotes
print("\n--- First 3 Quotes ---")
cursor.execute("SELECT * FROM quotes LIMIT 3")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Show all Einstein quotes
print("\n--- Einstein Quotes ---")
cursor.execute("SELECT * FROM quotes WHERE author = 'Albert Einstein'")
einstein = cursor.fetchall()
for row in einstein:
    print(row)

conn.close()