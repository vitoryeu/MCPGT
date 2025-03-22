# Базовий клас для аукціонів
class BaseAuction:
    def __init__(self):
        self.bids = {}
        self.auction_open = True

    def place_bid(self, bidder_name, bid_amount):
        if self.auction_open:
            self.bids[bidder_name] = bid_amount
            print(f"{bidder_name} зробив ставку на суму {bid_amount} одиниць.")
        else:
            print("Аукціон закритий. Ставки більше не приймаються.")

    def close_auction(self):
        raise NotImplementedError("Цей метод бути реалізований у підкласі.")


# 1. Англійський аукціон (відкриті ставки)
class EnglishAuction(BaseAuction):
    def close_auction(self):
        self.auction_open = False
        if self.bids:
            winner = max(self.bids, key=self.bids.get)
            print(f"[Англійський аукціон] Переможець: {winner} зі ставкою {self.bids[winner]} одиниць.")
        else:
            print("[Англійський аукціон] Ставки не було зроблено.")


# 2. Аукціон з прихованими ставками
class SealedBidAuction(BaseAuction):
    def __init__(self):
        super().__init__()
        self.sealed_bids = []

    def place_bid(self, bidder_name, bid_amount):
        if self.auction_open:
            self.sealed_bids.append((bidder_name, bid_amount))
            print(f"{bidder_name} зробив приховану ставку.")
        else:
            print("Аукціон закритий. Ставки більше не приймаються.")

    def close_auction(self):
        self.auction_open = False
        if self.sealed_bids:
            winner, highest_bid = max(self.sealed_bids, key=lambda x: x[1])
            print(f"[Аукціон з прихованими ставками] Переможець: {winner} зі ставкою {highest_bid} одиниць.")
        else:
            print("[Аукціон з прихованими ставками] Ставки не було зроблено.")


# 3. Голландський аукціон
class DutchAuction:
    def __init__(self, starting_price, decrement, min_price):
        self.current_price = starting_price
        self.decrement = decrement
        self.min_price = min_price
        self.winner = None

    def simulate(self, bidder_name):
        print(f"[Голландський аукціон] Початкова ціна: {self.current_price} одиниць.")
        while self.current_price >= self.min_price:
            response = input(f"{bidder_name}, чи приймаєте поточну ціну {self.current_price}? (y/n): ").strip().lower()
            if response == 'y':
                self.winner = (bidder_name, self.current_price)
                print(f"[Голландський аукціон] {bidder_name} погодився на ціну {self.current_price} одиниць.")
                return
            self.current_price -= self.decrement
        print("[Голландський аукціон] Ніхто не прийняв ціну.")

print("Англійський аукціон")
english = EnglishAuction()
english.place_bid("Петро", 100)
english.place_bid("Віталій", 150)
english.place_bid("Орест", 120)
english.close_auction()
print()
print("Аукціон з прихованими ставками")
sealed = SealedBidAuction()
sealed.place_bid("Петро", 110)
sealed.place_bid("Віталій", 140)
sealed.place_bid("Орест", 130)
sealed.close_auction()
print()
print("Голландський аукціон")
dutch = DutchAuction(starting_price=200, decrement=10, min_price=100)
dutch.simulate("Віталій")
