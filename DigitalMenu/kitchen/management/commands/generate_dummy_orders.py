from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from datetime import timedelta, date
from kitchen.models import Order  # Adjust this import to your actual app structure

class Command(BaseCommand):
    help = 'Generate dummy orders for the last 2 years'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to generate dummy orders...")
        
        try:
            # Generate orders for the last 2 years
            end_date = date.today()
            start_date = date(end_date.year - 2, end_date.month, end_date.day)
            current_date = start_date

            tables = [1, 2, 3, 4, 5, 6, 7, 8]  # Changed to integers for the table field
            statuses = ['in queue', 'completed', 'cancelled']  # Added your default status
            
            months = {
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
            }
            
            count = 0
            while current_date <= end_date:
                # Create 2-5 orders per day
                for _ in range(random.randint(2, 5)):
                    amount = random.randint(200, 2000)
                    table = random.choice(tables)
                    status = random.choice(statuses)
                    
                    # Weight towards completed orders
                    if random.random() < 0.8:
                        status = 'completed'
                    
                    order = Order.objects.create(
                        table=table,
                        amount=amount,
                        status=status,
                        date=current_date,
                        month=months[current_date.month],  # Converting month number to name
                        year=current_date.year
                    )
                    count += 1
                
                current_date += timedelta(days=1)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created {count} dummy orders'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating orders: {str(e)}'))
            self.stdout.write(self.style.ERROR(f'Error details: {type(e).__name__}'))