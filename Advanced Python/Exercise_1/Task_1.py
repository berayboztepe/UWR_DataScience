from decimal import Decimal

def vat_invoice(s_list):
    total_net = sum(s_list)
    return total_net * 0.23

def vat_receipt(s_list):
    return sum([price * 0.23 for price in s_list])

shopping_list = [0.1, 0.2, 0.3]

print(vat_invoice(shopping_list), vat_receipt(shopping_list))
print(vat_invoice(shopping_list) == vat_receipt(shopping_list))

shopping_list_decimal = [Decimal(str(price)) for price in shopping_list]

def vat_invoice_decimal(s_list):
    total_net = sum(s_list)
    dec_perc = Decimal('0.23')
    return total_net * dec_perc

def vat_receipt_decimal(s_list):
    dec_perc = Decimal('0.23')
    return sum([price * dec_perc for price in s_list])

print(vat_invoice_decimal(shopping_list_decimal), vat_receipt_decimal(shopping_list_decimal))
print(vat_invoice_decimal(shopping_list_decimal) == vat_receipt_decimal(shopping_list_decimal))
