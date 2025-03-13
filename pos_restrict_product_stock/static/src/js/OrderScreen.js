/** @odoo-module */
import { Order, Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import RestrictStockPopup from "@pos_restrict_product_stock/js/RestrictStockPopup";
import rpc from "@web/core/network/rpc_service";

// Function to get the correct stock type from POS settings
function getStockType(pos) {
    return pos.config.stock_type || "virtual"; // Default to 'virtual' if not set
}

// PATCHING ORDERLINE TO DEFER TO PosStore
patch(Orderline.prototype, {
    initialize(...args) {
        super.initialize(...args); // Fix for Odoo 17

        var stockType = getStockType(this.pos);
        const quantity = this.quantity || 1; // Get current or default quantity

        // Defer stock check to PosStore
        if (stockType === "qty_on_hand" && this.product.qty_available < quantity) {
            console.warn("🚨 Orderline: Quantity exceeds available stock, deferring to PosStore");
            this.pos.addProductToCurrentOrder(this.product, { quantity });
            return; // Stop further execution
        }
    },

    set_quantity(quantity) {
        var stockType = getStockType(this.pos);

        if (stockType === "qty_on_hand" && this.product.qty_available < quantity) {
            console.warn("🚨 Orderline: Quantity exceeds available stock, deferring to PosStore");
            // Defer to PosStore instead of showing popup here
            this.pos.addProductToCurrentOrder(this.product, { quantity });
            return; // Stop further execution
        }

        return super.set_quantity(quantity); // Fix for Odoo 17
    }
});

// PATCHING ORDER TO FETCH `new_quantity` FROM BACKEND AFTER PAYMENT VALIDATION
patch(Order.prototype, {
    async validate() {
        console.log("DEBUG: OrderScreen.js validate() is being called"); // Debug log added at the beginning
        const result = await super.validate(...arguments);

        // Fetch updated stock (`new_quantity`) from the backend
        const updated_stock = await rpc.query({
            model: 'stock.change.product.qty',
            method: 'search_read',
            args: [[], ['product_id', 'new_quantity']],
        });

        // Update stock in POS database without reloading the page
        for (const record of updated_stock) {
            let product = this.pos.db.get_product_by_id(record.product_id[0]);
            if (product) {
                product.qty_available = record.new_quantity;
            }
        }

        // Ensure UI displays correct stock immediately
        this.pos.db.product_by_id = {};
        this.pos.db.add_products(this.pos.models.Product);
        this.pos.trigger('reload-products');
        console.log("DEBUG: POS stock updated in real-time using new_quantity from stock.change.product.qty");

        // Return updated stock data along with the validation result
        return { result, updated_stock };
    }
});