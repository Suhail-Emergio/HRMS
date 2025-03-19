from django.shortcuts import render
from ninja import Router
from .schema import *
from settings.attendance_settings.models import *
# Create your views here.

attendance_settings_api = Router(tags=['attendance_settings'])

@attendance_settings_api.post("/attendance_settings", response={201: Message, 403: Message, 409: Message})
async def create_attendance_settings(request, data: AttendenceSettingSchema):
    created_by = request.auth
    if AttendaceSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Attendance Settings already exists for this organization"}
    AttendaceSettings.objects.create(**data.dict())
    return 201, {"message": "Attendance Settings created successfully."}

@attendance_settings_api.get("/attendance_settings", response={200: AttendenceSettingSchema, 404: Message})
async def get_attendance_settings(request, organization:int):
    try:
        attendance_settings = AttendaceSettings.objects.get(organization=organization)
        return 200, attendance_settings
    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}
    
@attendance_settings_api.put("/attendance_settings", response={200: Message, 404: Message})
async def update_attendance_settings(request, data: AttendenceSettingSchema):
    try:
        attendance_settings = AttendaceSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(attendance_settings, key, value)
        attendance_settings.save()
        return 200, {"message": "Attendance Settings updated successfully."}
    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}

@attendance_settings_api.post("/roster_shift_settings", response={201: Message, 403: Message, 409: Message})
async def roster_shift_settings(request, data: RosterShiftSettingsSchema):
    created_by = request.auth
    if RosterShiftSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Roster Shift Settings already exists for this organization"}
    RosterShiftSettings.objects.create(**data.dict())
    return 201, {"message": "Roster Shift Settings created successfully."}

@attendance_settings_api.get("/roster_shift_settings", response={200: RosterShiftSettingsSchema, 404: Message})
async def get_roster_shift_settings(request, organization:int):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=organization)
        return 200, roster_shift_settings
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}
    
@attendance_settings_api.put("/roster_shift_settings", response={200: Message, 404: Message})
async def update_roster_shift_settings(request, data: RosterShiftSettingsSchema):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(roster_shift_settings, key, value)
        roster_shift_settings.save()
        return 200, {"message": "Roster Shift Settings updated successfully."}
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}

   
@attendance_settings_api.post("/shift_change_settings", response={201: Message, 403: Message, 409: Message})
async def shift_change_settings(request, data: ShiftChangeSettingsSchema):
    created_by = request.auth
    if ShiftChangeSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Shift Change Settings already exists for this organization"}
    ShiftChangeSettings.objects.create(**data.dict())
    return 201, {"message": "Shift Change Settings created successfully."}

@attendance_settings_api.get("/shift_change_settings", response={200: ShiftChangeSettingsSchema, 404: Message})
async def get_shift_change_settings(request, organization:int):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=organization)
        return 200, shift_change_settings
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."}
    
@attendance_settings_api.put("/shift_change_settings", response={200: Message, 404: Message})
async def update_shift_change_settings(request, data: ShiftChangeSettingsSchema):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(shift_change_settings, key, value)
        shift_change_settings.save()
        return 200, {"message": "Shift Change Settings updated successfully."}
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."} 
    
@attendance_settings_api.post("/regularization_policies", response={201: Message, 403: Message, 409: Message})
async def regularization_policies(request, data: RegularizationPoliciesSchema):
    created_by = request.auth
    if RegularizationPolicies.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Regularization Policies already exists for this organization"}
    RegularizationPolicies.objects.create(**data.dict())
    return 201, {"message": "Regularization Policies created successfully."}

@attendance_settings_api.get("/regularization_policies", response={200: RegularizationPoliciesSchema, 404: Message})
async def get_regularization_policies(request, organization:int):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=organization)
        return 200, regularization_policies
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
@attendance_settings_api.put("/regularization_policies", response={200: Message, 404: Message})
async def update_regularization_policies(request, data: RegularizationPoliciesSchema):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(regularization_policies, key, value)
        regularization_policies.save()
        return 200, {"message": "Regularization Policies updated successfully."}
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
#sandwich rules

@attendance_settings_api.post("/sandwich_rules", response={201: dict, 409: dict})
def create_sandwich_rules(request, data: SandwichRulesSettingsSchema):
    if SandwichRulesSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Sandwich Rules already exist for this organization."}
    
    SandwichRulesSettings.objects.create(**data.dict())
    return 201, {"message": "Sandwich Rules created successfully."}

