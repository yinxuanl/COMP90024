package com.serverapp.restStructure;

import java.net.MalformedURLException;

import javax.ws.rs.DefaultValue;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;

import org.glassfish.jersey.server.JSONP;

import ResearchResult.TestModel;

@Path("/test")
public class RestTest {

	private TestModel model = new TestModel();
	
	@GET
	@Path("/tweets")
	@Produces({"application/json", "application/javascript"})
    @JSONP(queryParam = "callback")
	public String getTestModel(@DefaultValue("none") @QueryParam("param") String param) throws MalformedURLException
	{	
		System.out.println(param);
		return model.getTestModel().toString();
	}
	
}
