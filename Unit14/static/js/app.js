// variables
let tableData;
let filterButton = d3.select('#filter-btn');
let resetButton = d3.select('#reset-btn');

// global functions
function init() {
    tableData = data; 

    d3.selectAll('select').each(function () {            
        let records = new Set(data.map(item => item[this.id]));
        let elem = d3.select(`#${this.id}`);

        elem.selectAll('*').remove();
        
        records.forEach(item => {
            elem.append('option').text(item);
        });

        elem.property('selectedIndex', -1);
    });

    d3.select('#datetime').property('value', '');    
}

function filter() {
    datetimeFilter = d3.select('#datetime').property('value');

    if (datetimeFilter.length > 0) {

        let dt = new Date(datetimeFilter);

        if (isNaN(dt.getDate())) {
            alert('Invalid date');

        } else {
            let formatDate = `${dt.getMonth() + 1}/${dt.getDate()}/${dt.getFullYear()}`;

            d3.select('#datetime').property('value', formatDate);
            tableData = tableData.filter(item => item.datetime === formatDate );
        }
    }

    d3.selectAll('select').each(function () {
        if (this.selectedIndex !== -1) {
            tableData = tableData.filter(item => item[this.id] === this.options[this.selectedIndex].text);
        }
    });
}

function showTable(){
    let tbody = d3.select('#ufo-table').select("tbody");
    let dataKeys = Object.keys(data[0]);

    tbody.selectAll('*').remove();

    tableData.forEach ( item => {
        let row = tbody.append('tr');

        dataKeys.forEach(column => {
            row.append('td').text(item[column]);
        });
    });
}

// events
filterButton.on('click', () => {
    d3.event.preventDefault();

    filter();
    showTable();
});

resetButton.on('click', () => {
    d3.event.preventDefault();

    init();
    showTable();
})

d3.select(window).on("load", () => {
    init();
    showTable();
});