@attendance_settings_api.get("/sandwich_rules/{organization_id}", response={200: SandwichRulesSettingsSchema, 404: dict})
def get_sandwich_rules(request, organization_id: int):
    try:
        sandwich_rules = SandwichRulesSettings.objects.get(organization=organization_id)
        return 200, sandwich_rules
    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules not found for this organization."}

@attendance_settings_api.put("/sandwich_rules/{organization_id}", response={200: dict, 404: dict})
def update_sandwich_rules(request, organization_id: int, data: SandwichRulesSettingsSchema):
    try:
        sandwich_rules = SandwichRulesSettings.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(sandwich_rules, key, value)
        sandwich_rules.save()
        return 200, {"message": "Sandwich Rules updated successfully."}
    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules not found for this organization."}
    
# Overtime Compensation and CompOff Settings

# Overtime Settings
@attendance_settings_api.post("/overtime_settings", response={201: dict, 409: dict})
def create_overtime_settings(request, data: OvertimeSettingsSchema):
    if TimeManagementPolicy.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Overtime Settings already exist for this organization."}
    
    TimeManagementPolicy.objects.create(**data.dict())
    return 201, {"message": "Overtime Settings created successfully."}

@attendance_settings_api.get("/overtime_settings/{organization_id}", response={200: OvertimeSettingsSchema, 404: dict})
def get_overtime_settings(request, organization_id: int):
    try:
        overtime_settings = TimeManagementPolicy.objects.get(organization=organization_id)
        return 200, overtime_settings
    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Overtime Settings not found for this organization."}

@attendance_settings_api.put("/overtime_settings/{organization_id}", response={200: dict, 404: dict})
def update_overtime_settings(request, organization_id: int, data: OvertimeSettingsSchema):
    try:
        overtime_settings = TimeManagementPolicy.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(overtime_settings, key, value)
        overtime_settings.save()
        return 200, {"message": "Overtime Settings updated successfully."}
    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Overtime Settings not found for this organization."}

# Compensation Rules
@attendance_settings_api.post("/compensation_rules", response={201: dict, 409: dict})
def create_compensation_rules(request, data: CompensationRulesSchema):
    if CompensationRules.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Compensation Rules already exist for this organization."}
    
    CompensationRules.objects.create(**data.dict())
    return 201, {"message": "Compensation Rules created successfully."}

@attendance_settings_api.get("/compensation_rules/{organization_id}", response={200: CompensationRulesSchema, 404: dict})
def get_compensation_rules(request, organization_id: int):
    try:
        compensation_rules = CompensationRules.objects.get(organization=organization_id)
        return 200, compensation_rules
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found for this organization."}

@attendance_settings_api.put("/compensation_rules/{organization_id}", response={200: dict, 404: dict})
def update_compensation_rules(request, organization_id: int, data: CompensationRulesSchema):
    try:
        compensation_rules = CompensationRules.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(compensation_rules, key, value)
        compensation_rules.save()
        return 200, {"message": "Compensation Rules updated successfully."}
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found for this organization."}

# CompOff Rules
@attendance_settings_api.post("/compoff_rules", response={201: dict, 409: dict})
def create_compoff_rules(request, data: CompOffRulesSchema):
    if CompOffRules.objects.filter(organization=data.organization).exists():
        return 409, {"message": "CompOff Rules already exist for this organization."}
    
    CompOffRules.objects.create(**data.dict())
    return 201, {"message": "CompOff Rules created successfully."}

@attendance_settings_api.get("/compoff_rules/{organization_id}", response={200: CompOffRulesSchema, 404: dict})
def get_compoff_rules(request, organization_id: int):
    try:
        compoff_rules = CompOffRules.objects.get(organization=organization_id)
        return 200, compoff_rules
    except CompOffRules.DoesNotExist:
        return 404, {"message": "CompOff Rules not found for this organization."}

@attendance_settings_api.put("/compoff_rules/{organization_id}", response={200: dict, 404: dict})
def update_compoff_rules(request, organization_id: int, data: CompOffRulesSchema):
    try:
        compoff_rules = CompOffRules.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(compoff_rules, key, value)
        compoff_rules.save()
        return 200, {"message": "CompOff Rules updated successfully."}
    except CompOffRules.DoesNotExist:
        return 404, {"message": "CompOff Rules not found for this organization."}