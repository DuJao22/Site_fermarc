import sqlite3

conn = sqlite3.connect('instance/ecommerce.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE product ADD COLUMN image_url_2 VARCHAR(500)")
    print("✓ Coluna image_url_2 adicionada")
except sqlite3.OperationalError as e:
    print(f"image_url_2: {e}")

try:
    cursor.execute("ALTER TABLE product ADD COLUMN image_url_3 VARCHAR(500)")
    print("✓ Coluna image_url_3 adicionada")
except sqlite3.OperationalError as e:
    print(f"image_url_3: {e}")

try:
    cursor.execute("ALTER TABLE product ADD COLUMN image_url_4 VARCHAR(500)")
    print("✓ Coluna image_url_4 adicionada")
except sqlite3.OperationalError as e:
    print(f"image_url_4: {e}")

try:
    cursor.execute("ALTER TABLE product ADD COLUMN image_url_5 VARCHAR(500)")
    print("✓ Coluna image_url_5 adicionada")
except sqlite3.OperationalError as e:
    print(f"image_url_5: {e}")

conn.commit()
conn.close()
print("\n✓ Migração concluída com sucesso!")
