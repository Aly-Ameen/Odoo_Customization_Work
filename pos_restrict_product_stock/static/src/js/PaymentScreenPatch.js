/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

// Store the original _finalizeValidation method
const _finalizeValidationOrig = PaymentScreen.prototype._finalizeValidation;

patch(PaymentScreen.prototype, {
    async _finalizeValidation(...args) {
        console.log("DEBUG: PaymentScreenPatch _finalizeValidation is called");
        const result = await _finalizeValidationOrig.apply(this, args);

        try {
            // Get CSRF token from Odoo’s global context
            const csrfToken = window.odoo && window.odoo.csrf_token ? window.odoo.csrf_token : '';

            // Manual JSON-RPC call
            const response = await fetch('/web/dataset/call_kw/product.product/search_read', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Openerp-Session-Id': this.env.session_id || '',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'product.product',
                        method: 'search_read',
                        args: [[], ['id', 'qty_available']],
                        kwargs: {},
                    },
                    id: Math.floor(Math.random() * 10000),
                }),
            });

            const data = await response.json();
            console.log("Manual RPC response:", data);

            if (data.error) {
                throw new Error(data.error.message);
            }

            const updatedStock = data.result;
            console.log("Updating stock for", updatedStock.length, "products");

            // Update existing products in POS database
            for (const record of updatedStock) {
                const product = this.pos.db.get_product_by_id(record.id);
                if (product) {
                    console.log(`Updating product ${record.id}: qty_available from ${product.qty_available} to ${record.qty_available}`);
                    product.qty_available = record.qty_available;
                } else {
                    console.log(`Product ${record.id} not found in POS DB`);
                }
            }

            // Trigger UI refresh without resetting product_by_id
            this.pos.trigger('reload-products');
            console.log("DEBUG: Stock updated and UI refresh triggered in PaymentScreenPatch.js");
        } catch (err) {
            console.error("ERROR: Stock update failed in PaymentScreenPatch.js:", err);
            // Prevent the error from crashing the UI by not rethrowing
        }

        return result;
    },
});