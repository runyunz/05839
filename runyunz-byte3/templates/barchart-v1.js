// ----------- EVERY CHART NEEDS DATA --------------
// this is the data we passed from main.py
// the format for data is: 
// [{outcome1: amount1, ..., outcomen: amountn,
// Age:'<6mo'}, ..., {outcome1: amount1, ... , Age: '>7yr'}]
var data = {{data|safe}}
// x_labels is an array of all the ages
var x_labels = {{x_labels|safe}}
// y_labels is an array of all the outcomes 
var y_labels = {{y_labels|safe}}


// uncomment this if you want to see what data looks like on
// the javascript side. You'll need to open the javascript
// console in your browser to see the result
//console.log(data);

// ------- EVERY CHART NEEDS DATA ORGANIZED FOR EASY DISPLAY -----
// for each set of outcomes in the data array (one set of outcomes per age)
// we add a new array (d.outcomes) with information about every sub-bar's 
// y0 and y1 position for that age; and a new value (d.total) with 
// information about the total height of the stacked bar
data.forEach(function(d) {
 // the y0 position (lowest position) for the stacked bars will be 0 
 var y0 = 0;
 // however we want to calculate a y position
// for each of the bars so that they sit on top of each other.
// for this, we need to loop through all of the
// y labels. This runs function(name) once for each y label (name is the current label)
 // and stores each resulting dictionary in the array d.outcomes
 d.outcomes = y_labels.map(function(name) {
  // each outcome has a name, a y0 position (it's bottom), 
// and a y1 position (it's top). d[name] is the number of
// dogs with 'name' as their outcome (for this age)
  res = {name: name, y0: y0, y1: y0 + d[name]};
// and we also have to update y0 for the next rectangle.
  y0 = y0 + d[name];
  // then we return the dictionary we just created (which will be stored in d.outcomes)
  return res;});
 // we also store the total height for this stacked bar
 // (which is the y1 of the last bar (stored at length-1)
 d.total = d.outcomes[d.outcomes.length - 1].y1;
});


// ----------- EVERY CHART NEEDS SOME SETUP --------------
//Width and height and margins for the plot 
var margin = {top: 20, right: 20, bottom: 30, left: 40},
  width = 960 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

// set up the x axis scale to go from 0 to width
// rangeRoundBands sets up the bar width with no 
// fractional pixels, and the .1 specifies the distance between bars
var x_scale = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

// this specifies the domain of the x axis, which is ordinal
x_scale.domain(x_labels);

// set up the y axis scale to go from 0 to height
var y_scale = d3.scale.linear()
      .rangeRound([height, 0]);       

// this specifies the domain of the y axis (0 to the height of
// the tallest bar), which is linear 
y_scale.domain([0, d3.max(data, function(d) { return d.total; })]);

// set up the color scale (there are 6 outcomes) 
var color = d3.scale.ordinal()
      .range(["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
"#80b1d3", "#fdb462"]);

// create the x axis 
var xAxis = d3.svg.axis()
           .scale(x_scale)
           .orient("bottom");

// create the y axis
var yAxis = d3.svg.axis()
          .scale(y_scale)
          .orient("left")
          .tickFormat(d3.format(".2s"));

// associate the y labels with the color scale
color.domain(y_labels);

// ------- D3's DOM MANIPULATION MAGIC GOES HERE -------

// the svg element is for drawing. 
var svg = d3.select("body").append("svg")
  // note that we need to accound for margins 'by hand'
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
// and add a group that is inside the margins
.append("g")
  // this makes sure that everything we do inside this group is translated to margin coordinates
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
// draw the x axis (D3 handles the details in '.call')
svg.append("g")
 .attr("class", "x axis")
 .attr("transform", "translate(0," + height + ")")
 .call(xAxis);

// draw the y axis (D3 handles the details in '.call')
svg.append("g")
 .attr("class", "y axis")
 .call(yAxis)
.append("text")
 .attr("transform", "rotate(-90)")
 .attr("y", 6)
 .attr("dy", ".71em")
 .style("text-anchor", "end")
 .text("Number of Animals");

// The selection '.age' will correspond to the data
var animal = svg.selectAll(".AnimalType")
   // this joins the data to the selected elements
   .data(data)
 // the call to enter() actually creates the elements (one group per bar) and binds it to the data
 .enter().append("g")
   .attr("class", "g")
   .attr("x_position", function (d) {return x_scale(d.AnimalType);})
   .attr("transform", function(d) {return "translate(" + x_scale(d.AnimalType) + ",0)"; });

// this selects 'rect' which will correspond to one rect for each outcome in a bar (age)
animal.selectAll("rect")
    // join the outcome data for that age to each rectangle
   .data(function(d) { return d.outcomes; })
 // the call to enter() creates the elements (one rect per outcome) and binds them to the data
 .enter().append("rect")
   .attr("width", x_scale.rangeBand())
   // use the outcome data to determine y position and height
   .attr("y", function(d) { return y_scale(d.y1); })
   .attr("height", function(d) { return y_scale(d.y0) - y_scale(d.y1); })
   // use the color scale to determine the fill color
   .attr("fill", function(d) { return color(d.name); })
   // and cause it to show a tooltip on mouse over
   .on("mouseover", function(d) {
       //Get this bar's x/y values, then augment for the tooltip
       var xPosition = parseFloat(d3.select(this.parentNode).attr("x_position")) + 
           x_scale.rangeBand() / 2;
       var yPosition = parseFloat(d3.select(this).attr("y")) +   14;

       //Update the tooltip position and value
       d3.select("#tooltip")
           .style("left", xPosition + "px")
           .style("top", yPosition + "px")
           .select("#value")
           .text(d.y1-d.y0 + " animals were " + d.name + ".");

       //Show the tooltip (it's a div that is otherwise always hidden)
       d3.select("#tooltip").classed("hidden", false);
    })
// and cause it to disappear when the mouse exits 
.on("mouseout", function(d) {
       d3.select("#tooltip").classed("hidden", true)});

// create a legend with a 20 pixel high separation between
// items (one item per color in the scale)
var legend = svg.selectAll(".legend")
    // our data is the array of colors we created earlier
    .data(color.domain().slice().reverse())
 .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

// fill it with 18 x 18 rectangles in the colors
legend.append("rect")
    .attr("x", 18)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

// and add text 
legend.append("text")
   .attr("x", 40)
   .attr("y", 9)
   .attr("dy", ".35em")
   .style("text-anchor", "start")
   .text(function(d) { return d; });