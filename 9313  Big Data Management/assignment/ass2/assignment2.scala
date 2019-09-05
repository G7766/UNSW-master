// Use the named values (val) below whenever your need to
// read/write inputs and outputs in your program. 

// Write your solution here
// COMP9313 Assignment2
// Name: PEIGUO GUAN  
// zID: z5143964


// define my class
class myfunction{
  // define a function to change KB or MB to B, 
  // but also change from String to Long
  // (cause if the length is too large Integer can not meet the requirement)
  // so the input type is String and Output type is Long 
  def KB_MB_to_B(str:String):Long = {
      if ( str.contains("KB") == true){
        val newstr = str.substring(0,str.length()-2)
        val Intstr:Long = newstr.toInt * 1024
        return Intstr
      } else if(str.contains("MB") == true){
        val newstr = str.substring(0,str.length()-2)
        val Intstr:Long = newstr.toInt * 1024 * 1024
        return Intstr
      }else{
        val newstr = str.substring(0,str.length()-1)
        val Intstr:Long = newstr.toInt
        return Intstr
      }
  }
  // define a function to calculate mean value and varience value
  // after finish calculate the result then change to String and add "B"
  // the input type si List[Long] the output is List[Long]
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
  // define a function to keep all in one line
  // this can help to cahnge from RDD to DataFrame if required
  // and if the requirement is txt file, the result will be really good to csv file as well 
  def to_csv_line(str:String,list:List[String]):String = {
    var line = str
    for(i<-0 to list.length-1){
      line = line + ","+ list(i)
    }
    return line
  }
}


// my Assignment2 object
object Assignment2{
  // main function, and return Unit(void)
  def main(args:Array[String]): Unit = {

    // set the input path and output path is here 
    val inputFilePath  = "/import/glass/3/z5143964/Ass2/sample_input.txt"
    val outputDirPath = "/import/glass/3/z5143964/Ass2/output"
    val input = sc.textFile(inputFilePath)

    // split data line by line
    val l1 = input.map(_.split("[\n , ]"))
    // filter "" line
    val l2 = l1.filter(!_.contains(""))
    // what we need is only first column and third column
    // extract them from data
    val l3 = l2.map(pair => (pair(0),pair(3)))
    // group by key
    val l4 = l3.groupByKey()
    //println(l4.collect().toBuffer)

    // the element in the value, processed by KB_MB_to_B function and return new value
    val l6 = l4.mapValues(_.map(x => new myfunction().KB_MB_to_B(x)))
    
    // sort the key
    val l7 = l6.sortByKey()
    // sort the value
    val l8 = l7.mapValues(_.toList.sortBy(x=>x))
    
    // use the function get_mean_and_varience to add mean and varience in value
    // and also get the min and max value as required
    val l9 = l8.mapValues(x => new myfunction().get_mean_and_varience(x))
    //println(l9.collect().toBuffer)

    // change the value in to required output model
    val l10 = l9.map(x => new myfunction().to_csv_line(x._1,x._2))

    // save all the output into one file
    // according to the forum we don't need to output csv file
    // we just need to output csv type txt, right?
    // so the output type is txt 
    l10.coalesce(1,true).saveAsTextFile(outputDirPath)
    

    // But i also can ouput csv file 
    // change the data to dataframe
    // and use df attribute to save as csv file
    // uncommend the code
    //*****    output as csv file  ****
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






