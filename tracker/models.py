# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
    
class UserProfile(models.Model):
    SHIFT_CHOICES = [
        ("S1", "S1"),
        ("S2", "S2"),
        ("S3", "S3"),
        ("S4", "S4"),
        ("S5", "S5"),
    ]

    JOB_CHOICES = [
        ("RSR", "RSR"),
        ("Hauler", "Hauler"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    shift_type = models.CharField(max_length=2, choices=SHIFT_CHOICES, default="S1")
    job = models.CharField(max_length=50,choices= JOB_CHOICES, default="RSR")

    def __str__(self):
        return f"{self.user.username} | {self.shift_type} | {self.job}"



class Shift(models.Model):

    MOVE_TYPE_CHOICES = [
        ("regular", "Regular Move"),
        ("long", "Long Move"),
        ("pallete", "Pallete Return")
    ]

    JOB_ASSIGNMENTS = [
        ("RSR Replans", "RSR: Replenishments"),
        ("RSR L/D", "RSR: Letdowns/Putaways"),
    ]
    duty = models.CharField(max_length=50, choices=JOB_ASSIGNMENTS)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    regular_move = models.PositiveIntegerField(default=0)
    long_move = models.PositiveIntegerField(default=0)
    pallet_return = models.PositiveIntegerField(default=0)
    downtime_minutes = models.PositiveIntegerField(default=0)
    break_minutes = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")

    move_type = models.CharField(max_length=25, choices= MOVE_TYPE_CHOICES, default='regular')

    @property
    def total_moves(self):
        pallet_return_equiv = (self.pallet_return // 20) * 13
        return self.regular_move + (self.long_move * 2) + pallet_return_equiv
    
    def __str__(self):
        return f"{self.user.get_full_name()} | {self.duty}"
    
    def Production_Percentage(self):
        # 1) Pick target per hour based on duty
        target_per_hour = 13 if self.duty == "RSR Replans" else 31

        # 2) Calculate hours worked
        now = timezone.now()
        elapsed = (self.end_time or now) - self.start_time
        hours_worked = elapsed.total_seconds() / 3600

        # 3) Convert adjustments
        downtime_hours = self.downtime_minutes / 60
        pallet_equiv_hours = self.pallet_return // 20   # 20 pallets = 1 hr
        pallet_equiv_moves = (self.pallet_return // 20) * 13  # 20 pallets = 13 moves

        # 4) Total actual moves (including pallet returns)
        actual_moves = (
            self.regular_move +
            (self.long_move * 2) +
            pallet_equiv_moves
        )

        # 5) Adjust workable hours (never let it drop below 0.25 hr)
        effective_hours = max(0.25, hours_worked - downtime_hours - pallet_equiv_hours)

        # 6) Expected moves
        expected_moves = effective_hours * target_per_hour
        expected_moves = max(1, expected_moves)  # safety

        # 7) Return percentage
        return round((actual_moves / expected_moves) * 100, 1)


    


class Downtime(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='downtimes')
    reason = models.CharField(max_length=255)
    duration = models.IntegerField(default=0)
    
   
    
