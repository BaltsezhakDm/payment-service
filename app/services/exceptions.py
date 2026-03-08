class OverpaymentError(Exception):
    pass


class InvalidDepositAmountError(Exception):
    pass


class InvalidRefundAmountError(Exception):
    pass

class PaymentNotFoundError(Exception):
    pass

class OrderNotFoundError(Exception):
    pass