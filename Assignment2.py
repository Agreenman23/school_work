# Databricks notebook source
#ALEX GREENMAN

sc = spark.sparkContext
import os
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.types import IntegerType, StructType, StructField, LongType, StringType, DoubleType, TimestampType
from pyspark.ml.feature import StringIndexer, Bucketizer
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import OneHotEncoderEstimator
import pyspark.sql.functions as f
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


#create directories to store CSV files containing partitioned test data
dbutils.fs.mkdirs("FileStore/tables/Assignment2/partitioned_files")
dbutils.fs.mkdirs("FileStore/tables/Assignment2/partitioned_files_balanced")


fileDirectory = '/dbfs/FileStore/tables/'
direc = '/FileStore/tables/'

#move source data to specified directory
for filename in os.listdir(fileDirectory):
  if "stroke" in filename:
    dbutils.fs.mv(direc+filename, "FileStore/tables/Assignment2")

# COMMAND ----------

#read in CSV with user defined schema
strokeSchema = StructType( \
[StructField('id',IntegerType(),True), \
StructField('gender',StringType(),True), \
StructField('age',DoubleType(),True), \
StructField('hypertension',IntegerType(),True), \
StructField('heart_disease',IntegerType(),True), \
StructField('ever_married',StringType(),True), \
StructField('work_type',StringType(),True), \
StructField('Residence_type',StringType(),True), \
StructField('avg_glucose_level',DoubleType(),True), \
StructField('bmi',DoubleType(),True), \
StructField('smoking_status',StringType(),True), \
StructField('stroke', IntegerType(), True)
])

strokeDF = spark.read.format("csv").option("header", True).schema(strokeSchema).option("ignoreLeadingWhiteSpace", True).option("mode", "dropMalformed").load("FileStore/tables/Assignment2/stroke_data.csv")


#rename stroke column to label for pipeline purposes
strokeDF = strokeDF.withColumnRenamed("stroke", "label")

strokeDF.printSchema()

# COMMAND ----------

#get dataframe shape before drop
print((strokeDF.count(), len(strokeDF.columns)))

#address missing values
strokeDF.na.drop(subset=["smoking_status"])
bmi_mean = strokeDF.select(f.mean(strokeDF['bmi'])).collect()
bmi_mean = bmi_mean[0][0]
strokeDF = strokeDF.na.fill(bmi_mean,['bmi'])

#test to see if there are any lingering null values in the data 
strokeDF = strokeDF.na.drop()

#confirm no nulls remain
print((strokeDF.count(), len(strokeDF.columns)))

# COMMAND ----------

#get categorical columns from data based on dtype
categorical_cols = [item[0] for item in strokeDF.dtypes if item[1].startswith('string')]

#get numeric columns from data based on dtype
numeric_cols = [item[0] for item in strokeDF.dtypes if (item[1].startswith('double') and item[0]!= 'id')]
numeric_cols.extend([item[0] for item in strokeDF.dtypes if (item[1].startswith('int')and item[0]!= 'id')])

#view column groups
print(categorical_cols)
print(numeric_cols)

#get summary statistics of all numeric columns to better understand data
strokeDF[[numeric_cols]].summary().show()

#get count of categorical column values to better understand data
strokeDF.groupBy('gender').count().show()
strokeDF.groupBy('ever_married').count().show()
strokeDF.groupBy('work_type').count().show()
strokeDF.groupBy('Residence_type').count().show()
strokeDF.groupBy('smoking_status').count().show()
strokeDF.groupBy('label').count().show()

#clearly outcome variable is imbalanced, will need to be addressed

# COMMAND ----------

#begin data transformation process for categorical variables; stages does not include model yet
stages = [] 
for categoricalCol in categorical_cols:
  #index categorical variables
  stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol + "_index")
  #convert categorical variables into binary SparseVectors
  encoder = OneHotEncoderEstimator(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoricalCol + "_classVec"])
  stages += [stringIndexer, encoder]

assemblerInputs = [c + "_classVec" for c in categorical_cols] + numeric_cols
assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
stages += [assembler]

# COMMAND ----------

train_data, test_data = strokeDF.randomSplit([0.7, 0.3], seed=12345)

#address class imbalance by creating weight column which places more emphasis on minority class (no stroke) so classifier can 'learn' equally from all classes
dataset_size=train_data.select("label").count()
num_positives=train_data.select("label").where("label == 1").count()
per_ones=(float(num_positives)/float(dataset_size))*100
num_negatives=float(dataset_size-num_positives)

balancing_ratio= num_negatives/float(dataset_size)
train_data=train_data.withColumn("classWeights", f.when(train_data['label'] == 1,balancing_ratio).otherwise(1-balancing_ratio))
train_data.select("classWeights").where("label ==1").show(10)
train_data.select("classWeights").where("label == 0").show(10)

# COMMAND ----------

