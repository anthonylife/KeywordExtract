package keywordExtraction.tag;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

public class GenWordWordRelatedness {
	// web service address
	private static String WEB_SERVICE_COMPARE = "http://166.111.68.55:8000/"
			+ "wikipediaminer/services/compare";

	// words pair dictionary address
	private static String wordspair_dict = "/home/anthonylife/Doctor/Code/MyPaperCode/"
			+ "KeywordExtraction/sudo apt-get install libc6-dev-i386code/cleanData/Hulth2003/words_pair.dict";

	// words pair similarity value file address
	private static String wordspair_sim_dict = "/home/anthonylife/Doctor/Code/MyPaperCode/"
			+ "KeywordExtraction/code/cleanData/Hulth2003/words_pair.simvalue.dict";

	private static int interval = 10000;
	
	private static DocumentBuilderFactory dbf = DocumentBuilderFactory
			.newInstance();

	public static void main(String[] args) throws ParserConfigurationException,
			SAXException, IOException {
		String[] queryTag = new String[2];
		String url = null;
		double relateness = 0;
		String relateAttrName = "relatedness";
		
		FileReader rd_file = new FileReader(wordspair_dict);
		FileWriter wd_file = new FileWriter(wordspair_sim_dict);

		DocumentBuilder db = dbf.newDocumentBuilder();
		BufferedReader reader = new BufferedReader(rd_file);
		String readline = null;
		int idx = 0;
		
		// start to timing
		long startTime = System.currentTimeMillis();
		
		while ((readline = reader.readLine()) != null) {
			queryTag = readline.split(" ");
			url = WEB_SERVICE_COMPARE + "?term1=" + queryTag[0]
					+ "&term2=" + queryTag[1];

			// parse using builder to get DOM representation of the XML file
			Document dom = db.parse(url);

			Element root = dom.getDocumentElement();

			Element responseLabel = (Element) root.getElementsByTagName(
					"Response").item(0);

			// NodeList senseList = labelEle.getElementsByTagName("Sense");
			String relateStr = responseLabel.getAttribute(relateAttrName);
			
			if (relateStr.length() > 0){
				boolean hasWarning = responseLabel.getAttribute("warning").length() > 0 ? true
					: false;
				if (hasWarning)
					relateness = 0;
				else
					relateness = Double.valueOf(relateStr);
			}else{
				relateness = 0;
			}
			wd_file.write(readline + " " + String.valueOf(relateness) + "\n");
			
			// show time
			idx += 1;
			if (idx % interval == 0){
				long endTime = System.currentTimeMillis();
				System.out.println("Current run time:" + (endTime-startTime)/60 + "s.");
			}
		}
		rd_file.close();
		wd_file.close();
	}
}
