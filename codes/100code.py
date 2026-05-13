import datetime

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            return False
        self.stock += quantity
        return True

    def __str__(self):
        return f"[{self.product_id}] {self.name:<15} | 가격: {self.price:>8,d} | 재고: {self.stock:>5}"

class Order:
    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []
        self.total_amount = 0
        self.order_date = datetime.datetime.now()

    def add_item(self, product, quantity):
        if product.update_stock(-quantity):
            self.items.append((product.name, quantity, product.price))
            self.total_amount += product.price * quantity
            return True
        return False

    def print_invoice(self):
        print("\n" + "="*45)
        print(f"주문 번호: {self.order_id}")
        print(f"고객명: {self.customer_name}")
        print(f"주문 일시: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 45)
        for name, qty, price in self.items:
            print(f"{name:<15} {qty:>3} x {price:>8,d} = {qty*price:>10,d}")
        print("-" * 45)
        print(f"총 합계: {self.total_amount:>28,d} 원")
        print("="*45)

class InventoryManager:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def show_inventory(self):
        print("\n[현재 재고 현황]")
        print("-" * 50)
        for p in self.products.values():
            print(p)
        print("-" * 50)

def run_system():
    # 초기 데이터 설정
    manager = InventoryManager()
    manager.add_product(Product("P001", "서버 랙 42U", 1200000, 10))
    manager.add_product(Product("P002", "L3 스위치", 850000, 15))
    manager.add_product(Product("P003", "Cat.6 케이블 300m", 150000, 50))
    manager.add_product(Product("P004", "광트랜시버 SFP", 45000, 100))

    # 재고 확인
    manager.show_inventory()

    # 주문 생성 1
    order1 = Order("ORD-2024-001", "(주)테크솔루션")
    if order1.add_item(manager.products["P001"], 2):
        order1.add_item(manager.products["P003"], 5)
    order1.print_invoice()

    # 주문 생성 2 (재고 부족 시나리오)
    order2 = Order("ORD-2024-002", "네트워크 인프라팀")
    print(f"\n[알림] {manager.products['P002'].name} 주문 시도 중...")
    if not order2.add_item(manager.products["P002"], 20):
        print("결과: 재고가 부족하여 주문을 처리할 수 없습니다.")
    else:
        order2.print_invoice()

    # 최종 재고 확인
    manager.show_inventory()

    # 간단한 분석 보고서
    total_value = sum(p.price * p.stock for p in manager.products.values())
    print(f"\n[창고 자산 리포트]")
    print(f"현재 총 자산 가치: {total_value:,d} 원")

if __name__ == "__main__":
    run_system()