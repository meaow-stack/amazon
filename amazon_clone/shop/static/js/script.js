// Search Suggestions
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const query = this.value;
        const suggestions = document.getElementById('suggestions');
        if (!suggestions) return; // Exit if suggestions element is missing

        suggestions.innerHTML = '';

        if (query.length > 2) {
            const dummySuggestions = ['Laptop', 'Phone', 'Headphones', 'Book'].filter(item =>
                item.toLowerCase().includes(query.toLowerCase())
            );
            dummySuggestions.forEach(item => {
                const div = document.createElement('div');
                div.className = 'dropdown-item';
                div.textContent = item;
                div.onclick = () => {
                    searchInput.value = item;
                    document.getElementById('searchForm')?.submit();
                };
                suggestions.appendChild(div);
            });
            suggestions.classList.add('show');
        } else {
            suggestions.classList.remove('show');
        }
    });
}

// Cart Update
function updateCart(input) {
    const priceCell = input.parentElement.nextElementSibling;
    const totalCell = priceCell?.nextElementSibling;
    if (!priceCell || !totalCell) return; // Exit if DOM structure is invalid

    const priceText = priceCell.textContent.replace('$', '');
    const price = parseFloat(priceText);
    const quantity = parseInt(input.value) || 1; // Default to 1 if invalid

    if (isNaN(price)) return; // Exit if price is invalid
    const newTotal = (price * quantity).toFixed(2);
    totalCell.textContent = `$${newTotal}`;

    const totals = document.querySelectorAll('.item-total');
    let cartTotal = 0;
    totals.forEach(total => {
        const value = parseFloat(total.textContent.replace('$', '')) || 0;
        cartTotal += value;
    });
    const cartTotalElement = document.getElementById('cart-total');
    if (cartTotalElement) {
        cartTotalElement.textContent = `$${cartTotal.toFixed(2)}`;
    }
}

// Product Card Hover Effects
document.querySelectorAll('.product-card')?.forEach(card => {
    card.addEventListener('mouseenter', () => card.classList.add('shadow-lg'));
    card.addEventListener('mouseleave', () => card.classList.remove('shadow-lg'));
});