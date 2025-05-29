/* alert('hello');  */



let productData = {};


    Papa.parse("data/products.csv", {
        download: true,
        header: true,
        complete: function(results) {
            const rows = results.data;

            rows.forEach(product => {
                const category = product.category.trim().toLowerCase();

                if (!productData[category]) {
                    productData[category] = [];
                }

                productData[category].push({
                    id: Number(product.id),
                    title: product.title,
                    carat: product.carat ? parseFloat(product.carat) : null,
                    regular_price: parseFloat(product.regular_price),
                    sale_price: parseFloat(product.sale_price),
                    discount: parseInt(product.discount),
                    image: product.image,
                    category: category
                });
            });

            console.log("✅ Final productData:", productData); // <- Debug output
            callback(); // Continue after loading
        }
    });

