
function barGraph(config){
  return function (data){

    var chartScale = d3.scaleLinear()
      .range([0, 500])
      .domain([0, d3.max(data, function(d){return d[config.lengthValue];})]);
    var opaqueScale = d3.scaleLinear()
      .domain(d3.extent(data, function(d){return d[config.opaqueValue];}))
      .range([.5, 1]);

    var chart = d3.select('#'+config.chartId)
      .append('svg')
      .attr('width', config.width)
      .attr('height', config.height)
      .append('g')
      .attr('id', 'margin')
      .attr('transform', 'translate(20,30)');

    var datapoints = chart.selectAll('g.datapoint')
      .data(data)
      .enter()
        .append('g')
        .classed('datapoint', true)
        .attr('transform', function(d,i){return 'translate(0,'+i*25+')';});

    datapoints
      .append('text')
      .attr('y', 20)
      .on('click', function(d){overlap(d[config.labelValue]);})
      .text(function(d){return d[config.labelValue];});

    chart.selectAll('g.datapoint')
      .append('text')
      .attr('y', 20)
      .attr('x', function(d){return 220+chartScale(d[config.lengthValue]);})
      .text(function(d){ return (''+d[config.opaqueValue]).slice(0,4);})
      .attr('font-size', 10);

    chart.selectAll('g.datapoint')
      .append('rect')
      .classed('totals', true)
      .attr('x', 200)
      .attr('y', 0)
      .attr('height', 20)
      .attr('width', function(d){return chartScale(d[config.lengthValue]);})
      .attr('fill', 'blue')
      .attr('opacity', function(d){return opaqueScale(d[config.opaqueValue]);});
  };
}

$.ajax({
  type: 'GET',
  url: '/categories',
  async: true,
  data: {},
  dataType: 'json',
  success: barGraph({
    lengthValue: 'c.businesses',
    opaqueValue: 'c.average',
    labelValue: 'c.name',
    width: 800,
    height: 600,
    chartId: 'chart'
  }),
  error: function(j, s, e){console.log(s); console.log(e);}
});

function overlap(cat){
  $.ajax({
    type: 'GET',
    url: '/overlap',
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