lrModel = LogisticRegression(maxIter=10, featuresCol = 'features', labelCol = 'label', weightCol="classWeights")
stages += [lrModel]
#create pipeline object and train model on training data
p = Pipeline().setStages(stages)
pModel = p.fit(train_data)

# COMMAND ----------

#get shape information of test data
print((test_data.count(), len(test_data.columns)))

test_num_positives=test_data.select("label").where("label == 1").count()

print(test_num_positives)

#verify num partitions of test_data
print(test_data.rdd.getNumPartitions()) 

#repartition test data into 25 files
partitioned_test_data = test_data.repartition(25)

print(partitioned_test_data.rdd.getNumPartitions()) 

dbutils.fs.rm("/FileStore/tables/Assignment2/partitioned_files/", True)

partitioned_test_data.write.format("csv").option("header", True).save("/FileStore/tables/Assignment2/partitioned_files/")

# COMMAND ----------

#create schema for csv data being streamed in
strokeSchemaStream = StructType( \
[StructField('id',IntegerType(),True), \
StructField('gender',StringType(),True), \
StructField('age',DoubleType(),True), \
StructField('hypertension',IntegerType(),True), \
StructField('heart_disease',IntegerType(),True), \
StructField('ever_married',StringType(),True), \
StructField('work_type',StringType(),True), \
StructField('Residence_type',StringType(),True), \
StructField('avg_glucose_level',DoubleType(),True), \
StructField('bmi',DoubleType(),True), \
StructField('smoking_status',StringType(),True), \
StructField('label', IntegerType(), True)
])

#create stresm with maxFilesPerTrigger
sourceStream = spark.readStream.format("csv").option("header", True).schema(strokeSchemaStream).option("ignoreLeadingWhiteSpace", True).option("mode", "dropMalformed").option("maxFilesPerTrigger", 1).load("/FileStore/tables/Assignment2/partitioned_files/")

#transform data being streamed in
streamingRates = pModel.transform(sourceStream)

#create a column that indicates whether or not the model made a correct prediction
streamingRates = streamingRates.withColumn('match', f.when(f.col('label') == f.col('prediction'),1))
#for each section of data being streamed, groupby label (0 and 1), show the percentage of classifications that are correct along with their counts
streamingRates = streamingRates.groupBy('label').agg((f.sum(f.col('match'))/f.count('label')).alias("Correct Prediction Rate"),f.count('label').alias('count'))

display(streamingRates)

#to see features and predictions 
# display(streamingRates.select('label', 'features', 'prediction'))

# COMMAND ----------

#drop classWeights column, as the data will be 'manually' balanced below
strokeDF = strokeDF.drop('classWeights')
#get number of positives
pos_count=strokeDF.select("*").where("label == 1").count()
print(pos_count)
posDF=strokeDF.select("*").where("label == 1")
#get equal number of negatives
negDF = strokeDF.select("*").where("label == 0").limit(pos_count)

#combine into one new dataframe
balancedDF = posDF.union(negDF)
train_data_balanced, test_data_balanced = balancedDF.randomSplit([0.7, 0.3], seed=12345)

# COMMAND ----------

lrModel_1 = LogisticRegression(maxIter=10, featuresCol = 'features', labelCol = 'label')
#remove existing LR Model from stage; other stage items can be reused
stages = stages[:-1]
stages += [lrModel_1]
#now train model on newly balanced data set
p = Pipeline().setStages(stages)
pModel = p.fit(train_data_balanced)

# COMMAND ----------

#get shape information of test data balanced
print((test_data_balanced.count(), len(test_data_balanced.columns)))

test_data_balanced_num_positives=test_data_balanced.select("label").where("label == 1").count()

print(test_data_balanced_num_positives)

#verify num partitions of test_data balanced
print(test_data_balanced.rdd.getNumPartitions()) 

#repartition test data into 15 files
partitioned_test_data_balanced = test_data_balanced.repartition(15)

print(partitioned_test_data_balanced.rdd.getNumPartitions()) 

dbutils.fs.rm("/FileStore/tables/Assignment2/partitioned_files_balanced/", True)

partitioned_test_data_balanced.write.format("csv").option("header", True).save("/FileStore/tables/Assignment2/partitioned_files_balanced/")

# COMMAND ----------

sourceStream = spark.readStream.format("csv").option("header", True).schema(strokeSchemaStream).option("ignoreLeadingWhiteSpace", True).option("mode", "dropMalformed").option("maxFilesPerTrigger", 1).load("/FileStore/tables/Assignment2/partitioned_files_balanced/")

streamingRates = pModel.transform(sourceStream)

streamingRates = streamingRates.withColumn('match', f.when(f.col('label') == f.col('prediction'),1))
streamingRates = streamingRates.groupBy('label').agg((f.sum(f.col('match'))/f.count('label')).alias("Correct Prediction Rate"),f.count('label').alias('count'))


# display(streamingRates.select('label','features','prediction'))
display(streamingRates)
