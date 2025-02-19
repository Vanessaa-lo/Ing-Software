document.addEventListener('DOMContentLoaded', function() {
    const products = [
        { id: 1, name: 'Hamburguesa', price: 5.00 },
        { id: 2, name: 'Pizza', price: 8.00 },
        { id: 3, name: 'Ensalada', price: 4.50 },
        { id: 4, name: 'Sushi', price: 10.00 },
        { id: 5, name: 'Tacos', price: 6.00 }
    ];

    const productList = document.getElementById('product-list');
    const productSelect = document.getElementById('product-select');
    const orderItems = document.getElementById('order-items');
    const totalElement = document.getElementById('total');
    const customizeForm = document.getElementById('customize-form');

    let order = [];
    let total = 0;

    // Cargar productos en la lista y en el select
    products.forEach(product => {
        const li = document.createElement('li');
        li.textContent = `${product.name} - ${product.price}€`;
        productList.appendChild(li);

        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        productSelect.appendChild(option);
    });

    // Manejar el formulario de personalización
    customizeForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const productId = parseInt(productSelect.value);
        const quantity = parseInt(document.getElementById('quantity').value);
        const notes = document.getElementById('notes').value;

        const product = products.find(p => p.id === productId);
        if (product) {
            const orderItem = {
                product: product.name,
                quantity: quantity,
                price: product.price,
                notes: notes
            };

            order.push(orderItem);
            total += product.price * quantity;

            updateOrderSummary();
        }
    });

    // Actualizar el resumen del pedido
    function updateOrderSummary() {
        orderItems.innerHTML = '';
        order.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.product} x ${item.quantity} - ${item.price * item.quantity}€ (${item.notes})`;
            orderItems.appendChild(li);
        });

        totalElement.textContent = total.toFixed(2);
    }
});