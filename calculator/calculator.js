document.addEventListener('DOMContentLoaded', () => {
    const productSelect = document.getElementById('product-select');
    const quantityInput = document.getElementById('quantity');
    const destinationSelect = document.getElementById('destination-select');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultsContainer = document.getElementById('results-container');

    const productNameResult = document.getElementById('product-name-result');
    const quantityResult = document.getElementById('quantity-result');
    const destinationResult = document.getElementById('destination-result');
    const productCostResult = document.getElementById('product-cost-result');
    const shippingCostResult = document.getElementById('shipping-cost-result');
    const totalLandedCostResult = document.getElementById('total-landed-cost-result');
    const costPerUnitResult = document.getElementById('cost-per-unit-result');
    const disclaimerResult = document.getElementById('disclaimer-result');

    let productsData = [];
    const defaultCurrency = 'USD'; // Calculations will be primarily in USD

    // Fetch product data
    fetch('../products/products.json')
        .then(response => response.json())
        .then(data => {
            productsData = data.products;
            populateProductSelect(productsData);
            // Populate destinations based on the first product initially
            if (productsData.length > 0) {
                populateDestinationSelect(productsData[0]);
            }
        })
        .catch(error => {
            console.error('Error fetching products.json:', error);
            resultsContainer.innerHTML = '<p>Ошибка загрузки данных о продуктах. Пожалуйста, попробуйте позже.</p>';
            resultsContainer.style.display = 'block';
        });

    function populateProductSelect(products) {
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = product.name;
            productSelect.appendChild(option);
        });
        // Add event listener to update destinations when product changes
        productSelect.addEventListener('change', (event) => {
            const selectedProduct = productsData.find(p => p.id === event.target.value);
            if (selectedProduct) {
                populateDestinationSelect(selectedProduct);
            }
        });
    }

    function populateDestinationSelect(product) {
        // Clear previous options
        destinationSelect.innerHTML = '';
        if (product.shipping_cost_per_pallet_usd) {
            Object.keys(product.shipping_cost_per_pallet_usd).forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                // Replace underscores with spaces for display
                option.textContent = city.replace(/_/g, ' ');
                destinationSelect.appendChild(option);
            });
        }
    }

    calculateBtn.addEventListener('click', () => {
        const selectedProductId = productSelect.value;
        const quantity = parseFloat(quantityInput.value);
        const destination = destinationSelect.value;

        if (!selectedProductId || isNaN(quantity) || quantity <= 0 || !destination) {
            alert('Пожалуйста, выберите продукт, укажите корректное количество и выберите город назначения.');
            return;
        }

        const product = productsData.find(p => p.id === selectedProductId);
        if (!product) {
            alert('Выбранный продукт не найден.');
            return;
        }

        // --- Calculation Logic ---
        // Product Cost
        // Using the higher end of the USD price range for calculation.
        // Example: "0.55-0.69" -> use 0.69
        const priceRangeParts = product.price_usd_per_kg.split('-');
        const productPricePerKg = parseFloat(priceRangeParts[priceRangeParts.length - 1]);
        if (isNaN(productPricePerKg)) {
            alert('Ошибка в данных о цене продукта.');
            return;
        }
        const totalProductCost = productPricePerKg * quantity;

        // Shipping Cost
        const palletCapacityKg = product.pallet_capacity_kg || 1000; // Default if not specified
        const shippingCostPerPallet = product.shipping_cost_per_pallet_usd[destination];

        if (typeof shippingCostPerPallet === 'undefined') {
             alert('Стоимость доставки для выбранного города не найдена.');
             return;
        }

        const numberOfPallets = Math.ceil(quantity / palletCapacityKg);
        const totalShippingCost = numberOfPallets * shippingCostPerPallet;

        // Total Landed Cost
        const totalLandedCost = totalProductCost + totalShippingCost;
        const costPerUnit = totalLandedCost / quantity;

        // Display results
        productNameResult.textContent = `Продукт: ${product.name}`;
        quantityResult.textContent = `Количество: ${quantity} кг`;
        destinationResult.textContent = `Город назначения: ${destination.replace(/_/g, ' ')}`;

        productCostResult.textContent = `Общая стоимость товара: $${totalProductCost.toFixed(2)} USD`;
        shippingCostResult.textContent = `Ориентировочная стоимость доставки: $${totalShippingCost.toFixed(2)} USD (${numberOfPallets} паллет(ы))`;
        totalLandedCostResult.textContent = `ИТОГО (товар + доставка): $${totalLandedCost.toFixed(2)} USD`;
        costPerUnitResult.innerHTML = `<strong>Ориентировочная стоимость за кг (с доставкой): $${costPerUnit.toFixed(2)} USD/кг</strong>`;

        disclaimerResult.textContent = 'Примечание: Все расчеты являются ориентировочными и основаны на стандартных условиях. Фактическая стоимость может отличаться. Свяжитесь с нами для получения точного расчета.';
        resultsContainer.style.display = 'block';
    });
});
