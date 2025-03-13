/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";

class RestrictStockPopup extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        console.log("DEBUG: RestrictStockPopup initialized with props:", this.props);
    }

    confirm() {
        console.log("DEBUG: OK clicked with pro_id:", this.props.pro_id);
        // Do not add the product here; PosStore already prevents addition
        this.props.close({ confirmed: true, payload: this.props.pro_id });
    }

    // Remove cancel method to avoid user cancellation
}

RestrictStockPopup.template = 'RestrictStockPopup';
export default RestrictStockPopup;