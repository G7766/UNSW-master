// Creating Client in scala
import edu.stanford.nlp.pipline.*
import edu.stanford.nlp.simple._

import java.io.File
import java.util.Properties
import java.util.stream.Collections

object CaseIndex{

	def getAllFiles(dir:String):List[File] = {
		val path = new File(dir)
		if (path.exists && path.isDirectory){
			return path.listFiles.filter(_.isFile).toList
		} else{
			IOException => println("There is not file or it is not a directory");
		}
	} 



	def main(args:Array[String]):Unit = {

		path = args(0)
		legal_idx = getAllFiles(path)
		legal_idx.collect().toBuffer
		//cases = types


		//StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

	}
}
