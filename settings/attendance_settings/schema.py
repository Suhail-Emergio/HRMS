from datetime import date, datetime,time
from ninja import Schema
from typing import *
from employee.basic_details.schema import *
from typing import List, Optional


class AttendanceSettingsSchema(Schema):
    enable_attendance: bool
    default_attendance_status: str
    deduct_salary_for_absent_days: str
    company_start_time: time
    company_end_time: time
    hide_total_hours: bool
    hide_attendance_punches: bool
    disable_web_attendance: bool
    enable_ip_restrictions: bool
    disable_mobile_attendance: bool

class RosterShiftSettingsSchema(Schema):
    enable_roster_shifts: bool
    allow_managers_assign_shifts: bool
    restrict_shift_change_days: int
    restrict_week_off_per_month: int
    restrict_week_off_per_week: int

class ShiftChangeSettingsSchema(Schema):
    allow_employee_shift_change_request: bool
    enable_manager_approval: bool
    default_approval_status: str

class SandwichRulesSettingsSchema(Schema):
    enable_sandwich_rules: bool
    week_off_holidays_between_absents: bool
    week_off_holidays_after_absent: bool
    week_off_holidays_before_absent: bool
    absent_week_offs_holidays_beginning_month: bool
    absent_week_offs_holidays_end_month: bool

class RegularizationPoliciesSchema(Schema):
    enable_justify_punch: bool
    restrict_attendance_justification_days: int
    enable_request_punch: bool
    enable_multiple_punches: bool
    restrict_punch_request_days: int
    punch_approval_status: str
    restrict_duty_punch_employee: int
    restrict_real_time_justify_employee: int
    restrict_punch_request_manager: int
    restrict_attendance_approval_manager: int
    restrict_late_justify_manager: int
    restrict_early_exit_justify_manager: int
    restrict_total_time_justify_manager: int

class TimeManagementPolicySchema(Schema):
    enable_overtime: bool
    overtime_approval_status: str
    round_off_minutes: bool
    rounding_method: str
    rounding_value: int
    convert_overtime_to_compensation: bool
    comp_off_request_on_overtime: bool
    default_overtime_rule: str
    enable_undertime: bool
    enable_attendance_rules: bool

class CalculationPolicySchema(Schema):
    enable_attendance_unit: bool
    number_of_unit_for_absent: int
    deduct_break_hours: bool
    daily_auto_attendance_calculation: bool
    enable_leave_based_rules: bool
    auto_assign_shift: bool

class WeeklyOffSchema(Schema):
    weekday: str
    all_weeks: Optional[bool]
    second_week: Optional[bool]
    fifth_week: Optional[bool]
    alternate_weeks: Optional[bool]
    all_but_last: Optional[bool]
    third_week: Optional[bool]
    last_two_weeks: Optional[bool]
    first_week: Optional[bool]
    fourth_week: Optional[bool]
    last_week: Optional[bool]