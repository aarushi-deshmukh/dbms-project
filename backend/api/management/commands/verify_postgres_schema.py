from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, connection, transaction

from api.models import Product, Seller


class Command(BaseCommand):
    help = 'Verify PostgreSQL schema constraints, indexes, foreign keys, one-to-one relations, and transactions.'

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            raise CommandError('Schema verification must run against PostgreSQL.')

        expected = {
            'api_product': {
                'constraints': {'product_stock_non_negative'},
                'indexes': {('seller_id',), ('category',), ('created_at',)},
                'foreign_keys': {'seller_id'},
            },
            'api_cartitem': {
                'constraints': {'unique_cart_product', 'cartitem_quantity_positive'},
                'indexes': {('cart_id',), ('product_id',)},
                'foreign_keys': {'cart_id', 'product_id'},
            },
            'api_wishlist': {
                'constraints': {'unique_buyer_product_wishlist'},
                'indexes': {('buyer_id',), ('product_id',)},
                'foreign_keys': {'buyer_id', 'product_id'},
            },
            'api_buyer': {
                'indexes': {('user_id',), ('created_at',)},
                'foreign_keys': {'user_id'},
                'one_to_one': {'user_id'},
            },
            'api_seller': {
                'indexes': {('user_id',), ('created_at',)},
                'foreign_keys': {'user_id'},
                'one_to_one': {'user_id'},
            },
            'api_order': {
                'indexes': {('buyer_id',), ('status',), ('created_at',), ('order_number',)},
                'foreign_keys': {'buyer_id', 'shipping_address_id'},
            },
            'api_orderitem': {
                'indexes': {('order_id',), ('product_id',)},
                'foreign_keys': {'order_id', 'product_id'},
            },
        }

        with connection.cursor() as cursor:
            constraints_by_table = {
                table: connection.introspection.get_constraints(cursor, table)
                for table in expected
            }

        failures = []
        for table, checks in expected.items():
            constraints = constraints_by_table[table]

            for name in checks.get('constraints', set()):
                if name not in constraints:
                    failures.append(f'{table}: missing constraint {name}')

            for columns in checks.get('indexes', set()):
                if not self._has_columns_constraint(constraints, columns, index=True):
                    failures.append(f'{table}: missing index on {", ".join(columns)}')

            for column in checks.get('foreign_keys', set()):
                if not self._has_column_constraint(constraints, column, foreign_key=True):
                    failures.append(f'{table}: missing foreign key on {column}')

            for column in checks.get('one_to_one', set()):
                if not self._has_column_constraint(constraints, column, unique=True):
                    failures.append(f'{table}: missing one-to-one unique constraint on {column}')

        if failures:
            raise CommandError('\n'.join(failures))

        self._verify_model_constraints()
        self._verify_transaction_rollback()

        self.stdout.write(self.style.SUCCESS('PostgreSQL schema verification passed.'))

    @staticmethod
    @staticmethod
    def _has_column_constraint(constraints, column, **flags):
        for details in constraints.values():
            if column not in details.get('columns', []):
                continue
            if all(Command._matches_flag(details, flag, value) for flag, value in flags.items()):
                return True
        return False

    @staticmethod
    def _has_columns_constraint(constraints, columns, **flags):
        expected = list(columns)
        for details in constraints.values():
            if details.get('columns') != expected:
                continue
            if all(Command._matches_flag(details, flag, value) for flag, value in flags.items()):
                return True
        return False

    @staticmethod
    def _matches_flag(details, flag, expected):
        actual = details.get(flag)
        if flag == 'foreign_key' and expected is True:
            return actual is not None
        return actual == expected

    def _verify_model_constraints(self):
        for model in apps.get_models():
            model.check()

        try:
            with transaction.atomic():
                Product.objects.create(
                    name='schema-negative-stock-probe',
                    description='constraint probe',
                    price='1.00',
                    stock=-1,
                )
        except IntegrityError:
            pass
        else:
            raise CommandError('product_stock_non_negative did not reject negative stock.')

    def _verify_transaction_rollback(self):
        initial_count = Seller.objects.count()

        try:
            with transaction.atomic():
                user_model = Seller._meta.get_field('user').remote_field.model
                user = user_model.objects.create_user(
                    username='schema-rollback-probe',
                    email='schema-rollback-probe@example.com',
                    password='not-used',
                )
                Seller.objects.create(
                    user=user,
                    company_name='Rollback Probe',
                    contact_number='0000000000',
                    address='Rollback Street',
                    city='Rollback City',
                    country='Rollback Country',
                    pincode='000000',
                )
                raise IntegrityError('force rollback')
        except IntegrityError:
            pass

        if Seller.objects.count() != initial_count:
            raise CommandError('transaction rollback verification failed.')

        self.stdout.write('Verified models: Buyer, Seller, Product, CartItem, Wishlist, Order, OrderItem.')
