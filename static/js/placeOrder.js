function getPrice(product) {
    var selProduct = product.value;
    var priceField = document.getElementById('newLIPrice')
    
    var ajaxRequest = new XMLHttpRequest()
    
    var params = "product=" + selProduct;
    ajaxRequest.open("POST", "{{=get_price_url}}", true);
    ajaxRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //ajaxRequest.setRequestHeader("Content-length", params.length);
    //ajaxRequest.setRequestHeader("Connection", "close");

    ajaxRequest.onreadystatechange = function() {//Call a function when the state changes.
	    if(ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
		    //alert("Price retrieved is: " + ajaxRequest.responseText);
		    priceField.value = ajaxRequest.responseText;
	    }
    }
    ajaxRequest.send(params);
}

function sendLine(purchase) {
    var selPurchase = purchase.value;
    var id = {{=userid}}
    var price = document.getElementById('newLIPrice').value;
    var product = document.getElementById('newLIProduct').value;
    var quantity = document.getElementById('newLIQuantity').value;
    
    var ajaxRequest = new XMLHttpRequest()
    
    var params = "id=" + id + "&price=" + price + 
	"&product=" + product + "&quantity=" + quantity;
    ajaxRequest.open("POST", "{{=get_sendLine_url}}", true);
    ajaxRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    ajaxRequest.onreadystatechange = function() {
	if(ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
	    alert("Line is in database!");
	}
    }
    ajaxRequest.send(params);
}

function getLineTotal() {
    var lineTotalField = document.getElementById('newLITotal');
    var quantity = document.getElementById('newLIQuantity').value;
    var price = document.getElementById('newLIPrice').value;
    var lineTotalOld = lineTotalField.value
    var lineTotalNew = quantity * price
    // update Line Total
    lineTotalField.value = lineTotalNew;

    // update Grand Total
    var orderTotalNode = document.getElementById('order_total');
    var orderTotalOld = orderTotalNode.innerHTML
    var orderTotalNew = orderTotalOld - lineTotalOld + lineTotalNew;
    orderTotalNode.innerHTML = orderTotalNew;
}

function addLineItem() {
    var productInput = document.getElementById('newLIProduct');
    var quantityInput = document.getElementById('newLIQuantity');
    var priceInput = document.getElementById('newLIPrice');
    var linetotalInput = document.getElementById('newLITotal');
    var product = productInput.value
    var quantity = quantityInput.value
    var price   = priceInput.value
    var linetotal = linetotalInput.value

    if (product == "None" || quantity <= 0 || price <= 0 || quantity * price != linetotal)
	{ alert("Invalid input.  Please try again!")
	    document.getElementById('order_total').innerHTML -= linetotal
	    document.getElementById("newitemform").reset();
	    return false
	}

    // ... here goes check for sufficient inventory via Ajax ... 

    var liTable = document.getElementById('lineitems');
    var length = liTable.rows.length;
    //alert("Current number of line items is " + length);
    // Create an empty row at the end of the table
    var row = liTable.insertRow(length);
    // Create the row entries and set the class attribute
    var productCell = row.insertCell(0); productCell.className="product";
    var quantityCell = row.insertCell(1); quantityCell.className="quantity";
    var priceCell = row.insertCell(2); priceCell.className="price";
    var linetotalCell = row.insertCell(3); linetotalCell.className="linetotal";

    // copy values into Line Item table
    //alert("Coyping product: " + product);
    productCell.innerHTML = product;
    //alert("Copied product: "  + productCell.innerHTML);
    quantityCell.innerHTML= quantity;
    priceCell.innerHTML   = price;
    linetotalCell.innerHTML=linetotal;

    //clear input cells
    document.getElementById("newitemform").reset();
}
</script>
