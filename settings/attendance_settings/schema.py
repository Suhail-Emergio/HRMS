from datetime import date, datetime, time
from ninja import Schema
from typing import *
from employee.basic_details.schema import *

class organizationDetail(Schema):
     id:int
     name:str

class Message(Schema):
    message: str

class AttendenceSettingSchema(Schema):
    organization: int
    enable_attendance: bool
    default_attendance_status:Optional[str]
    deduct_salary_for_absent_days: Optional[str]
    company_start_time:Optional[time]
    company_end_time: Optional[time]
    hide_total_hours: Optional[bool]
    hide_attendance_punches: Optional[bool]
    disable_web_attendance: Optional[bool]
    enable_ip_restrictions: Optional[bool]
    disable_mobile_attendance: Optional[bool]

class RosterShiftSettingsSchema(Schema):
    organization: int
    enable_roster_shifts: Optional[bool]
    allow_managers_assign_shifts: Optional[bool]
    restrict_shift_change_days: Optional[int]
    restrict_week_off_per_month: Optional[int]
    restrict_week_off_per_week: Optional[int]

class ShiftChangeSettingsSchema(Schema):
    organization: int
    allow_employee_shift_change_request: Optional[bool]
    enable_manager_approval: Optional[bool]
    default_approval_status: Optional[str]

class RegularizationPoliciesSchema(Schema):
    organization: int
    enable_justify_punch: Optional[bool]
    restrict_attendance_justification_days: Optional[int]
    enable_request_punch: Optional[bool]
    enable_multiple_punches: Optional[bool]
    restrict_punch_request_days: Optional[int]
    punch_approval_status: Optional[str]
    restrict_duty_punch_employee: Optional[int]
    restrict_real_time_justify_employee: Optional[int]
    restrict_punch_request_manager: Optional[int]
    restrict_attendance_approval_manager: Optional[int]
    restrict_late_justify_manager: Optional[int]
    restrict_early_exit_justify_manager: Optional[int]
    restrict_total_time_justify_manager: Optional[int]

class SandwichRulesSettingsSchema(Schema):
    organization: int
    enable_sandwich_rules: Optional[bool] = False
    week_off_holidays_between_absents: Optional[bool] = False
    week_off_holidays_after_absent: Optional[bool] = False
    week_off_holidays_before_absent: Optional[bool] = False
    absent_week_offs_holidays_beginning_month: Optional[bool] = False
    absent_week_offs_holidays_end_month: Optional[bool] = False

class OvertimeSettingsSchema(Schema):
    organization: int
    enable_overtime: Optional[bool] = False
    overtime_approval_status: Optional[str] = "Manager Approved"
    round_off_minutes: Optional[bool] = False
    rounding_method: Optional[str] = "Standard"
    rounding_value: Optional[int] = 1
    convert_overtime_to_compensation: Optional[bool] = False
    comp_off_request_on_overtime: Optional[bool] = False
    default_overtime_rule: Optional[str] = "Compensation"

class CompensationRulesSchema(Schema):
    organization: int
    daily_eligibility: Optional[str] = None
    weekoff_eligibility: Optional[str] = None
    holiday_eligibility: Optional[str] = None
    daily_rule: Optional[Dict] = None
    weekoff_rule: Optional[Dict] = None
    holiday_rule: Optional[Dict] = None

class CompOffRulesSchema(Schema):
    organization: int
    daily_eligibility: Optional[str] = None
    weekoff_eligibility: Optional[str] = None
    holiday_eligibility: Optional[str] = None
    daily_rule: Optional[Dict] = None
    weekoff_rule: Optional[Dict] = None
    holiday_rule: Optional[Dict] = None