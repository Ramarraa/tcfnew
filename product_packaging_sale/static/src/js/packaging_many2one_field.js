/** @odoo-module **/

import { registry } from "@web/core/registry";
import {
    buildM2OFieldDescription,
    Many2OneField,
} from "@web/views/fields/many2one/many2one_field";


export class PackagingMany2OneField extends Many2OneField {
    get m2oProps() {
        const props = super.m2oProps;
        const uomValue = this.props.record.data.product_uom_id;
        const referenceUomId = Array.isArray(uomValue)
            ? uomValue[0]
            : uomValue && typeof uomValue === "object"
              ? uomValue.id
              : uomValue;

        const productValue = this.props.record.data.product_id;
        const productId = Array.isArray(productValue)
            ? productValue[0]
            : productValue && typeof productValue === "object"
              ? productValue.id
              : productValue;

        return {
            ...props,
            context: {
                ...props.context,
                packaging_reference_uom_id: referenceUomId || false,
                packaging_reference_qty: this.props.record.data.product_uom_qty || 1.0,
                packaging_product_id: productId || false,
            },
        };
    }
}

registry.category("fields").add("packaging_many2one", {
    ...buildM2OFieldDescription(PackagingMany2OneField),
    component: PackagingMany2OneField,
});
