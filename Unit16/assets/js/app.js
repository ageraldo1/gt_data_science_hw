const dimensions = {
    width: 980,
    height: 600 
};

const margin = {
    top: 20,
    right: 40, 
    bottom: 150,
    left: 120
};

const graphWidth = dimensions.width - margin.left - margin.right;
const graphHeight = dimensions.height - margin.top - margin.bottom;

const svg = d3.select('#scatter')
    .append('svg')
    .attr('width', dimensions.width)
    .attr('height', dimensions.height);

const graph = svg.append('g')
    .attr('width', graphWidth)
    .attr('height', graphHeight)
    .attr('transform', `translate(${margin.left}, ${margin.top})`);    

// scales
const x = d3.scaleLinear().range([0, graphWidth]);
const y = d3.scaleLinear().range([graphHeight, 0]);

// axes groups
const xAxisGroup = graph.append('g')
    .attr('class', 'x-axis')
    .attr('transform', `translate(${0}, ${graphHeight})`);
    
const yAxisGroup = graph.append('g')
    .attr('class', 'y-axis');

// graph selection
scatterFilters = [
    {
        x_attribute: 'poverty',
        x_text: 'In Poverty (%)',
        y_attribute: 'obesity',
        y_text: 'Obese (%)'
    },      
    {
        x_attribute: 'age',
        x_text: 'Age (median)',
        y_attribute: 'smokes',
        y_text: 'Smokes (%)'
    },
    {
        x_attribute: 'income',
        x_text: 'Household Income (Median)',
        y_attribute: 'healthcare',
        y_text: 'Lacks Healthcare (%)'
    }, 
];

let scatterSetup = Object.assign({}, scatterFilters[0]);

// x-axis and y-axis labels
let positionX = graphHeight + 40;
let positionY = 0 - margin.left;

scatterFilters.forEach(item => {
    graph
        .append("text")
        .attr("transform", `translate(${graphWidth / 2}, ${positionX} )`)
        .attr("class", (item.x_attribute === scatterSetup.x_attribute) ? 'active legend-x-axis' : 'inactive legend-x-axis')
        .attr("value", item.x_attribute)
        .text(item.x_text)        
        .on('click', function() {            
            d3.selectAll('.legend-x-axis').classed('active', false);
            d3.selectAll('.legend-x-axis').classed('inactive', true);

            d3.select(this).classed('active', true);           
            d3.select(this).classed('inactive', false);

            let selection  = scatterFilters.filter( item => item.x_attribute == d3.select(this).attr("value"))[0];
            scatterSetup.x_attribute = selection.x_attribute;
            scatterSetup.x_text = selection.x_text;

            update(data);
        });

    graph
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", positionY)
        .attr("x", 0 - (graphHeight/2))
        .attr("dy","1em")
        .attr("class", (item.y_attribute === scatterSetup.y_attribute) ? 'active legend-y-axis' : 'inactive legend-y-axis')
        .attr("value", item.y_attribute)
        .text(item.y_text)
        .on('click', function() {
            d3.selectAll('.legend-y-axis').classed('active', false);
            d3.selectAll('.legend-y-axis').classed('inactive', true);

            d3.select(this).classed('active', true);           
            d3.select(this).classed('inactive', false);

            let selection  = scatterFilters.filter( item => item.y_attribute == d3.select(this).attr("value"))[0];
            scatterSetup.y_attribute = selection.y_attribute;
            scatterSetup.y_text = selection.y_text;

            update(data);
        });
    
    positionX += 25;
    positionY += 30;
});

// tooltip
const tip = d3.tip()
    .attr('class', 'd3-tip')
    .html(d => {
        return `${d.state} <br> ${scatterSetup.x_attribute} : ${d[scatterSetup.x_attribute]} <br>  ${scatterSetup.y_attribute} : ${d[scatterSetup.y_attribute]}`;
    });

graph.call(tip);

const update = (data) => {

    // 1 - set domain scale
    x.domain([d3.min(data, d => +d[scatterSetup.x_attribute] * 0.9), d3.max(data, d => +d[scatterSetup.x_attribute] * 1.02)]);
    y.domain([d3.min(data, d => +d[scatterSetup.y_attribute] * 0.9), d3.max(data, d => +d[scatterSetup.y_attribute] * 1.02)]);

    // 2 - create axes
    const xAxis = d3.axisBottom(x)
    const yAxis = d3.axisLeft(y)
    
    // 3 - call axes
    xAxisGroup.call(xAxis);
    yAxisGroup.call(yAxis);

    // 4 - create circles for objects
    const circles = graph.selectAll('circle')
        .data(data);

    // 5 - add new points
    circles.enter()
        .append('circle')
            .attr('r', 9)
            .attr('cx', d => x(+d[scatterSetup.x_attribute]))
            .attr('cy', d => y(+d[scatterSetup.y_attribute]))
            .attr('class', 'stateCircle')
            .on('mouseover', (d, i, n) => {
                d3.select(n[i]).attr('class', 'hoverCircle');
                tip.show(d, n[i]);
            })
            .on('mouseout', (d, i, n) => {
                d3.select(n[i]).attr('class', 'stateCircle');
                tip.hide(d, n[i]);
            });            

    // 6 - add state text abbreviation
    const abbreviations = graph.selectAll("text")
        .data(data);

    abbreviations.enter()        
        .append('text')
            .selectAll("tspan")
            .data(data)
            .enter()         
                .append("tspan")
                    .attr('class', 'stateText')
                    .style("font-size", "10px")
                    .attr("x", d => x(+d[scatterSetup.x_attribute]))
                    .attr("y", d => y(+d[scatterSetup.y_attribute] - 0.1))                
                    .text(d => d.abbr);

    // 7 - update current points
    circles.transition()
        .duration(500)
            .attr('cx', d => x(+d[scatterSetup.x_attribute]))
            .attr('cy', d => y(+d[scatterSetup.y_attribute]));

    abbreviations.transition()
        .duration(500)
        .selectAll("tspan")
            .attr("x", d => x(+d[scatterSetup.x_attribute]))
            .attr("y", d => y(+d[scatterSetup.y_attribute] - 0.1));

    // 8 - remove unwanted points
    circles.exit().remove();
    abbreviations.exit().remove();
};
    
let data = [];

d3.csv("/assets/data/data.csv").then(response => {
    data = response.map(item => item);

    update(data);
});