class Order:
    def __init__(self, price, order, status=None):
        self.price = price
        self.order = order
        self.status = status

    @staticmethod
    def order_decoder(order_dict):
        order = Order(**order_dict)
        return order
