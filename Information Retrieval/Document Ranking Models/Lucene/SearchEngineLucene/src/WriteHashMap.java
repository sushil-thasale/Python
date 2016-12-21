import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;


public class WriteHashMap {

	 public void writeToFile(HashMap<String,Long> term_and_freq) throws IOException
	    {	    	
	    	Set keySet = term_and_freq.keySet();
	    	System.out.println("Writing Term-Frequency pair to text file");
			 Iterator i = keySet.iterator();
			 PrintWriter pw = new PrintWriter(new FileWriter("D:\\NEU Study Material\\Semeter 1\\IR\\Assignments\\A04\\run 6\\sorted_term.txt",true));
			 			 
			 Integer line_count = 1;
			 while (i.hasNext()) {
				
				 String rank = line_count.toString();
				 String line = rank + "|";
				 
				 String term = (String) i.next();
				 line = line + term + "|" + term_and_freq.get(term).toString() + "\n";
				 pw.write(line);
				 line_count++; }
			pw.close(); } }
