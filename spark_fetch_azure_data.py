jdbcHostName = "justine-server.database.windows.net"
jdbcPort = "1433"
jdbcDatabase = "Justine"
jdbcUserName = "justine"
jdbcPassword = "aloy@123"
jdbcDriver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

jdbcUrl = f"jdbc:sqlserver://{jdbcHostName}:{jdbcPort};databaseName={jdbcDatabase};user={jdbcUserName};password={jdbcPassword}"

df = spark.read.format("jdbc").option("url",jdbcUrl).option("dbtable","SalesLT.Product").load()
display(df)
df = df.na.fill({"Size":"Size not provided"})
df=df.dropDuplicates()
df=df.cache()
display(df)

df1=spark.read.format("jdbc").option("url",jdbcUrl).option("dbtable","SalesLT.ProductCategory").load()

df_join = df.join(df1, df.ProductCategoryID==df1.ProductCategoryID, "leftouter").select(df.Name,df1.rowguid)

display(df_join)
df_join.write.format("jdbc").option("url",jdbcUrl).option("dbtable","SalesLT.JoinTable").mode("append").save()
