package couchdbConnection;

import java.util.List;

import java.net.MalformedURLException;

import com.google.gson.JsonObject;

import org.ektorp.CouchDbConnector;
import org.ektorp.CouchDbInstance;
import org.ektorp.ViewQuery;
import org.ektorp.http.HttpClient;
import org.ektorp.http.StdHttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;

public class couchdbConnect  {
	
	public CouchDbConnector connectToDB(String dbname) throws MalformedURLException{
		
	HttpClient httpClient = new StdHttpClient.Builder()
            .url("http://192.168.99.100:5984/")
            .username("mapUser")
            .password("myCouchDBSecret")
            .build();
	CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);
	
	//test the db existacne
	CouchDbConnector db = dbInstance.createConnector(dbname, true);
	System.out.println(db.getDatabaseName());
	return db;
	}
	
	public List<JsonObject> bulkDocsRetrieve(String view,List<String> keys,CouchDbConnector db) {

			List<JsonObject> docs=null;
			ViewQuery q = new ViewQuery()
			                      .allDocs()
			                      .includeDocs(true)
			                      .keys(keys);
			       
			docs = db.queryView(q, JsonObject.class);
			return docs;
	}

}
