/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import RestrictStockPopup from "@pos_restrict_product_stock/js/RestrictStockPopup";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    async addProductToCurrentOrder(product, options = {}) {
        // Prevent multiple calls for the same product
        if (this._processingProduct === product.id) {
            console.warn("⏸️ Skipping duplicate call for product:", product.display_name);
            return;
        }
        this._processingProduct = product.id; // Set flag

        try {
            console.log("🔍 [FIRST CHECK] Attempting to add product:", product.display_name, "Qty Available:", product.qty_available);

            // Ensure qty_available is up-to-date
            const updatedProduct = this.db.get_product_by_id(product.id);
            console.log("🔍 [UPDATED CHECK] Product:", updatedProduct.display_name, "Qty Available:", updatedProduct.qty_available);

            const type = this.config.stock_type;
            const stock_qty = updatedProduct.qty_available;
            const quantity = options.quantity || 1; // Default to 1 if quantity not provided

            // Calculate the total quantity already in the order for this product
            const currentOrder = this.selectedOrder;
            const existingLine = currentOrder.get_orderlines().find(line => line.product.id === updatedProduct.id);
            const currentQuantityInOrder = existingLine ? existingLine.quantity : 0;
            const totalQuantityAfterAdd = currentQuantityInOrder + quantity;

            console.log("🔍 Checking stock for:", updatedProduct.display_name, "Qty Available:", stock_qty, "Requested Quantity:", quantity, "Total Quantity After Add:", totalQuantityAfterAdd);

            // Check if stock restriction applies (either 0 stock initially or exceeding stock limit)
            if (this.config.is_restrict_product && type === 'qty_on_hand' && stock_qty < totalQuantityAfterAdd) {
                console.warn("🚨 Product stock limit reached or out of stock:", updatedProduct.display_name);

                // Show popup to inform the user
                await this.popup.add(RestrictStockPopup, {
                    title: 'Out of Stock',
                    body: `Stock Alert !!||${updatedProduct.display_name} is Out Of Stock||The Available Quantity = ${stock_qty}`,
                    pro_id: updatedProduct.id,
                });

                console.log("🚫 Preventing product addition due to stock limit:", updatedProduct.display_name);
                delete this._processingProduct;
                return; // Exit without adding the product
            }

            console.log("✅ Adding product:", product.display_name);
            const result = await super.addProductToCurrentOrder(product, options);
            delete this._processingProduct;
            return result;
        } catch (error) {
            console.error("ERROR: Failed to add product:", error.message);
            delete this._processingProduct;
            await this.popup.add('ErrorPopup', {
                title: 'Error',
                body: 'Failed to add product: ' + error.message,
            });
        }
    },
});