
function barGraph(data){

    var chartScale = d3.scaleLinear()
      .range([0, 500])
      .domain([0, d3.max(data, function(d){return d.barValue;})]);

    var chart = d3.select('#barChart')
      .append('svg')
      .attr('width', 800)
      .attr('height', 600)
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
      .text(function(d){return d.barLabel;});

    chart.selectAll('g.datapoint')
      .append('text')
      .attr('y', 20)
      .attr('x', function(d){return 150+chartScale(d.barValue);})
      .text(function(d){ return (''+d.barValue).slice(0,4);})
      .attr('font-size', 10);

    chart.selectAll('g.datapoint')
      .append('rect')
      .classed('totals', true)
      .attr('x', 200)
      .attr('y', 0)
      .attr('height', 20)
      .attr('width', function(d){return chartScale(d.barValue);})
      .attr('fill', 'blue');
      
}
