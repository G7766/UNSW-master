// Use the named values (val) below whenever your need to
// read/write inputs and outputs in your program. 

// Write your solution here
// COMP9313 Assignment2
// Name: PEIGUO GUAN  
// zID: z5143964
//import org.apache.spark.SparkConf
//import org.apache.spark.SparkContext._
//import org.apache.spark.SparkContext

class myfunction{
  def KB_MB_to_B(str:String):Long = {
      if ( str.contains("KB") == true){
        val newstr = str.substring(0,str.length()-2)
        val Intstr:Long = newstr.toInt * 1024
        //val finalstr:String = Intstr.toString + "B"
        return Intstr
      } else if(str.contains("MB") == true){
        val newstr = str.substring(0,str.length()-2)
        val Intstr:Long = newstr.toInt * 1024 * 1024
        //val finalstr:String = Intstr.toString + "B"
        return Intstr
      }else{
        val newstr = str.substring(0,str.length()-1)
        val Intstr:Long = newstr.toInt
        return Intstr
      }
  }
  def get_mean_and_varience(list: List[Long]):List[String] = {
    val min:Long = list(0)
    val max:Long = list(list.length-1) 
    var sum:Long = 0
    for(i<-0 to list.length-1){
      sum = sum + list(i)
    }
    val mean = sum/list.length
    var varience:Long = 0
    for(i<-0 to list.length-1){
      varience = varience + (list(i)-mean)*(list(i)-mean)
    }
    varience = varience/list.length
    
    //add in list and change to string + "B"
    var z = List(min.toString +"B", max.toString + "B", mean.toString + "B", varience.toString + "B")
    return z
  }
  def to_csv_line(str:String,list:List[String]):String = {
    var line = str
    for(i<-0 to list.length-1){
      line = line + ","+ list(i)
    }
    return line
  }
}



object Assignment2{

  def main(args:Array[String]): Unit = {
    val inputFilePath  = "/import/glass/3/z5143964/Ass2/sample_input.txt"
    val outputDirPath = "/import/glass/3/z5143964/Ass2/output"
    val input = sc.textFile(inputFilePath)


    val l1 = input.map(_.split("[\n , ]"))
    val l2 = l1.filter(!_.contains(""))
    val l3 = l2.map(pair => (pair(0),pair(3)))
    val l4 = l3.groupByKey()
    //println(l4.collect().toBuffer)
    //println("-------")
    //val l5_KB =l4.mapValues(_.filter(_.contains("KB")))
    val l6 = l4.mapValues(_.map(x => new myfunction().KB_MB_to_B(x)))
    
    //println(l6.collect().toBuffer)
    //println("-------")

    val l7 = l6.sortByKey()
    val l8 = l7.mapValues(_.toList.sortBy(x=>x))
    
    //println(l8.collect().toBuffer)
    //println("-------")

    val l9 = l8.mapValues(x => new myfunction().get_mean_and_varience(x))
    //println(l9.collect().toBuffer)
    val l10 = l9.map(x => new myfunction().to_csv_line(x._1,x._2))
    l10.coalesce(1,true).saveAsTextFile(outputDirPath)
    
    //*****    output as csv file  ****
    //println(l10.collect().toBuffer)
    //val l11 = l10.toDF()
    //println(l10.collect().toBuffer)
    //l11.write.format("csv").save(outputDirPath)
    //l10.saveAsTextFile(outputDirPath)
    

  }
}



//val pattern = "(k|K)(b|B)".r
//val mathKB = pattern.findFirstIn(test)
//!! bbb.contains("sd")      => true, false
//if (mathKB!=None){ println("true")}

//val bbb= "asdasda"
//bbb.length()
//val newbbb = bbb.substring(0,len-2)






