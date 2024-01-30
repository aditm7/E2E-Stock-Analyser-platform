jQuery(document).ready(function($){ 
    alert("reloaded")
                
    $('.live-search-list li').each(function(){ 
    $(this).attr('data-search-term', $(this).text().toLowerCase()); 
    }); 
      
    $('.live-search-box').on('keyup', function(){ 
      
    var searchTerm = $(this).val().toLowerCase(); 
      
        $('.live-search-list li').each(function(){ 
      
            if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) { 
                $(this).show(); 
            } else { 
                $(this).hide(); 
            } 
      
        }); 
      
    }); 
      
}); 

function updateSearch(){
    $('.live-search-list li').each(function(){ 
        $(this).attr('data-search-term', $(this).text().toLowerCase()); 
        }); 
          
        $('.live-search-box').on('keyup', function(){ 
          
        var searchTerm = $(this).val().toLowerCase(); 
          
            $('.live-search-list li').each(function(){ 
          
                if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) { 
                    $(this).show(); 
                } else { 
                    $(this).hide(); 
                } 
          
            }); 
          
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

            // Update the showing stock list
            const ul1 = document.querySelector('.live-search-list');
            ul1.innerHTML = '';

            newShowingStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="search-list">
                        ${stock} 
                        <button type="button" onclick="selectStock('${stock}')">✓</button>
                    </label>`;
                ul1.appendChild(li);
            });
            updateSearch()

            // Update the selected stock list
            const ul2 = document.querySelector('.selected-stock-list');
            ul2.innerHTML = '';

            newSelectedStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="selected-list">
                        ${stock} 
                        <button type="button" onclick="removeStock('${stock}')">X</button>
                    </label>`;
                ul2.appendChild(li);
            });
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

            // Update the showing stock list
            const ul1 = document.querySelector('.live-search-list');
            ul1.innerHTML = '';

            newShowingStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="search-list">
                        ${stock} 
                        <button type="button" onclick="selectStock('${stock}')">✓</button>
                    </label>`;
                ul1.appendChild(li);
            });
            updateSearch()

            // Update the selected stock list
            const ul2 = document.querySelector('.selected-stock-list');
            ul2.innerHTML = '';

            newSelectedStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="selected-list">
                        ${stock} 
                        <button type="button" onclick="removeStock('${stock}')">X</button>
                    </label>`;
                ul2.appendChild(li);
            });
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

            // Update the showing stock list
            const ul1 = document.querySelector('.live-search-list');
            ul1.innerHTML = '';

            newShowingStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="search-list">
                        ${stock} 
                        <button type="button" onclick="selectStock('${stock}')">✓</button>
                    </label>`;
                ul1.appendChild(li);
            });
            updateSearch()

            // Update the selected stock list
            const ul2 = document.querySelector('.selected-stock-list');
            ul2.innerHTML = '';

            newSelectedStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="selected-list">
                        ${stock} 
                        <button type="button" onclick="removeStock('${stock}')">X</button>
                    </label>`;
                ul2.appendChild(li);
            });
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

            // Update the showing stock list
            const ul1 = document.querySelector('.live-search-list');
            ul1.innerHTML = '';

            newShowingStocks.forEach(stock => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="search-list">
                        ${stock} 
                        <button type="button" onclick="selectStock('${stock}')">✓</button>
                    </label>`;
                ul1.appendChild(li);
            });
            updateSearch()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}