jQuery(document).ready(function($){ 
    alert("reloaded")
                
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
      
}); 

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

function updateShowingList(newShowingStocks, stocks_map){
    // Update the showing stock list
    const tdbody = document.querySelector('.live-search-list');
    tdbody.innerHTML = '';

    newShowingStocks.forEach(stock => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="code">${stocks_map[stock]['code']}</td>
            <td>${stocks_map[stock]['avg_price']}</td>
            <td>${stocks_map[stock]['cagr']}</td>
            <td>
            <label class="search-list">
                <!-- {{ stock }}  -->
                <button type="button" name="selected_stock" onclick="selectStock('${ stock }')">✓</button>
            </label>
            </td>
        `;
        tdbody.appendChild(tr);
    });
    updateSearch()
}

function updateSelectedList(newSelectedStocks){
    // Update the selected stock list
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

function selectStock(selectedStock) {
    // Make an asynchronous GET request to the server
    fetch(`/stock/select_stock?selected_stock=${selectedStock}`)
        .then(response => response.json())
        .then(data => {
            // Update the content dynamically based on the response
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list
            updateSelectedList(newSelectedStocks)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function removeStock(selectedStock) {
    // Make an asynchronous GET request to the server
    fetch(`/stock/remove_stock?removed_stock=${selectedStock}`)
        .then(response => response.json())
        .then(data => {
            // Update the content dynamically based on the response
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list
            updateSelectedList(newSelectedStocks)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function reset() {
    // Make an asynchronous GET request to the server
    fetch(`/stock/reset_filter`)
        .then(response => response.json())
        .then(data => {
            // Update the content dynamically based on the response
            const newShowingStocks = data.new_showing_stocks;
            const newSelectedStocks = data.new_selected_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list
            updateShowingList(newShowingStocks, stocks_map)

            // Update the selected stock list
            updateSelectedList(newSelectedStocks)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function showall() {
    // Make an asynchronous GET request to the server
    fetch(`/stock/show_all_stocks`)
        .then(response => response.json())
        .then(data => {
            // Update the content dynamically based on the response
            const newShowingStocks = data.new_showing_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list
            updateShowingList(newShowingStocks,stocks_map)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function filterStocks() {
    var from_price = document.getElementById('from_price').value;
    var to_price = document.getElementById('to_price').value;
    // Make an asynchronous GET request to the server
    fetch(`/stock/filter_stocks?from_price=${from_price}&to_price=${to_price}`)
        .then(response => response.json())
        .then(data => {
            // Update the content dynamically based on the response
            const newShowingStocks = data.new_showing_stocks;
            const stocks_map = data.stocks_map;

            // Update the showing stock list
            updateShowingList(newShowingStocks,stocks_map)

            document.getElementById('from_price').value = '';
            document.getElementById('to_price').value = '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
}