package assignment1;

/**
 * NAME: PEIGUO GUAN
 * ZID: z5143964
 * 
 * This class solves the problem posed for Assignment1
 * 
 */
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
//import java.util.Iterator;
import java.util.List;
//import java.util.StringTokenizer;
import java.util.Map;
//import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
//import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
//import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.Job;
//import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;


public class Assignment1 {
  
	
// Map Class the output type is <Object, Text, Text, Text>
public static class TokenizerMapper
			 extends Mapper<Object, Text, Text, Text>{
	
	public void map(Object key, Text value, Context context) 
				throws IOException, InterruptedException {
		
		// To get the value of the number of gram, 
		// in java using context.getConfiguration().get("NumOfgram") to get parameter in mapreduce
		int num_gram = Integer.parseInt(context.getConfiguration().get("NumOfgram"));
		// get current process file name
		// in mapreduce, using context.getInputSplit()).getPath().getName() to get path and file name
		String filename = ((FileSplit) context.getInputSplit()).getPath().getName();
		//Text to string
		String line = value.toString();
		String[] words = line.split(" ");
		
		// to split n gram words ->word
		for (int i=0;i<words.length-num_gram+1;i++) {
			String word="";
			for(int j=0;j<num_gram;j++) {
				if(j==num_gram-1) {
					word = word + words[i+j];
				}
				else {
					word = word + words[i+j]+" ";
				}
			}
			Text word_w = new Text(word);
			// combine count 1 with the n-gram word and send to reduce
			String send = "1" + " "+ filename;
			Text one = new Text(send);
			context.write(word_w, one);
		}
	}
 }

// Reduce class
public static class IntSumReducer extends Reducer<Text,Text,Text,Text> {
	public static Text key_f = new Text();
	public static Text result = new Text();
	
	// build hash map
	//used in cleanup, plz ignore it
	Map<String,String> map=new HashMap<String, String>();
	public void reduce(Text key, Iterable<Text> values,Context context) 
			throws IOException, InterruptedException {
		// transfer the parameter Min number of Count	
		int min_count = Integer.parseInt(context.getConfiguration().get("MinCount"));
		int sum = 0;
		String sum_filename = "";
		
		// Reduce all the value and sum up
		// add the file name in the last
		// if the file name not exit add it
		for (Text val : values) {
			String r = val.toString();
			String[] words = r.split(" ");
				sum += Integer.parseInt(words[0]);
				sum_filename = sum_filename + words[1] + " ";
		}
		
		// Build a String array
		// sort it and add in the Final_result
		String[] str = sum_filename.split(" ");
		
		List<String> list = new ArrayList<String>();
		for (int i=0; i<str.length; i++) {
			if(!list.contains(str[i])) {
					list.add(str[i]);
			}
		}
		// sort 
		Collections.sort(list);
		
		String f = "";
		for (int j=0; j<list.size();j++) {
			if (j==list.size()-1) {
				f = f + list.get(j);
			}
			else{
				f = f + list.get(j)+" "; 
			}
		}
		String Final_result = Integer.toString(sum) + " " + f;
		map.put(key.toString(),Final_result);
		result.set(Final_result);
		
		// filter the result, if number is less than Min number, not write
		if (sum>=min_count) {
				context.write(key, result);
		}
	}
	
	// I just write this part which is the same result as filter in reduce
	// Through it i know the use of clean up
	// this part is new knowledge for me, so i keep it
	// please ignore it
	
//    @Override
//    public void cleanup(Context context) 
//    		throws IOException, InterruptedException{
//    	int min_count = Integer.parseInt(context.getConfiguration().get("MinCount"));
//    	//Map<String,String> map1=new HashMap<String, String>();
//    	//map1 = map;
//    	Map<String, String> treeMap = new TreeMap<String, String>(map);
//    	Iterator<String> iterator = treeMap.keySet().iterator(); 
//    	while (iterator.hasNext()) {
//    		String key = (String)iterator.next(); 
//    		System.out.print(key + " ");
//    		String value = map.get(key);
//    		System.out.println(value);
//    		String[] words = value.split(" ");
//    		if(Integer.parseInt(words[0])>=min_count) {
//        		context.write(new Text(key),new Text(value));
//        	}
//    		
//    	}
//    }
}

public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();
		// pass the parameter to the conf
		conf.set("NumOfgram", args[0]);
		conf.set("MinCount", args[1]);
		
		// Build Job
		Job job = Job.getInstance(conf, "word count");
		
		// to initialize the conf path is on the Assignment1.class path
		job.setJarByClass(Assignment1.class);

		
		// set Mapper class
		job.setMapperClass(TokenizerMapper.class);
		//  do not use combiner cause it will process file by file
		// combiner can help to make it efficient
		// but it is not solution in this assignment
		//  job.setCombinerClass(IntSumReducer.class);
		
		// set Reduce class
		job.setReducerClass(IntSumReducer.class);
		
		// reducer output format
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// input file path -> args[2]
		FileInputFormat.addInputPath(job, new Path(args[2]));;
		// output file path -> args[3]
		FileOutputFormat.setOutputPath(job, new Path(args[3]));
		// waiting for the job to finish
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
	
}