/* The purpose of this source code is to sample test suites of varying number of failing tests 
 * from test suites of Defects4J defects to evaluate the affect of number of failing tests on 
 * the quality of patch produced by automated program repair techniques
 * 
 * Input:
 * This code takes as input two arguments: (1) path to file coverage_stats.csv and (2) path to 
 * file coverage_matrix.csv
 * 
 * Output: 
 * Files with naming convention <project><defectid>_<target_normalized_failing_test_count>_<datapoint>_neg.tests 
 * (for e.g., chart26_4_0_neg.tests) which lists the failing tests that satisfy the target normalized failing test count 
 *  
 * command to compile: javac ComputeSubsetsDefects4J.java
 * command to run: java ComputeSubsetsDefects4J <path to coverage_stats.csv> <path to coverage_matrix.csv>
 * 
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;

public class ComputeSubsetsDefects4J {
	
    private static Map<String, List<String>> relevantTestMethods = new HashMap<String, List<String>>();
    private static Map<String, List<String>> triggeringTestMethods = new HashMap<String, List<String>>();
    private static Map<String, List<String>> linesCoveredByTest = new HashMap<String,List<String>>();
    private static Map<String, String> defectLines = new HashMap<String,String>();

    // method to process the coverage matrix files and initialize the above data-structures 
	public static void InitializeDataStructures(String covstatspath, String covmatrixpath) {

		BufferedReader br = null;
		String line = "";
		String delimiter = ",";

		try {
		    br = new BufferedReader(new FileReader(covstatspath));
		    List<String> relTestMethods = new ArrayList<String>();
		    List<String> trigTestMethods = new ArrayList<String>();
		    boolean dflag = false;
		    String prevdefect = "";
		    while ((line = br.readLine()) != null) {
		        String[] record = line.split(delimiter);
		        if(record[0].equals("Defect") || record[2].contains("#0#0.0%")){
		        	continue;
		        }
		        defectLines.put(record[0],record[2].split("#")[0]);
		        		        
		        if (!prevdefect.equals(record[0])) {
		        	if (prevdefect!="") {
		        		relevantTestMethods.put(prevdefect, relTestMethods);
		        		triggeringTestMethods.put(prevdefect, trigTestMethods);
		        		dflag=true;
		        	} 
		        		prevdefect = record[0];
		        		if(dflag) {
		        			relTestMethods = new ArrayList<String>();
		        			trigTestMethods = new ArrayList<String>();
		        			dflag=false;
		        		}
		        	}

		        	if (record[3].equals("relevant")) {
		        		relTestMethods.add(record[1]);
		        	}else if (record[3].equals("triggering")) {
		        		trigTestMethods.add(record[1]);
		        	}
		    }

		} catch (FileNotFoundException e) {
		    e.printStackTrace();
		} catch (IOException e) {
		    e.printStackTrace();
		} finally {
		    if (br != null) {
		        try {
		            br.close();
		        } catch (IOException e) {
		            e.printStackTrace();
		        }
		    }
		}
		
		br = null;
		line = "";
		try {
		    br = new BufferedReader(new FileReader(covmatrixpath));
		    String prevtest = "";
		    String prevdefect = "";
		    List<String> linesCovered = new ArrayList<String>();
		    boolean dflag = false;
		    while ((line = br.readLine()) != null) {
		        String[] record = line.split(delimiter);
		        
		        if(record[0].equals("Defect")){
		        	continue;
		        }
		        if (!prevtest.equals(record[1])) {
		        	if (prevtest!="") {
		        		linesCoveredByTest.put(prevdefect.concat(":::" + prevtest.trim()), linesCovered);
		        		dflag=true;
		        	} 
		        		prevtest = record[1];
		        		prevdefect = record[0];
		        		if(dflag) {
		        			linesCovered = new ArrayList<String>();
		        			dflag=false;
		        		}
		        	}
		        if(record[3]==null) {
		        	System.out.println(record[0] + " " + record[1]);
		        	break;
		        }
		        String[] lines = record[3].split(" ");
		        for(int i=0; i<lines.length; i++) {
		        	linesCovered.add(record[2]+":::"+lines[i].trim());
		        }
		    }

		} catch (FileNotFoundException e) {
		    e.printStackTrace();
		} catch (IOException e) {
		    e.printStackTrace();
		} finally {
		    if (br != null) {
		        try {
		            br.close();
		        } catch (IOException e) {
		            e.printStackTrace();
		        }
		    }
		}

	}
	
	// method to generate csv files for individual defects which are used for creating scatter plots
	private static void generatePlotData() {
		for (Entry<String, List<String>> entry : relevantTestMethods.entrySet())
		{	
			Map<String, Integer> relevantTestID = new HashMap<String, Integer>();
			Map<String, Integer> methodLineID = new HashMap<String, Integer>();
		    String defect = entry.getKey();		    
		    List<String> reltests = entry.getValue();
		    List<String> trigtests = triggeringTestMethods.get(defect);
		    List<String> allRelevantTests = new ArrayList<String>();
		    for(int i=0; i<reltests.size(); i++)
		    	allRelevantTests.add(reltests.get(i));
		    for(int i=0; i<trigtests.size(); i++)
		    	allRelevantTests.add(trigtests.get(i));
		   
			String filename = defect.replace("Buggy", "").toLowerCase() + "_coverage.csv"; 
			File testfile = new File(filename);
			BufferedWriter writer = null;
			try {
				writer = new BufferedWriter(new FileWriter(testfile));
			} catch (IOException e1) {
				e1.printStackTrace();
			}
			try {
				writer.write("TestID\tMethodLineID\n");
			} catch (IOException e1) {
				e1.printStackTrace();
			}
		    int relevanttestuniqueid = 1;
		    int methodlineuniqueid = 1;
		    for(int i=0; i<allRelevantTests.size(); i++){
		    	if (!relevantTestID.containsKey(allRelevantTests.get(i))){
	    			relevantTestID.put(allRelevantTests.get(i), relevanttestuniqueid);
	    			System.out.println(defect + "\t" + allRelevantTests.get(i) + "\t" + relevanttestuniqueid++);
		    	}
		    	List<String> methodLineCovered = linesCoveredByTest.get(defect.concat(":::" + allRelevantTests.get(i)));

		    	for(int j=0; j<methodLineCovered.size(); j++){
		    		if (!methodLineID.containsKey(methodLineCovered.get(j))){
		    			methodLineID.put(methodLineCovered.get(j), methodlineuniqueid++);
		    		}
		    			 try {
		 					writer.write(relevantTestID.get(allRelevantTests.get(i)) + "\t" + methodLineID.get(methodLineCovered.get(j)));
		 					writer.newLine();
		 				} catch (IOException e) {
		 					e.printStackTrace();
		 				}
		    	}
		    }
		    try {
				writer.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	// method to create test suite samples for triggering tests experiments
	// each sampled test suite will have varying #triggering tests
	private static void computeSubsetTriggeringTests(){
		
		for (Entry<String, List<String>> entry : relevantTestMethods.entrySet())			// for each defect
		{
			Map<Integer, List<Integer>> dataPoints = new HashMap<Integer, List<Integer>>();
			int testsperdatapoint=5;
		    String defect = entry.getKey();
		    List<String> reltests = entry.getValue();
		    List<String> trigtests = triggeringTestMethods.get(defect);
		    Map<Integer, ArrayList<ArrayList<Integer>>> sampleperdataPoint = new HashMap<Integer, ArrayList<ArrayList<Integer>>>();
		    
		    // considering defects which have >= 5 triggering tests 
		    if(trigtests.size() >= 5){		    	
		    	
		    	// creating 5 data-points between 1 and #triggering-tests
		    	dataPoints.put(trigtests.size(), Arrays.asList((trigtests.size()/5), 2*trigtests.size()/5, 3*trigtests.size()/5, 4*trigtests.size()/5, trigtests.size())); 
		    	
		    	for(int i=0; i<dataPoints.get(trigtests.size()).size(); i++){  // for each of the five data-points
		    		int datapoint = dataPoints.get(trigtests.size()).get(i);
		    		int c=0;
		    		while (true) {
		    			if(datapoint<trigtests.size()){
		    				ArrayList<Integer> sample = selectRandomTests(datapoint, trigtests);
		    				ArrayList<ArrayList<Integer>> existingtestsets = sampleperdataPoint.get(datapoint);
		    				
		    				if (existingtestsets!=null && !IsPresent(existingtestsets, sample)){
			    					existingtestsets.add(sample);
		    				}else{
		    					existingtestsets = new ArrayList<ArrayList<Integer>>();
		    					existingtestsets.add(sample);
		    				}
		    				sampleperdataPoint.put(datapoint, existingtestsets);
		    				if ((trigtests.size() < testsperdatapoint
									&& sampleperdataPoint.get(datapoint).size() == trigtests.size())
									|| sampleperdataPoint.get(datapoint).size() == testsperdatapoint
									|| datapoint == trigtests.size()) {
		    				
									System.out.println("FOUND " + sampleperdataPoint.get(datapoint).size()
										+ " SAMPLES with #tests per sample= " + datapoint + " samples="
										+ sampleperdataPoint.get(datapoint));
									
									// store samples generated in files
									// e.g. for closure46 (which has total #triggering-test = 3) 
									// we get:
									// FOUND 3 SAMPLES with #tests per sample= 1 samples=[[2], [0], [1]]
									// FOUND 3 SAMPLES with #tests per sample= 2 samples=[[0, 1], [2, 0], [2, 1]]
									// FOUND 1 SAMPLES with #tests per sample= 3 samples=[[0,1,2]]
									// generated file closure46_1_0_neg.tests will contain single triggering test of id 2
									// generated file closure46_1_1_neg.tests will contain single triggering test of id 0
									// generated file closure46_1_2_neg.tests will contain single triggering test of id 1
									// generated file closure46_2_0_neg.tests will contain two triggering tests of ids 0 and 1
									// generated file closure46_2_1_neg.tests will contain two triggering test of ids 2 and 0

								try {
									generateTestFiles(defect, datapoint, sampleperdataPoint.get(datapoint), trigtests, reltests);
								} catch (IOException e) {
									e.printStackTrace();
								}
								break;
							}
		    			}else{
		    				break;
		    			}
		    		}
		    	}		    	
		    }
		}
		
	}
	
	// method to randomly select "datapoint" number of passing tests while sampling for triggering test experiment
	private static ArrayList<Integer> selectRandomTests(int datapoint, List<String>tests) {
		ArrayList<Integer> sample=new ArrayList<Integer>();
		Random generator = new Random();
		if(datapoint < tests.size()){
			while(sample.size() < datapoint)
			{
				int randIndex = generator.nextInt(tests.size());
				if (!sample.contains(randIndex)){
					sample.add(randIndex);
				}
			}
		}
		return sample;
	}
	
	// method to write sampled tests to files for triggering test experiment
	private static void generateTestFiles(String defect, int datapoint, ArrayList<ArrayList<Integer>> samples,  List<String> trigtests, List<String> reltests) throws IOException {
	
			for(int i=0; i<samples.size(); i++){
				String filename = defect.replace("Buggy", "").toLowerCase() + "_" + datapoint + "_" + i + "_neg.tests"; 
				File testfile = new File(filename);
				BufferedWriter writer = new BufferedWriter(new FileWriter(testfile));
				
				System.out.println(filename);
				for(int j=0; j<samples.get(i).size(); j++){
					String trigtest = trigtests.get(samples.get(i).get(j)).replace("#", "::");
					System.out.println(trigtest);
					 try {
						writer.write(trigtest);
						writer.newLine();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
				writer.close();
			}
			
			// creating test file with all the triggering tests 
			String filename = defect.replace("Buggy", "").toLowerCase() + "_" + trigtests.size() + "_" + 0 + "_neg.tests"; 
			File testfile = new File(filename);
			BufferedWriter writer = new BufferedWriter(new FileWriter(testfile));
			
			System.out.println(filename);
			for(int j=0; j<trigtests.size(); j++){
				String trigtest = trigtests.get(j).replace("#", "::");
				System.out.println(trigtest);
				 try {
					writer.write(trigtest);
					writer.newLine();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			writer.close();
		
			// creating files containing positive tests
			String filename1 = defect.replace("Buggy", "").toLowerCase() + "_pos.tests"; 
			File testfile1 = new File(filename1);
			BufferedWriter writer1 = new BufferedWriter(new FileWriter(testfile1));
			
			System.out.println(filename1);
			for(int j=0; j<reltests.size(); j++){
				String reltest = reltests.get(j).replace("#", "::");
				System.out.println(reltest);
				 try {
					writer1.write(reltest);
					writer1.newLine();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			writer1.close();
		}
	
	// helper method for computeSubsetTriggeringTests()
	public static <T> boolean listEqualsNoOrder(List<T> l1, List<T> l2) {
	    final Set<T> s1 = new HashSet<>(l1);
	    final Set<T> s2 = new HashSet<>(l2);
	    return s1.equals(s2);
	}
	
	// helper method for computeSubsetTriggeringTests()
	private static boolean IsPresent(ArrayList<ArrayList<Integer>> existingtestsets, ArrayList<Integer> sample) {
		for(int i=0; i< existingtestsets.size(); i++)
		{	if(listEqualsNoOrder(existingtestsets.get(i),sample))
				return true;
		}
		return false;
	}

	// method used for computing the coverage of a set of tests of a given defect
	private static double computeCoverage(String defect, List<String> subsetTests) {
		Set<String> AlllinesCovered = new HashSet<String>();
		double coverage = 0.0;
		for(int i=0; i<subsetTests.size(); i++) {
			String reltest = subsetTests.get(i).trim();
			AlllinesCovered.addAll(linesCoveredByTest.get(reltest));
		}
		double linescovered =  AlllinesCovered.size();
		double totallines = Double.parseDouble(defectLines.get(defect).trim());
		coverage = linescovered/totallines*100.0;
		return Math.round(coverage*100.0)/100.0;
	}
	
	// method to sample tests for coverage experiment using greedy approach
    private static void computeSubsetCoverageGreedy(){
    	
//    	For each defect, do following for 5 times:
//    		1. let S = set of all failing tests
//    		2. current_cov = coverage(s)
//    		3. For each target coverage T do following for 500 times:
//    			3.1 select a test from the set of passing tests randomly and add it to S (say new set is S')
//    			3.2 if the coverage of S' satisfies T and S' has not been sampled before then break
//    			3.3 if the coverage of S' < T then repeat 3.1 
//    			3.4 if the coverage of S' > T then remove test with highest coverage from S' and repeat 3.1 
    	
    	
    	int numdatapoints = 5;	// for each target coverage we need at-least these many distinct samples
		int datapoint = 1;
		ArrayList<ArrayList<String>> allSampledTests = new ArrayList<ArrayList<String>>();
		Random generator = new Random();
		while (datapoint <= numdatapoints) {
			
//			creating separate output file for each data-point
//			String outfile = "CoverageSampleGreedySimpleChart26_" + datapoint + ".txt";
//			try {
//				System.setOut(new PrintStream(new FileOutputStream(outfile)));
//			} catch (FileNotFoundException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}	
			
	    	double[] targetcoverages = {20, 40.0, 60.0, 80.0, 100.0};
	    	double delta = 10.0; 
	    	for (Entry<String, List<String>> entry : relevantTestMethods.entrySet()) 
			{
				String defect = entry.getKey();
				
				if(!defect.equals("Lang43Buggy")){
					continue;
				}
				
				System.out.println("\nSAMPLING BEGINS FOR DEFECT: " + defect);
		
				List<String> reltests = entry.getValue();
				List<String> trigtests = triggeringTestMethods.get(defect);
				List<String> triggeringTests = new ArrayList<String>();
				List<String> triedPassingTests = new ArrayList<String>();
				ArrayList<String> sampledTests = new ArrayList<String>();
				
				for (int i = 0; i < trigtests.size(); i++)
					triggeringTests.add(defect.concat(":::" + trigtests.get(i)));
				double mincov = Math.round(computeCoverage(defect, triggeringTests) * 100.0) / 100.0; 
				List<String> allRelevantTests = new ArrayList<String>();
				for (int i = 0; i < reltests.size(); i++)
					allRelevantTests.add(defect.concat(":::" + reltests.get(i)));
				for (int i = 0; i < trigtests.size(); i++)
					allRelevantTests.add(defect.concat(":::" + trigtests.get(i)));
				double maxcov = Math.round(computeCoverage(defect, allRelevantTests) * 100.0) / 100.0; 
				
				System.out.println("MIN-COV:" + mincov + " MAX-COV:" + maxcov + " #NEG-TESTS:" + trigtests.size() + " #POS-TESTS:" + reltests.size());
				
				if(maxcov - mincov < 25.0){
					System.out.println("Cannot sample tests for " + defect + " as max - min coverage < 25");
					continue; 
				}
				ArrayList<Double> possibleCoverages = new ArrayList<Double>();
				for (int t = 0; t < targetcoverages.length; t++) {		// for each target coverage
					double targetcov = targetcoverages[t];
					int iterations = 10000;								
					boolean foundflag = false;
					System.out.println("\nTARGET COVERAGE:" + targetcov);	
					while(iterations-- > 0){							// try sampling for 500 times
						triedPassingTests.clear();
						sampledTests.clear();
						sampledTests.addAll(triggeringTests);			// add all triggering tests to the sample
						double currcov = mincov;
						double normcov = 0.0;
						while(triedPassingTests.size() < reltests.size()){		// until there exists some passing tests that are not tried
							int randIndex = generator.nextInt(reltests.size());
							if (!triedPassingTests.contains(reltests.get(randIndex))){	// add randomly selected passing test 
								triedPassingTests.add(reltests.get(randIndex));
								String randompassingtest = defect.concat(":::" + reltests.get(randIndex)); 
								sampledTests.add(randompassingtest);
								currcov = computeCoverage(defect, sampledTests);
								normcov = (double) Math.round(((currcov - mincov) / (maxcov - mincov)) * 100.0);
							//	System.out.println("currcov: " + currcov + " normcov: " + normcov + " targetcov + delta: " + (targetcov + delta)) ;
								if(!possibleCoverages.contains(normcov))
									possibleCoverages.add(normcov);
									
								if (normcov <= targetcov + delta && normcov > targetcov - delta) {
									if(IsAlreadySampled(allSampledTests,sampledTests)==false){
										foundflag = true;
										System.out.println("FOUND SAMPLE");
										System.out.println("normalized-cov:" + normcov + " actual-cov:" + currcov + " sample-size:" + sampledTests.size());
										System.out.println("tests => " + sampledTests.toString());
										allSampledTests.add((ArrayList<String>) sampledTests.clone());
										break;
									}
								}else if(normcov > targetcov + delta){
									sampledTests.remove(randompassingtest);
									// deleteTestWithHighestCoverage(sampledTests, defect, triggeringTests);
								}
							}
						}
						if(foundflag == true){
							break;
						}
					}
				}
				System.out.println(possibleCoverages.toString());
				System.out.println("\nSAMPLING ENDS FOR DEFECT: " + defect);
			}
	    	System.out.println("******** DONE FOR ALL DEFECTS *****************");
			System.out.println("******** DATAPOINT: " + datapoint + "*****************");
			datapoint++;
		}
    }
	
	// helper method for computeSubsetCoverageGreedy()
	public static <T> boolean setEquals(List<String> l1, List<String> l2) {
	    final Set<String> s1 = new HashSet<String>(l1);
	    final Set<String> s2 = new HashSet<String>(l2);
	    return s1.equals(s2);
	}
	
	// helper method for computeSubsetCoverageGreedy()
	private static boolean IsAlreadySampled(ArrayList<ArrayList<String>> existingtestsets, ArrayList<String> sample) {
		for(int i=0; i< existingtestsets.size(); i++)
		{	
			if(existingtestsets.get(i).size() != sample.size()){
				continue;
			}
			if(!existingtestsets.get(i).get(0).split(":::")[0].equals(sample.get(0).split(":::")[0])){
				continue;
			}
			if(listEqualsNoOrder(existingtestsets.get(i),sample)){
				return true;
			}
		}
		return false;
	}
    
    // method used for deleting the test with highest coverage from the sampled tests for coverage experiment
    private static void deleteTestWithHighestCoverage(List<String> sampledTests, String defect, List<String> triggeringTests) {
		double maxcov = -1.0;
		String testWithMaxCov = "";
		List<String> tmptest = new ArrayList<String>();
		
		for(int i=0; i<sampledTests.size(); i++){
			if(triggeringTests.contains(sampledTests.get(i)))  // we do not want to delete any failing tests of high coverage
				continue;
			tmptest.add(sampledTests.get(i));
			double cov = computeCoverage(defect, tmptest);
			if (cov > maxcov){
				maxcov = cov;
				testWithMaxCov = sampledTests.get(i);
			}
		}
		sampledTests.remove(testWithMaxCov);
	}

    
	public static void main(String[] args) {
		
		if (args.length == 2) {
		    	String covstatspath = args[0];
		    	String covmatrixpath = args[1];		
				InitializeDataStructures(covstatspath,covmatrixpath);
//				computeSubsetCoverageGreedy();
//				generatePlotData();
			 	computeSubsetTriggeringTests();
//				computeSubset();
		
		}else{
			System.out.println("ERROR: Invalid arguments. please specify paths to coverage_stats.csv and coverage_matrix.csv files");
			System.exit(1);
		}
	}
	
}
