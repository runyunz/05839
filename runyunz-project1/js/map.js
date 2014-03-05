(function() {
	// width and height
	var w = 1000;
	var h = 600;

	// projection
	var projection = d3.geo.albersUsa()
							.translate([w/2, h/2])
							.scale([1000]);

	// path
	var path = d3.geo.path()
						.projection(projection);

	// color
	var color = d3.scale.quantize()
				.range(["#7cb109","#008b54","#01d9ff","#016fac","#d0281d","#ff9934","#ec6c3f","#da2a50"]);

	// tooltip
	var tooltip = d3.select("body")
					.append("div")
					.attr("id", "tooltip")
					.style("visibility","hidden");
	tooltip.append("p")
			.attr("id", "state")
			.text("state");
	tooltip.append("hr")
	tooltip.append("p")
			.attr("id", "count")
			.text("count");
	tooltip.append("p")
			.attr("id", "percent")
			.text("percent");

	// svg
	var svg = d3.select("#container")
				.append("svg")
				.attr("width", w)
				.attr("height", h);

	//Load in GeoJSON data
	d3.json("data/state-count.json", function(data){
		var sum = 0;
		d3.json("data/us-states.json", function(json) {
			for (var j = 0; j < json.features.length; j++) {
				var jsonState = json.features[j].properties.name;
				if (jsonState in data) {
					json.features[j].properties.value = parseInt(data[jsonState]);
					sum += parseInt(data[jsonState]);
				}
			}

			color.domain([
				d3.min(json.features, function(d) { return d.properties.value; }),
				d3.max(json.features, function(d) { return d.properties.value; })
			]);

			//Bind data and create one path per GeoJSON feature
			svg.selectAll("path")
				.data(json.features)
				.enter()
				.append("path")
				.attr("d", path)
				.attr("class", "path")
				.style("fill", function(d) {
							var value = d.properties.value;
							if (value) {
				 				return color(value);
				 			} else {
								return "#ccc";
							}
				})
				.style("opacity", 1)
				.on("mouseover", function(d) {
					var percent = d.properties.value/sum * 100;
					tooltip.style("visibility", "visible");
					tooltip.select("#state")
					.html(d.properties.name);
					tooltip.select("#count")
					.html(d.properties.value + " reports");
					tooltip.select("#percent")
					.html(percent.toFixed(2).toString() + "% of total");
				})
				.on("mousemove", function() {
					tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
				})
				.on("mouseout", function() {
					tooltip.style("visibility", "hidden");
				});

			//Load in cities data
			d3.tsv("data/top-cities-processed.tsv", function(cities) {
				svg.selectAll("circle")
				   .data(cities)
				   .enter()
				   .append("circle")
				   .attr("cx", function(d) {
					   return projection([d.longitude, d.latitude])[0];
				   })
				   .attr("cy", function(d) {
						return projection([d.longitude, d.latitude])[1];
				   })
				   .attr("r", function(d) {
				   		return Math.sqrt(parseInt(d.count) * 0.8);
				   })
				   .style("fill", "yellow")
				   .style("opacity", 0.8)
					.on("mouseover", function(d) {
						tooltip.style("visibility", "visible")
								.style("background-color", "#333")
								.style("color", "white")
								.style("border-radius", "10px");
						
						tooltip.select("#state")
						.html(d.city);
						tooltip.select("#count")
						.html(d.count + " reports" );
						tooltip.select("#percent")
						.html("");
					})
					.on("mousemove", function() {
						tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
					})
					.on("mouseout", function() {
						tooltip.style("visibility", "hidden")
							.style("background-color", "white")
							.style("color", "#333")
							.style("border-radius", "0px");

					});

			});	
			
			// lengend
			var legend = svg.selectAll(".legend")
			    .data(color.range())
				.enter().append("g")
			    .attr("class", "legend")
			    .attr("transform", function(d, i) { return "translate(0," + i * 30 + ")"; })
			legend.append("rect")
			      .attr("x", w * 0.85)
			      .attr("y", h * 2/5)
			      .attr("width", 18)
			      .attr("height", 18)
			      .attr("id", function(d){return d;})
			      .style("fill", function(d) {return d;})
			      .style("fill-opacity", 0.9); 
			legend.append("text")
			   .attr("x", w * 0.85 + 75)
			   .attr("y", h * 2/5 + 10)
			   .attr("dy", ".35em")
			   .style("text-anchor", "end")
			   .style("color", "#666")
			   .style("font-size", "16px")
			   .text(function(d) {
			        var r = color.invertExtent(d);
			        return "< " + d3.round(r[1]).toString() ;
			    }
			);
			svg.append("text")
			   .attr("x", w * 0.9 + 70)
			   .attr("y", h * 2/5 - 15)
			   .style("text-anchor", "end")
			   .style("color", "#666")
			   .style("text-align","right")
			   .style("font-weight","bold")
			   .style("font-size","0.8em")
			   .text("Number of Reports");

			//context
			var context = d3.select("#container")
			.append("div")
			.attr("id", "context");
			context.append("h1")
				.attr("id", "title")
				.text("UFO Report in US");
			context.append("p")
			        .attr("class", "content")
			        .html("From 1998 to 2010, <span id = 'sum'>" + sum + "</span> UFO Sightings were reported in United States.<br/> Check the choropleth to see which states and cities are most popular among our extraterrestrial visitors.");
			context.append("p")
			        .attr("class", "content")
			        .html("Visit <a href='http://www.nuforc.org/'> National UFO Reporting Center </a> for more information and data source.");        
		});
	});
})();