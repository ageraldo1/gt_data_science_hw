function buildMetadata(sample) {

    let sampleData  = d3.selectAll('#sample-metadata');
    sampleData.select('*').remove();
    
    let table = sampleData.append('table');
    table.classed('table', true).classed('table-condensed', true);
    
    let tbody = table.append('tbody');

    d3.json(`/metadata/${sample}`).then((data) => {
        for (var elem in data.result) {
            let row = tbody.append('tr');

            row.append('td').append('strong').text(elem);
            row.append('td').append('small').text(data.result[elem]);    
        }

        // BONUS: Build the Gauge Chart
        buildGauge(data.result.wfreq);

    });  
  }
  
  function buildCharts(sample) {    
    // @TODO: Build a Bubble Chart using the sample data
    d3.json(`/samples/${sample}/-1`).then((data) => {
      let values = [];
      let labels = [];
      let hover = [];

      data.result.forEach((item) => {
        labels.push(item.otu_id);
        values.push(item.sample_value);
        hover.push(item.otu_label);
      });

      let graphData = [{
        x: labels,
        y: values,
        text: hover,
        mode: 'markers',
        marker: {
          size: values,
          color: labels,
          colorscale: "Earth"
        }
      }];

      let graphLayout = {
        hovermode: 'closest',
        xaxis: {
          title: 'OTU ID'
        },
        font: {size: 14}
      };

      Plotly.newPlot('bubble', graphData, graphLayout);
    });

    // @TODO: Build a Pie Chart
    d3.json(`/samples/${sample}`).then((data) => {
      let values = [];
      let labels = [];
      let hover = [];

      data.result.forEach((item) => {
        labels.push(item.otu_id);
        values.push(item.sample_value);
        hover.push(item.otu_label);
      });

      let graphData = [{
        values: values,
        labels: labels,
        hovertext: hover,
        hoverinfo: 'text',
        type: 'pie'
      }];

      let graphLayout = {
        font: {size: 14}
      };

      Plotly.newPlot('pie', graphData, graphLayout);
    });
     
  }
  
  function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
  
    // Use the list of sample names to populate the select options
    d3.json("/samples").then((sampleNames) => {        
      sampleNames['result'].forEach((sample) => {
        selector
          .append("option")
          .text(sample)
          .property("value", sample);
      });
  
      // Use the first sample from the list to build the initial plots
      if (sampleNames.result.length > 0) {
        const firstSample = sampleNames['result'][0];

        buildCharts(firstSample);
        buildMetadata(firstSample);
      }
    });
  }
  
  function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    buildCharts(newSample);
    buildMetadata(newSample);
  }
  
  // Initialize the dashboard
  init();
  