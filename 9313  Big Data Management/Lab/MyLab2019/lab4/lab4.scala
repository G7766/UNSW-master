import org.apache.spark.sql.SQLContext
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler

//start:
//spark-shell
// :load lab4.scala
// Lab4.main(Array())
object Lab4{
	def main(args:Array[String]){
		val FULL_PATH_OF_TRAINING_DATA_FILE = "/import/glass/3/z5143964/WordCount/iris_binary.csv"
		val sqlContext = new SQLContext(sc)
		val df =sqlContext.read.format("csv").option("header","true")
		.option("inferSchema","true")
		.load(FULL_PATH_OF_TRAINING_DATA_FILE)
		df.show(10)

		val vecAssemb = new VectorAssembler().setInputCols(Array("sepal_length",
		"sepal_width", "petal_length", "petal_width")).setOutputCol("features")

		val df2 = vecAssemb.transform(df)
		val df3 = df2.withColumnRenamed("species", "label")
		val df4 = df3.drop("sep_length").drop("sepal_width").drop("petal_length").drop("petal_width")
		
		//train
		val logReg = new LogisticRegression()
		val model = logReg.fit(df4)
		//predict
		val predict = model.transform(df4)
		val predictSummary = model.transform(df4).select("features","prediction","label")
		predictSummary.show(100)
	}


}