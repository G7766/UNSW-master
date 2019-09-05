import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import java.io._

import org.mortbay.util.ajax.JSON


import play.api.libs.json._


import scala.xml.XML
import scala.collection.mutable.{ListBuffer, Set}
import scalaj.http._

import scala.util._

object CaseIndex {
  // get all the file in path
  def getAllFiles(dir: String): List[File] = {
    val path = new File(dir)
    if (path.exists && path.isDirectory) {
      return path.listFiles.filter(_.isFile).toList
    } else {
      //println("There is not file or it is not a directory")
      return List[File]()
    }
  }

  // process steps:
  def processAllFile(path: List[File]):Unit= {
    //for all file in path
    //1.load
    //2.process each one by one
    //3.separate each tags to diff parameter
    //4.reconstruct the value and send to the elasticsearch API
    
    path.foreach(file =>{
      println(file)
      val f = xml.XML.loadFile(file)
      //get file name from path: .getname()
      val f_name = file.getName().split("\\.")(0)

      //separate each part
      val name = (f  \ "name").text
      val url = (f \ "AustLII").text

      //val catchphrases = new StringBuilder("")
      // put all the catchphrase into one string List
      //(f  \ "catchphrases" \ "catchphrase").foreach(c => {
      //  catchphrases ++= c.text + " "
      //})
      val catchphrases = new ListBuffer[String]()
      // put all the catchphrase into one string List
      (f  \ "catchphrases" \ "catchphrase").foreach(c => {
        catchphrases += c.text.replace("\"","\\\"")
      })




      val sentences = new ListBuffer[String]()
      (f \ "sentences" \ "sentence").foreach(s => {
        sentences += s.text.replace("\"","\\\"")
      })

      // create set for the entity
      var locations:Set[String] = Set()
      var people: Set[String] = Set()
      var organizations: Set[String] = Set()
      var other: Set[String] = Set()

      // %7B => { , %7D => }
      // POST to analyse sentence list
      //println(sentences)
      sentences.foreach( s => {
        //run the ner annotator without the additional annotators: ner.applyFineGrained =false
        //println("request start:")
        val request_NLP_content =
          """http://localhost:9000/?properties=%7B'annotators':'ner','ner.applyFineGrained':'false','outputFormat':'json'%7D"""
        val feedback_NLP = Http(request_NLP_content)
          .postData(s.mkString)
          .method("POST").header("Content-Type", "application/json")
          .option(HttpOptions.readTimeout(150000))
          .asString.body
        // to json
        val NLP_json = Json.parse(feedback_NLP)
        //println("NLP_json:")
        //print(NLP_json)
        //println(NLP_json.getClass.toString())

        //extract all entities
        val tokens = NLP_json \\ "tokens"
        //println("tokens:")
        //println(tokens)
        tokens.foreach(token => {
          val text = token \\ "word"
          val ner = token \\ "ner"
          // index from the token text
          var i = 0
          for (i <- 0 until text.length) {
            if (ner(i).toString == "\"PERSON\"") {
              people += text(i).toString
            }
            else if (ner(i).toString == "\"LOCATION\"") {
              locations += text(i).toString
            }
            else if (ner(i).toString == "\"ORGANIZATION\"") {
              organizations += text(i).toString
            }
          }

        })
      })
      // finish process sentences
      // send to elasticsearch
      // convert to list
      val people_list = "[" + people.toList.mkString(",") + "]"
      val locations_list = "[" + locations.toList.mkString(",") + "]"
      val organizations_list = "[" + organizations.toList.mkString(",") + "]"
      // new catchphrases
      val catchphrases_str = "[" + catchphrases.map(x => "\"" + x.filter(_ >= ' ') + "\"").mkString(",") + "]"
      //val catchphrases_str = catchphrases.toString.filter(_ >= ' ')
      // new sentence list
      val sentences_list = "[" +
        sentences.map(x => "\"" + x.filter(_ >= ' ') + "\"").mkString(",") + "]"

      //println("people:")
      //println(people_list)
      //println("locations:")
      //println(locations_list)
      //println("oraganizations:")
      //println(organizations_list)
      println("catchphrases_str:")
      println(catchphrases_str)
      //println("sentenecs:")
      //println(sentences_list)
      //println(sentences_list.getClass.toString())

      // create a new document
      println(f_name)
      val fffname = "test111111"
      // test
      //val es_post_data = s"""{"filename":${fffname},"name":${name},"AustLII":${url},"catchphrases":${catchphrases.toString.filter(_ >= ' ')},"sentences":${sentences_list},"person":${people_list},"location":${locations_list},"organization":${organizations_list}}"""
      //val es_post_data = "{\"filename\":\"${f_name}\",\"name\":\"${name}\",\"AustLII\":\"${url}\",\"catchphrases\":\"${catchphrases.toString.filter(_ >= ' ')}\",\"sentences\":\"${sentences_list}\",\"person\":\"${people_list}\",\"location\":\"${locations_list}\",\"organization\":\"${organizations_list}\"}"
      
      
      val es_post_data = s"""{"filename":\"${f_name}\","name":\"${name}\","AustLII":\"${url}\","catchphrases":${catchphrases_str},"sentences":${sentences_list},"person":${people_list},"location":${locations_list},"organization":${organizations_list}}"""
      
      
      // load data to elasticsearch address
      val addresss = "http://localhost:9200/legal_idx111/cases/"+fffname+"?pretty"
      println(addresss)
      val final_result = Http("http://localhost:9200/legal_idx111/cases/"+fffname+"?pretty")
        .postData(es_post_data).method("PUT")
        .header("Content-Type", "application/json")
        .option(HttpOptions.readTimeout(800000))
        .asString
      //println(final_result)
    })
  }

  def main(args: Array[String]): Unit = {
    //val conf = new SparkConf().setAppName("Assignment3").setMaster("local")
    //val sc = new SparkContext(conf)

    val path = args(0)
    //val path = "/import/glass/3/z5143964/Ass3_1/cases_test"
    val paths = getAllFiles(path)
    // paths.foreach(println)
    // ES:port 9200
    // index:
    val index_resquest = Http("http://localhost:9200/legal_idx111")
      .method("PUT")
      .header("Content-Type", "application/json")
      .option(HttpOptions.connTimeout(150000))
      .option(HttpOptions.readTimeout(150000))
      .asString
    // mapping:
    val post_data =
      """{"cases":{"properties":{"filename":{"type":"text"},"name":{"type":"text"},"AustLII":{"type":"text"},"catchphrases":{"type":"text"},"sentences":{"type":"text"},"person":{"type":"text"},"location":{"type":"text"},"organization":{"type":"text"}}}}"""
    val mapping_request = Http("http://localhost:9200/legal_idx111/cases/_mapping?pretty")
      .postData(post_data)
      .method("PUT")
      .header("Content-Type", "application/json")
      .option(HttpOptions.connTimeout(150000))
      .option(HttpOptions.readTimeout(150000))
      .asString

    //println("process start")
    processAllFile(paths)
  }
}

