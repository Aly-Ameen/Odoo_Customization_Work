**_Inventory Task**_
Fix Summary: Correcting Batch Number Selection Based on Expiry Date and Availability 

**_Issue:**_
The Batch Number field on the product screen was incorrectly displaying the batch (lot) with
the earliest expiration date, even if that lot had no available quantity. The requirement was to
ensure that the batch number reflects the lot with:
1. The earliest expiration date.
2. Available stock (On Hand Quantity > 0).


**_Fix Implementation**_
1. Filter Lots by Expiration Date: The solution retrieves all lots for the product, sorted in
ascending order by expiration date.
2. Check Stock Availability: For each lot, the system verifies if it has available stock by
checking the On Hand Quantity ( product_qty ) in the stock.lot model.
3. Select the First Valid Lot: The first lot that meets both conditions (earliest expiry &
available stock) is assigned to the Batch Number field.
4. Fallback Mechanism: If no valid lot is found, the batch number remains empty to avoid
displaying incorrect information.

5. This fix ensures that the Batch Number field always reflects the most relevant lot, improving
stock traceability and accuracy in product tracking.
