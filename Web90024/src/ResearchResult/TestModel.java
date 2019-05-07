package ResearchResult;

import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.ektorp.CouchDbConnector;

import com.google.gson.JsonObject;

import couchdbConnection.couchdbConnect;


public class TestModel {
	private static couchdbConnect connection;
	
	public TestModel(){
		
	}
	
	public List<JsonObject> getTestModel() throws MalformedURLException
	{
		
			CouchDbConnector db = connection.connectToDB("######name of the database");
			List<JsonObject> result= new ArrayList<JsonObject>();
			
//			System.out.println("PARAM:" + param);

			List<String> keys = Arrays.asList(new String[]{"topic_test"});
			result=connection.bulkDocsRetrieve("_all_docs",keys,db);
			
			return result;
		
	}
}
