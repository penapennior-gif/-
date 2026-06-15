

class CategoryModelTest(TestCase):
    def test_create_category(self):
        cat = Category.objects.create(name="Электроника", slug="electronics")
        self.assertEqual(str(cat), "Электроника")
        self.assertEqual(cat.slug, "electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Книги", slug="books")

    def test_create_product(self):
        product = Product.objects.create(
            category=self.category,
            name="Python для начинающих",
            slug="python-beginners",
            description="Отличная книга",
            price=1500.00,
            stock=10,
            featured=True,
            featured_order=1,
            specifications="Мягкая обложка"
        )
        self.assertEqual(str(product), "Python для начинающих")
        self.assertEqual(product.price, Decimal("1500.00"))
        self.assertTrue(product.available)  # default True
        self.assertEqual(product.stock, 10)
        self.assertIsNotNone(product.created)
        self.assertIsNotNone(product.updated)

    def test_negative_stock_not_allowed(self):
        product = Product(
            category=self.category,
            name="Тест",
            slug="test",
            description="...",
            price=100,
            stock=-5
        )
        with self.assertRaises(ValidationError):
            product.full_clean()  # Django валидация (если в модели нет constraints, но можно добавить)

    def test_get_absolute_url(self):
        product = Product.objects.create(
            category=self.category,
            name="Ноутбук",
            slug="laptop",
            description="Игровой",
            price=50000,
            stock=3
        )
        self.assertEqual(product.get_absolute_url(), "/product/laptop/")  # зависит от urls.py, уточните

    def test_default_ordering(self):
        p1 = Product.objects.create(category=self.category, name="A", slug="a", price=10, stock=1, created="2024-01-01 10:00:00")
        p2 = Product.objects.create(category=self.category, name="B", slug="b", price=20, stock=1, created="2024-01-02 10:00:00")
        products = list(Product.objects.all())
        self.assertEqual(products[0], p2)  # сначала новый (по -created)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Техника", slug="tech")
        self.product = Product.objects.create(
            category=self.category,
            name="Телефон",
            slug="phone",
            price=15000,
            stock=5
        )

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            first_name="Иван",
            last_name="Петров",
            email="ivan@example.com",
            phone="+71234567890",
            address="Ленина 10",
            total_price=15000
        )
        self.assertEqual(str(order), f"Заявка #{order.id} - Иван Петров")
        self.assertEqual(order.status, "new")  # default
        self.assertIsNotNone(order.created)
        self.assertIsNotNone(order.updated)

    def test_order_status_choices(self):
        order = Order.objects.create(first_name="Test", last_name="Test", email="t@t.com", phone="1", address="addr", total_price=0)
        for status_code, _ in Order.STATUS_CHOICES:
            order.status = status_code
            order.save()
            self.assertEqual(order.status, status_code)

    def test_order_item_creation(self):
        order = Order.objects.create(first_name="A", last_name="B", email="ab@b.com", phone="1", address="addr", total_price=30000)
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )
        self.assertEqual(str(item), f"{self.product.name} x 2")
        self.assertEqual(item.price, Decimal("15000"))

    def test_order_cascade_delete(self):
        order = Order.objects.create(first_name="C", last_name="D", email="cd@d.com", phone="1", address="addr", total_price=100)
        OrderItem.objects.create(order=order, product=self.product, price=100, quantity=1)
        self.assertEqual(OrderItem.objects.count(), 1)
        order.delete()
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_user_set_null_on_delete(self):
        user = User.objects.create_user(username="temp", password="temp")
        order = Order.objects.create(user=user, first_name="X", last_name="Y", email="x@y.com", phone="1", address="addr", total_price=0)
        user.delete()
        order.refresh_from_db()
        self.assertIsNone(order.user)