import sqlite3  # import sqlite module/library

"Create a variable 'conn' and pass sqlite connect method to it "
"if the file doesnt exist it will create it. If it exists it will just use it."

conn = sqlite3.connect("")
"cursor method iterates through database/tables"
cursor = conn.cursor()
