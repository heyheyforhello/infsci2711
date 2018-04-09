var chartScale;
var opaqueScale;

function categories(data){
  console.log(data);
  topCategories = data.slice(0,20)
  chartScale = d3.scaleLinear()
    .range([0, 500])
    .domain([0, d3.max(topCategories, function(d){return d['c.businesses'];})]);
  opaqueScale = d3.scaleLinear()
    .domain(d3.extent(topCategories, function(d){return d['c.average'];}))
    .range([.5, 1]);

  var chart = d3.select('#chart')
    .append('svg')
    .attr('width', 900)
    .attr('height', 800)
    .append('g')
    .attr('id', 'drawing')
    .attr('transform', 'translate(20,30)');

  chart.selectAll('g.datapoint')
    .data(topCategories)
    .enter()
      .append('g')
      .classed('datapoint', true)
      .attr('transform', function(d,i){return 'translate(0,'+i*25+')';});

  chart.selectAll('g.datapoint')
    .append('text')
    .attr('y', 20)
    .on('click', function(d){overlap(d['c.name']);})
    .text(function(d){return d['c.name'];});

  chart.selectAll('g.datapoint')
    .append('text')
    .attr('y', 20)
    .attr('x', function(d){return 220+chartScale(d['c.businesses']);})
    .text(function(d){ return d['c.businesses'] + " businesses, average rating " + (''+d['c.average']).slice(0,4);})
    .attr('font-size', 10);

  chart.selectAll('g.datapoint')
    .append('rect')
    .classed('totals', true)
    .attr('x', 200)
    .attr('y', 0)
    .attr('height', 20)
    .attr('width', function(d){return chartScale(d['c.businesses']);})
    .attr('fill', 'blue')
    .attr('opacity', function(d){return opaqueScale(d['c.average']);});
}

$.ajax({
  type: 'GET',
  url: 'http://localhost:8080/categories',
  async: true,
  data: {},
  dataType: 'json',
  success: categories,
  error: function(j, s, e){console.log(s); console.log(e);}
});

function overlap(cat){
  $.ajax({
    type: 'GET',
    url: 'http://localhost:8080/overlap',
    async: true,
    data: {category: cat},
    success: drawOverlap
  });
}

function drawOverlap(data){
  console.log(data);
  var chart = d3.select('#chart #drawing')
  var bars = chart.selectAll('rect.overlap')
    .data(data)
    .enter()
      .append('rect')
      .classed('overlap', true)
      .attr('x', 200)
      .attr('y', function(d, i){return i*25;})
      .attr('height', 20)
      .attr('fill', 'red')
      .attr('width', 0);
  chart.selectAll('rect.overlap')
    .transition()
    .attr('width', function(d){return chartScale(d['o.count']);});
}
