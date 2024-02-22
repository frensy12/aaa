let coinPriceElement = document.getElementById('coinPrice');
let currentPrice = 100;

// Create a WebSocket connection
const socket = new WebSocket('wss://socketsbay.com/wss/v2/1/demo/');

socket.addEventListener('message', function(event) {
    // Update the price when a message is received from the server
    currentPrice = parseInt(event.data);
    updatePrice();
});

function decreasePrice() {
    currentPrice -= 1.2;
    updatePrice();
    // Send the new price to the server
    socket.send(currentPrice.toString());
}

function increasePrice() {
    currentPrice += 2.9;
    updatePrice();
    // Send the new price to the server
    socket.send(currentPrice.toString());
}

function updatePrice() {
    coinPriceElement.textContent = currentPrice;
}
