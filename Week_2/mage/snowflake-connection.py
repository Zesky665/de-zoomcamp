import snowflake.connector as snow

connection = snow.connect(
    account='abc-123',
    user='username',
    password='password',
    warehouse='WEEK_2_DE_ZC_SVC_WH',
    database='WEEK_2_DE_ZC_DB',
    schema='WEEK_2_DE_ZC_DB_SCHEMA'
)

# Define a cursor
cursor = connection.cursor()

try:
    # Execute a SQL query against Snowflake to get the current_version
    cursor.execute("SELECT current_version()")
    one_row = cursor.fetchone()

    # Display the version information
    print("Connection Successful")
    print(one_row[0])

finally:
    print("Connection Closed")
    cursor.close()

connection.close()