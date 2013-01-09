package keywordExtraction.tag;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.tagger.maxent.MaxentTagger;

/**
 * @author anthonylife
 * @date 1/9/2013
 * @description: TextTagger label all the words in each document of the
 *               specified corpus with Part-of-speech tags. Note we should
 *               specify the suffix of the documents.
 */
public class TextTagger {
	// file location setting
	private String src_corp_dir = "/home/anthonylife/Doctor/Code/MyPaperCode/" +
			"KeywordExtraction/data/sourcedata/Hulth2003";
	private String doc_suffix = "abstr";
	private String tar_corp_dir = "/home/anthonylife/Doctor/Code/MyPaperCode/" +
			"KeywordExtraction/code/cleanData/Hulth2003";

	// Stanford postagger setting
	private String model_file = "taggers/wsj-0-18-bidirectional-distsim.tagger";
	private MaxentTagger tagger;

	// other variables
	List<String[]> doclist = new ArrayList<String[]>();
	List<String> dirlist = new ArrayList<String>();

	public TextTagger() throws ClassNotFoundException, IOException {
		System.out.println("Do some initilization...");

		// Initialize the tagger
		tagger = new MaxentTagger(model_file);
		getdirlist();
		getdoclist();

		System.out.println("Initilization finished.");
	}

	/*
	 * get the next level directories as there may exist multiple level
	 * directories.
	 */
	public void getdirlist() throws IOException {
		File file = new File(src_corp_dir);
		System.out.println(src_corp_dir);
		if (!file.isDirectory()) {
			System.out.println("Invalid directory!");
			System.exit(0);
		}

		String[] namelist = file.list();
		for (int i = 0; i < namelist.length; i++) {
			//System.out.println(namelist[i]);
			file = new File(src_corp_dir + "/" + namelist[i]);
			if (file.isDirectory()) {
				dirlist.add(file.getPath());
			}
		}
	}

	/* get all the documents list */
	public void getdoclist() throws IOException {
		FileAccept acceptCondition = new FileAccept(doc_suffix);

		for (int i = 0; i < dirlist.size(); i++) {
			File file = new File(dirlist.get(i));
			if (!file.isDirectory()) {
				System.out.println("Invalid directory!");
				System.exit(0);
			}

			String[] namearray = file.list(acceptCondition);
			doclist.add(namearray);
		}
	}
	
	/*
	 * call Stanford tagger to label sentence and output the results to files
	 */
	public void runTagging() throws IOException{
		// Maybe multiple directories in the specified corpus
		for (int  i = 0; i < dirlist.size(); i++){
			String[] temp = dirlist.get(i).split("/");
			String sublevel_dirname = temp[temp.length-1];
			String[] docarray = doclist.get(i);
			
			// for each document
			try {
				for (int j = 0; j < docarray.length; j++){
					String srcdoc_fullname = dirlist.get(i) + "/" + docarray[j];
					String tardoc_fullname = tar_corp_dir + "/" + sublevel_dirname + 
							"/" + docarray[j];
					
					FileReader rd_file = new FileReader(srcdoc_fullname);
					FileWriter wd_file = new FileWriter(tardoc_fullname);
					
					BufferedReader reader = new BufferedReader(rd_file);
					String readline = null;				
					while((readline = reader.readLine()) != null){
						// The tagged string
						String taggedline = tagger.tagString(readline);
						wd_file.write(taggedline+"\n");
					}
					rd_file.close();
					wd_file.close();
				}
			} catch (IOException e) {
					// TODO Auto-generated catch block	
				e.printStackTrace();
				System.out.println("Error when writing target doc!");
				System.exit(0);
			}
		}
		
	}

	public static void main(String[] args) throws ClassNotFoundException, IOException{
		TextTagger textTagger = new TextTagger();
		
		// execute the labeling commander. 
		textTagger.runTagging();
	}
}

/**
 * @description: This class is utilized by "file.list" method
 */
class FileAccept implements FilenameFilter {
	public String s = null;

	FileAccept(String filter_str) {
		s = filter_str;
	}

	@Override
	public boolean accept(File dir, String name) {
		// TODO Auto-generated method stub
		return name.endsWith(s);
	}
}
