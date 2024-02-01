// Validate that the start date is less than the end date.
function validateDates() {
    var startDate = document.getElementById('from_date').value;
    var endDate = document.getElementById('to_date').value;

    var startDateObj = new Date(startDate);
    var endDateObj = new Date(endDate);

    if (startDateObj >= endDateObj) {
        alert('Start date must be less than the end date.');
        return false;
    }

    return true;
}

// Function to hide and show the display stocks depending on the text present in the search bar.
function updateSearch(){
    $('.live-search-list tr').each(function(){ 
        $(this).attr('data-search-term', $(this).text().toLowerCase()); 
    }); 
    
    $('.live-search-box').on('keyup', function(){  
        var searchTerm = $(this).val().toLowerCase(); 
        $('.live-search-list tr').each(function(){ 
            if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) { 
                $(this).show(); 
            } else { 
                $(this).hide(); 
            }
        }); 
          
    }); 
}


// Dynamically updating the list of showing stocks.
jQuery(document).ready(function($){ 
    updateSearch()
}); 


/**
 * Updates the showing stock list in the UI.
 *
 * @param {Array} newShowingStocks - The array of stock symbols to display.
 * @param {Object} stocks_map - A map containing information about each stock.
 */
function updateShowingList(newShowingStocks, stocks_map){
    // The html element to be updated.
    const tdbody = document.querySelector('.live-search-list');
    tdbody.innerHTML = '';

    newShowingStocks.forEach(stock => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="text-align: left;">${stocks_map[stock]['company']}</td>
            <td>${stocks_map[stock]['cagr']}</td>
            <td>
            <label class="search-list">
                <!-- {{ stock }}  -->
                <button type="button" name="selected_stock" onclick="selectStock('${stock}')">✓</button>
            </label>
            </td>
        `;
        tdbody.appendChild(tr);
    });

    // Hide/show the new showing stocks depending on the search bar text.
    updateSearch()
}


/**
 * Updates the selected stock list in the UI.
 *
 * @param {Array} newSelectedStocks - The array of selected stock symbols to display.
 */
function updateSelectedList(newSelectedStocks){
    // The html element to be updated.
    const ul2 = document.querySelector('.selected-stock-list');
    ul2.innerHTML = '';

    newSelectedStocks.forEach(stock => {
        const li = document.createElement('li');
        li.classList.add('item');
        li.innerHTML = `
            <label class="selected-list">
                ${stock} 
                <button type="button" onclick="removeStock('${stock}')">x</button>
            </label>`;
        ul2.appendChild(li);
    });
}


/**
 * Handles the selection of a stock.
 *
 * @param {string} selectedStock - The symbol of the selected stock.
 */
function selectStock(selectedStock) {
    // Make a GET request to the server to fetch the new list of selected and showing stocks.
    fetch(`/stock/select_stock?selected_stock=${selectedStock}`)
        .then(response => response.json())
        .then(data => {
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list in the UI.
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list in UI.
            updateSelectedList(newSelectedStocks)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


/**
 * Handles the removal of a stock.
 *
 * @param {string} selectedStock - The symbol of the removed stock.
 */
function removeStock(selectedStock) {
    // Make a GET request to the server to fetch the new list of selected and showing stocks.
    fetch(`/stock/remove_stock?removed_stock=${selectedStock}`)
        .then(response => response.json())
        .then(data => {
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list in the UI.
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list in the UI.
            updateSelectedList(newSelectedStocks)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Resets the selected stock list and removes all applied filters.
function reset() {
    // Make a GET request to the server to fetch the new list of selected and showing stocks.
    fetch(`/stock/reset_filter`)
        .then(response => response.json())
        .then(data => {
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list in the UI.
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list in the UI.
            updateSelectedList(newSelectedStocks)

            // Reset the filter input boxes in the UI.
            document.getElementById('from_cagr').value = '';
            document.getElementById('to_cagr').value = '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Removes all applied filters and displays all non-selected stocks in showing list.
function showall() {
    // Make a GET request to the server to fetch the new list of showing stocks.
    fetch(`/stock/show_all_stocks`)
        .then(response => response.json())
        .then(data => {
            const newShowingStocks = data.new_showing_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list in the UI.
            updateShowingList(newShowingStocks,stocks_map)

            // Reset the filter input boxes in the UI.
            document.getElementById('from_cagr').value = '';
            document.getElementById('to_cagr').value = '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Displays the filtered stocks in the showing list based on filter inputs.
function filterStocks() {
    var from_cagr = document.getElementById('from_cagr').value;
    var to_cagr = document.getElementById('to_cagr').value;
    // Make a GET request to the server to fetch the new list of showing stocks.
    fetch(`/stock/filter_stocks?from_cagr=${from_cagr}&to_cagr=${to_cagr}`)
        .then(response => response.json())
        .then(data => {
            const newShowingStocks = data.new_showing_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list in the UI.
            updateShowingList(newShowingStocks,stocks_map)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Fetch the market data of the selected list of stocks and display the charts in the UI.
async function updateGraph() {
    try {
        // Make a GET request to the server to fetch the market data of the selected stocks.
        const response = await fetch(`/stock/update_graph`);
        const stockDataArray = await response.json();

        // Render the chart plotted using the market data in the UI.
        addGraphImg(stockDataArray);
    } catch (error) {
        console.error('Error:', error);
    }
}


/**
 * Adds candlestick and line graphs to the specified HTML div elements based on the given stock data.
 *
 * @param {Object} stockDataArrayObject - Object containing an array of stock data and related information.
 *                                       Format: { stockDataArray: [ { stock, data }, { stock, data }, ...] }
 */
function addGraphImg(stockDataArrayObject){
    // Removing the existing graphs from the div elements.
    const div = document.querySelector('#graph_ohlc');
    div.innerHTML = '';
    const div2 = document.querySelector('#graph_line');
    div2.innerHTML = '';
    if(stockDataArrayObject.stockDataArray.length==0){
        div.innerHTML = `<p>Please select stocks and update graphs</p>`;
        return;
    }
    stockDataArray = stockDataArrayObject.stockDataArray;

    // Build anychart chart and display in UI.
    anychart.onDocumentReady(function () {

        const chart_ohlc = anychart.stock();
        const chart_line = anychart.stock();

        for (let i = 0; i < stockDataArray.length; i++) {
            const stock = stockDataArray[i];
            var table = anychart.data.table('date');
            table.addData(stock.data);

            mapping_ohlc = table.mapAs({'open':"open",'high': "high", 'low':"low", 'close':"close"});
            const series_ohlc = chart_ohlc.plot(0).candlestick(mapping_ohlc);

            mapping_line = table.mapAs({'value':"close"});
            var series_line = chart_line.plot(0).line(mapping_line);
            
            series_ohlc.name(stock.stock);
            series_line.name(stock.stock);
        }
        chart_ohlc.title("Candlestick Data of Selected Stocks");
        chart_line.title("Closing Price of Selected Stocks");
        chart_ohlc.container('graph_ohlc');
        chart_ohlc.draw();
        chart_line.container('graph_line');
        chart_line.draw();
      });
}